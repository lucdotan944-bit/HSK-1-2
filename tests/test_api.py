"""API smoke tests: exercise the real seeding pipeline against a throwaway
sqlite file and check the highest-traffic endpoints respond correctly."""
import pytest
from fastapi.testclient import TestClient

import database


@pytest.fixture(scope="module")
def client(tmp_path_factory):
    original_db_path = database.DB_PATH
    database.DB_PATH = str(tmp_path_factory.mktemp("api_test") / "test.db")
    import main  # imported here so `database.DB_PATH` is already patched before startup seeds it

    with TestClient(main.app) as c:
        yield c
    database.DB_PATH = original_db_path


def test_root_returns_service_info(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json()["service"] == "hsk-app-api"


def test_stats_reflects_seeded_word_count(client):
    from seed_data import get_words

    res = client.get("/api/stats")
    assert res.status_code == 200
    data = res.json()
    assert data["total"] == len(get_words())
    assert data["due"] == data["total"]  # nothing reviewed yet


def test_missing_theme_returns_404(client):
    res = client.get("/api/themes/does-not-exist")
    assert res.status_code == 404


def test_missing_dialogue_returns_404(client):
    res = client.get("/api/dialogues/does-not-exist")
    assert res.status_code == 404


def test_review_submit_schedules_next_review(client):
    words = client.get("/api/words/1").json()["words"]
    word_id = words[0]["id"]

    res = client.post("/api/review", json={"word_id": word_id, "quality": 5})
    assert res.status_code == 200
    data = res.json()
    assert data["repetitions"] == 1
    assert data["interval"] == 1


def test_review_submit_unknown_word_returns_404(client):
    res = client.post("/api/review", json={"word_id": 999_999_999, "quality": 5})
    assert res.status_code == 404


def test_exam_start_and_submit_round_trip(client):
    start = client.get("/api/exam/1/start")
    assert start.status_code == 200
    payload = start.json()
    assert payload["questions"]
    assert payload["time_limit_seconds"] > 0

    answers = [{"section": q["section"], "correct": True} for q in payload["questions"]]
    submit = client.post("/api/exam/1/submit", json={"answers": answers, "duration_seconds": 30})
    assert submit.status_code == 200
    result = submit.json()
    assert result["correct_count"] == len(answers)
    assert result["passed"] is True


def test_exam_submit_rejects_invalid_section(client):
    res = client.post(
        "/api/exam/1/submit",
        json={"answers": [{"section": "not-a-real-section", "correct": True}]},
    )
    assert res.status_code == 422


def test_pronunciation_log_rejects_invalid_score(client):
    res = client.post(
        "/api/pronunciation/log",
        json={"target_text": "你好", "score": "not-a-real-score"},
    )
    assert res.status_code == 422


def test_daily_session_blocks_match_selected_level_exactly(client):
    for level in (1, 6):
        res = client.get(f"/api/daily-session?level={level}")
        assert res.status_code == 200
        blocks = res.json()["blocks"]
        assert len(blocks["review"]) > 0
        assert all(w["hsk_level"] == level for w in blocks["review"])
        assert blocks["listening"]["hsk_level"] == level
        assert blocks["speaking"]["hsk_level"] == level
        assert blocks["conversation_hsk_level"] == level
