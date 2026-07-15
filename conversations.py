"""Hội thoại phân nhánh (scripted branching dialogue) để luyện phản xạ giao tiếp.

Thay thế "hội thoại mô phỏng với AI" bằng cây hội thoại viết sẵn — không gọi
LLM/API trả phí. Học viên chọn (hoặc nói) câu trả lời, cây tiến tới nhánh
tương ứng. Dữ liệu tĩnh, cùng dạng với bảng `dialogues` trong seed_data.py.
"""

CONVERSATIONS = {
    "order_food": {
        "title": "Gọi món ở quán ăn",
        "hsk_level": 1,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "你好！你要吃什么？", "pinyin": "nǐ hǎo! nǐ yào chī shén me?", "vi": "Chào bạn! Bạn muốn ăn gì?"},
                "choices": [
                    {"id": "a", "cn": "我要一个米饭。", "pinyin": "wǒ yào yí gè mǐfàn.", "vi": "Tôi muốn một phần cơm.", "next": "n2"},
                    {"id": "b", "cn": "我想看看菜单。", "pinyin": "wǒ xiǎng kàn kan càidān.", "vi": "Tôi muốn xem thực đơn.", "next": "n2b"},
                ],
            },
            "n2b": {
                "npc": {"cn": "好的，这是菜单。", "pinyin": "hǎo de, zhè shì càidān.", "vi": "Được, đây là thực đơn."},
                "choices": [
                    {"id": "a", "cn": "我要一个米饭。", "pinyin": "wǒ yào yí gè mǐfàn.", "vi": "Tôi muốn một phần cơm.", "next": "n2"},
                ],
            },
            "n2": {
                "npc": {"cn": "你要喝什么？", "pinyin": "nǐ yào hē shén me?", "vi": "Bạn muốn uống gì?"},
                "choices": [
                    {"id": "a", "cn": "我要喝茶。", "pinyin": "wǒ yào hē chá.", "vi": "Tôi muốn uống trà.", "next": "n3"},
                    {"id": "b", "cn": "我要喝水。", "pinyin": "wǒ yào hē shuǐ.", "vi": "Tôi muốn uống nước.", "next": "n3"},
                ],
            },
            "n3": {
                "npc": {"cn": "好，请等一下。", "pinyin": "hǎo, qǐng děng yí xià.", "vi": "Được, xin chờ một chút."},
                "choices": [
                    {"id": "a", "cn": "谢谢！", "pinyin": "xiè xie!", "vi": "Cảm ơn!", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "不客气！", "pinyin": "bú kè qi!", "vi": "Không có gì!"},
                "choices": [],
            },
        },
    },
    "ask_direction": {
        "title": "Hỏi đường",
        "hsk_level": 1,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "请问，医院在哪儿？", "pinyin": "qǐng wèn, yīyuàn zài nǎr?", "vi": "Xin hỏi, bệnh viện ở đâu?"},
                "choices": [
                    {"id": "a", "cn": "对不起，我不知道。", "pinyin": "duì bu qǐ, wǒ bù zhī dào.", "vi": "Xin lỗi, tôi không biết.", "next": "end_unknown"},
                    {"id": "b", "cn": "医院在前面。", "pinyin": "yīyuàn zài qián miàn.", "vi": "Bệnh viện ở phía trước.", "next": "n2"},
                ],
            },
            "n2": {
                "npc": {"cn": "谢谢你！很远吗？", "pinyin": "xiè xie nǐ! hěn yuǎn ma?", "vi": "Cảm ơn bạn! Có xa không?"},
                "choices": [
                    {"id": "a", "cn": "不远，走五分钟。", "pinyin": "bù yuǎn, zǒu wǔ fēn zhōng.", "vi": "Không xa, đi bộ năm phút.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "太好了，谢谢！", "pinyin": "tài hǎo le, xiè xie!", "vi": "Tuyệt quá, cảm ơn!"},
                "choices": [],
            },
            "end_unknown": {
                "npc": {"cn": "没关系，谢谢。", "pinyin": "méi guān xi, xiè xie.", "vi": "Không sao, cảm ơn."},
                "choices": [],
            },
        },
    },
    "shopping": {
        "title": "Mua sắm",
        "hsk_level": 2,
        "start": "n1",
        "nodes": {
            "n1": {
                "npc": {"cn": "欢迎光临！你想买什么？", "pinyin": "huān yíng guāng lín! nǐ xiǎng mǎi shén me?", "vi": "Chào mừng! Bạn muốn mua gì?"},
                "choices": [
                    {"id": "a", "cn": "这件衣服多少钱？", "pinyin": "zhè jiàn yī fu duō shǎo qián?", "vi": "Cái áo này bao nhiêu tiền?", "next": "n2"},
                ],
            },
            "n2": {
                "npc": {"cn": "一百块。", "pinyin": "yì bǎi kuài.", "vi": "Một trăm tệ."},
                "choices": [
                    {"id": "a", "cn": "太贵了，便宜一点吧。", "pinyin": "tài guì le, pián yi yì diǎn ba.", "vi": "Đắt quá, rẻ hơn chút đi.", "next": "n3"},
                    {"id": "b", "cn": "好，我要买。", "pinyin": "hǎo, wǒ yào mǎi.", "vi": "Được, tôi mua.", "next": "end"},
                ],
            },
            "n3": {
                "npc": {"cn": "好吧，八十块。", "pinyin": "hǎo ba, bā shí kuài.", "vi": "Được rồi, tám mươi tệ."},
                "choices": [
                    {"id": "a", "cn": "谢谢，我要买。", "pinyin": "xiè xie, wǒ yào mǎi.", "vi": "Cảm ơn, tôi mua.", "next": "end"},
                ],
            },
            "end": {
                "npc": {"cn": "谢谢惠顾！", "pinyin": "xiè xie huì gù!", "vi": "Cảm ơn đã mua hàng!"},
                "choices": [],
            },
        },
    },
}
