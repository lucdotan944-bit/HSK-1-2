"""Auth + multi-user isolation: đăng ký/đăng nhập, khách tự tạo, tiến độ tách riêng."""
import pytest
from fastapi.testclient import TestClient

import database


@pytest.fixture()
def make_client(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_PATH", str(tmp_path / "test.db"))
    import main

    clients = []

    def _make():
        c = TestClient(main.app)
        c.__enter__()
        clients.append(c)
        return c

    yield _make
    for c in clients:
        c.__exit__(None, None, None)


def _word_id(client):
    return client.get("/api/words/1").json()["words"][0]["id"]


def test_guest_created_on_first_write(make_client):
    c = make_client()
    assert "hn_session" not in c.cookies
    res = c.post("/api/review", json={"word_id": _word_id(c), "quality": 5})
    assert res.status_code == 200
    assert c.cookies.get("hn_session")


def test_two_browsers_have_isolated_progress(make_client):
    a, b = make_client(), make_client()
    wid = _word_id(a)
    a.post("/api/review", json={"word_id": wid, "quality": 5})

    xp_a = a.get("/api/gamify/state").json()["xp"]
    xp_b = b.get("/api/gamify/state").json()["xp"]
    assert xp_a > 0
    assert xp_b == 0  # người dùng B không thấy tiến độ của A

    # Từ vừa ôn không còn đến hạn với A, nhưng vẫn "chưa học" với B
    due_a = {w["id"] for w in a.get("/api/review/1?limit=200").json()["words"]}
    due_b = {w["id"] for w in b.get("/api/review/1?limit=200").json()["words"]}
    assert wid not in due_a
    assert wid in due_b


def test_register_keeps_guest_progress(make_client):
    c = make_client()
    c.post("/api/review", json={"word_id": _word_id(c), "quality": 5})
    xp_before = c.get("/api/gamify/state").json()["xp"]
    assert xp_before > 0

    res = c.post("/api/auth/register", json={
        "email": "luc@example.com", "password": "matkhau123", "display_name": "Luc",
    })
    assert res.status_code == 200
    assert res.json()["kept_progress"] is True
    assert c.get("/api/gamify/state").json()["xp"] == xp_before
    me = c.get("/api/auth/me").json()
    assert me["authenticated"] is True
    assert me["email"] == "luc@example.com"


def test_register_rejects_duplicate_email_and_short_password(make_client):
    c = make_client()
    ok = c.post("/api/auth/register", json={"email": "a@b.com", "password": "12345678"})
    assert ok.status_code == 200
    dup = c.post("/api/auth/register", json={"email": "a@b.com", "password": "12345678"})
    assert dup.status_code == 409
    short = c.post("/api/auth/register", json={"email": "x@y.com", "password": "123"})
    assert short.status_code == 400


def test_login_from_other_browser_restores_account(make_client):
    a = make_client()
    a.post("/api/review", json={"word_id": _word_id(a), "quality": 5})
    a.post("/api/auth/register", json={"email": "sync@example.com", "password": "matkhau123"})
    xp = a.get("/api/gamify/state").json()["xp"]

    b = make_client()  # "thiết bị" thứ hai
    bad = b.post("/api/auth/login", json={"email": "sync@example.com", "password": "saimatkhau"})
    assert bad.status_code == 401
    good = b.post("/api/auth/login", json={"email": "sync@example.com", "password": "matkhau123"})
    assert good.status_code == 200
    assert b.get("/api/gamify/state").json()["xp"] == xp


def test_logout_clears_session(make_client):
    c = make_client()
    c.post("/api/auth/register", json={"email": "out@example.com", "password": "matkhau123"})
    assert c.get("/api/auth/me").json()["authenticated"] is True
    c.post("/api/auth/logout")
    assert c.get("/api/auth/me").json()["authenticated"] is False
