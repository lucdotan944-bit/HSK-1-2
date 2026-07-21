"""AI chat endpoint tests: demo mode (no API key), status, and the daily cap."""
import pytest
from fastapi.testclient import TestClient

import database


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    original_db_path = database.DB_PATH
    database.DB_PATH = str(tmp_path_factory.mktemp("ai_chat_test") / "test.db")
    import main

    with TestClient(main.app) as c:
        yield c
    database.DB_PATH = original_db_path


def test_status_reports_demo_mode_without_key(client, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    res = client.get("/api/ai-chat/status")
    assert res.status_code == 200
    body = res.json()
    assert body["enabled"] is False
    assert body["limit"] > 0
    assert body["remaining_today"] == body["limit"]


def test_demo_respond_returns_structured_reply(client, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    res = client.post(
        "/api/ai-chat/respond",
        json={"messages": [{"role": "user", "content": "你好"}], "hsk_level": 1, "topic_id": "greetings"},
    )
    assert res.status_code == 200
    body = res.json()
    assert body["demo"] is True
    for field in ("reply_cn", "reply_pinyin", "reply_vi", "suggestions"):
        assert field in body
    assert len(body["suggestions"]) >= 1
    assert {"cn", "pinyin", "vi"} <= set(body["suggestions"][0])


def test_demo_advances_through_turns(client, monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    first = client.post("/api/ai-chat/respond", json={"messages": [{"role": "user", "content": "你好"}]}).json()
    second = client.post(
        "/api/ai-chat/respond",
        json={"messages": [
            {"role": "user", "content": "你好"},
            {"role": "assistant", "content": first["reply_cn"]},
            {"role": "user", "content": "我叫小明"},
        ]},
    ).json()
    assert second["reply_cn"] != first["reply_cn"]


def test_real_mode_daily_cap_returns_429(client, monkeypatch):
    import ai_chat
    from datetime import date

    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test-not-a-real-key")
    # Quota giờ tính theo user — lấy user của session cookie hiện tại (được
    # tạo tự động ở các request POST trước đó trong module này).
    token = client.cookies.get("hn_session")
    assert token, "expected earlier POSTs to have created a guest session"
    conn = database.get_db()
    user_id = conn.execute(
        "SELECT user_id FROM sessions WHERE token=?", (token,)
    ).fetchone()["user_id"]
    conn.execute(
        "INSERT INTO ai_chat_usage (user_id, day, count) VALUES (?, ?, ?) "
        "ON CONFLICT(user_id, day) DO UPDATE SET count = excluded.count",
        (user_id, date.today().isoformat(), ai_chat.DAILY_LIMIT),
    )
    conn.commit()
    conn.close()

    res = client.post("/api/ai-chat/respond", json={"messages": [{"role": "user", "content": "你好"}]})
    assert res.status_code == 429
    assert "lượt" in res.json()["error"]

    status = client.get("/api/ai-chat/status").json()
    assert status["enabled"] is True
    assert status["remaining_today"] == 0
