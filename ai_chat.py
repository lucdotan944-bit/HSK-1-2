"""AI conversation practice ("Luyện hội thoại AI").

Calls Claude through the official anthropic SDK to role-play level-appropriate
Chinese conversations with Vietnamese scaffolding (pinyin, translation, gentle
corrections, suggested replies). Structured outputs (output_config.format)
guarantee a parseable JSON reply.

Runs in one of two modes:
- Real mode when ANTHROPIC_API_KEY is set (on Render: add it as an env var).
- Demo mode otherwise: a small scripted exchange so the whole UI works before
  a key is configured. Demo turns don't consume the daily quota.

Cost controls: Haiku-tier model by default (override with AI_CHAT_MODEL),
short history window, and a per-day turn cap stored in ai_chat_usage.
"""
import logging
import os
from datetime import date

logger = logging.getLogger("hsk-app.ai_chat")

# Model is env-overridable so upgrading tiers is a config change, not a deploy.
AI_CHAT_MODEL = os.environ.get("AI_CHAT_MODEL", "claude-haiku-4-5")
DAILY_LIMIT = int(os.environ.get("AI_CHAT_DAILY_LIMIT", "30"))
MAX_HISTORY_MESSAGES = 12  # bound tokens per request; older turns are dropped

RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "reply_cn": {"type": "string", "description": "Câu trả lời tiếng Trung giản thể, 1-2 câu ngắn"},
        "reply_pinyin": {"type": "string", "description": "Pinyin có dấu thanh của reply_cn"},
        "reply_vi": {"type": "string", "description": "Bản dịch tiếng Việt tự nhiên của reply_cn"},
        "correction": {
            "anyOf": [
                {
                    "type": "object",
                    "properties": {
                        "corrected_cn": {"type": "string"},
                        "explanation_vi": {"type": "string"},
                    },
                    "required": ["corrected_cn", "explanation_vi"],
                    "additionalProperties": False,
                },
                {"type": "null"},
            ],
            "description": "Sửa lỗi câu vừa rồi của học viên, null nếu câu đúng",
        },
        "suggestions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "cn": {"type": "string"},
                    "pinyin": {"type": "string"},
                    "vi": {"type": "string"},
                },
                "required": ["cn", "pinyin", "vi"],
                "additionalProperties": False,
            },
            "description": "2-3 câu trả lời mẫu học viên có thể dùng tiếp",
        },
    },
    "required": ["reply_cn", "reply_pinyin", "reply_vi", "correction", "suggestions"],
    "additionalProperties": False,
}


def is_enabled():
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


_client = None


def _get_client():
    global _client
    if _client is None:
        import anthropic
        _client = anthropic.Anthropic()
    return _client


def _system_prompt(hsk_level, topic_label):
    return f"""Bạn là gia sư hội thoại tiếng Trung thân thiện cho người Việt Nam đang học HSK {hsk_level}.

Nhiệm vụ: đóng vai một người bạn Trung Quốc trò chuyện với học viên về chủ đề "{topic_label}".

Quy tắc bắt buộc:
- Mỗi lượt chỉ trả lời 1-2 câu tiếng Trung giản thể NGẮN, dùng từ vựng và ngữ pháp trong phạm vi HSK {hsk_level} trở xuống.
- Luôn kết thúc bằng một câu hỏi hoặc gợi mở để học viên nói tiếp.
- reply_pinyin: pinyin đầy đủ dấu thanh. reply_vi: dịch tiếng Việt tự nhiên.
- correction: nếu câu tiếng Trung vừa rồi của học viên có lỗi ngữ pháp, dùng sai từ, hoặc thiếu tự nhiên, đưa ra câu sửa đúng (corrected_cn) và giải thích NGẮN GỌN bằng tiếng Việt (explanation_vi), giọng khích lệ. Nếu câu đúng hoặc học viên viết tiếng Việt, để null.
- suggestions: 2-3 câu trả lời mẫu đơn giản (kèm pinyin + nghĩa Việt) mà học viên có thể dùng để đáp lại câu của bạn.
- Nếu học viên viết tiếng Việt vì chưa biết nói thế nào, hãy đáp như thể hiểu ý họ và gợi ý cách nói câu đó bằng tiếng Trung trong suggestions.
- Giữ cuộc trò chuyện tích cực, kiên nhẫn, không giảng dài dòng."""


# Scripted fallback so the feature is fully clickable before an API key exists.
_DEMO_TURNS = [
    {
        "reply_cn": "你好！很高兴认识你。你叫什么名字？",
        "reply_pinyin": "Nǐ hǎo! Hěn gāoxìng rènshi nǐ. Nǐ jiào shénme míngzi?",
        "reply_vi": "Chào bạn! Rất vui được làm quen. Bạn tên là gì?",
        "correction": None,
        "suggestions": [
            {"cn": "我叫小明。", "pinyin": "Wǒ jiào Xiǎomíng.", "vi": "Mình tên là Tiểu Minh."},
            {"cn": "你好！我是学生。", "pinyin": "Nǐ hǎo! Wǒ shì xuésheng.", "vi": "Chào bạn! Mình là học sinh."},
        ],
    },
    {
        "reply_cn": "很好！你从哪儿来？",
        "reply_pinyin": "Hěn hǎo! Nǐ cóng nǎr lái?",
        "reply_vi": "Hay quá! Bạn đến từ đâu?",
        "correction": None,
        "suggestions": [
            {"cn": "我从越南来。", "pinyin": "Wǒ cóng Yuènán lái.", "vi": "Mình đến từ Việt Nam."},
            {"cn": "我是河内人。", "pinyin": "Wǒ shì Hénèi rén.", "vi": "Mình là người Hà Nội."},
        ],
    },
    {
        "reply_cn": "越南很漂亮！你为什么学中文？",
        "reply_pinyin": "Yuènán hěn piàoliang! Nǐ wèishénme xué Zhōngwén?",
        "reply_vi": "Việt Nam đẹp lắm! Vì sao bạn học tiếng Trung?",
        "correction": None,
        "suggestions": [
            {"cn": "因为我想去中国。", "pinyin": "Yīnwèi wǒ xiǎng qù Zhōngguó.", "vi": "Vì mình muốn đi Trung Quốc."},
            {"cn": "我喜欢中文。", "pinyin": "Wǒ xǐhuān Zhōngwén.", "vi": "Mình thích tiếng Trung."},
        ],
    },
    {
        "reply_cn": "加油！我们下次再聊吧。",
        "reply_pinyin": "Jiāyóu! Wǒmen xiàcì zài liáo ba.",
        "reply_vi": "Cố lên nhé! Lần sau mình lại trò chuyện tiếp nha.",
        "correction": None,
        "suggestions": [
            {"cn": "好的，再见！", "pinyin": "Hǎo de, zàijiàn!", "vi": "Được, tạm biệt!"},
            {"cn": "谢谢你！", "pinyin": "Xièxie nǐ!", "vi": "Cảm ơn bạn!"},
        ],
    },
]


def demo_respond(messages):
    """Deterministic scripted reply keyed on how many user turns have happened."""
    user_turns = sum(1 for m in messages if m.get("role") == "user")
    turn = _DEMO_TURNS[min(max(user_turns - 1, 0), len(_DEMO_TURNS) - 1)]
    return dict(turn)


def get_usage_today(conn, user_id):
    row = conn.execute(
        "SELECT count FROM ai_chat_usage WHERE user_id = ? AND day = ?",
        (user_id, date.today().isoformat()),
    ).fetchone()
    return row["count"] if row else 0


def increment_usage(conn, user_id):
    conn.execute(
        """INSERT INTO ai_chat_usage (user_id, day, count) VALUES (?, ?, 1)
           ON CONFLICT(user_id, day) DO UPDATE SET count = count + 1""",
        (user_id, date.today().isoformat()),
    )


class AiChatError(Exception):
    def __init__(self, status_code, message_vi):
        super().__init__(message_vi)
        self.status_code = status_code
        self.message_vi = message_vi


def respond(messages, hsk_level, topic_label):
    """One conversation turn against the real Claude API. Raises AiChatError
    with a Vietnamese, user-displayable message on failure."""
    import anthropic
    import json

    history = [
        {"role": m["role"], "content": m["content"][:500]}
        for m in messages[-MAX_HISTORY_MESSAGES:]
        if m.get("role") in ("user", "assistant") and (m.get("content") or "").strip()
    ]
    if not history or history[-1]["role"] != "user":
        raise AiChatError(400, "Tin nhắn cuối phải là của học viên.")

    try:
        response = _get_client().messages.create(
            model=AI_CHAT_MODEL,
            max_tokens=1024,
            system=_system_prompt(hsk_level, topic_label),
            messages=history,
            output_config={"format": {"type": "json_schema", "schema": RESPONSE_SCHEMA}},
        )
    except anthropic.AuthenticationError:
        logger.exception("AI chat: invalid API key")
        raise AiChatError(503, "API key AI không hợp lệ — người quản trị cần kiểm tra cấu hình.")
    except anthropic.RateLimitError:
        logger.warning("AI chat: rate limited")
        raise AiChatError(503, "AI đang bận, vui lòng thử lại sau một phút.")
    except anthropic.APIStatusError:
        logger.exception("AI chat: API error")
        raise AiChatError(503, "Dịch vụ AI tạm thời gặp sự cố, vui lòng thử lại sau.")
    except anthropic.APIConnectionError:
        logger.exception("AI chat: connection error")
        raise AiChatError(503, "Không kết nối được tới dịch vụ AI, vui lòng thử lại.")

    if response.stop_reason == "refusal":
        raise AiChatError(400, "AI từ chối nội dung này — hãy quay lại chủ đề học tiếng Trung nhé.")

    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        raise AiChatError(502, "AI trả về dữ liệu không hợp lệ, vui lòng thử lại.")
