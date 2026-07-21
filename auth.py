"""Tài khoản & phiên đăng nhập.

Thiết kế:
- Mỗi trình duyệt nhận một session cookie (httpOnly). Request GHI (POST) đầu
  tiên chưa có session sẽ tự tạo "người dùng khách" (users.is_guest=1) — tiến
  độ tách riêng ngay từ lúc chưa đăng ký.
- Request ĐỌC (GET) không có session KHÔNG tạo user (tránh SSR/crawler tạo
  rác) — trả None, endpoint trả về trạng thái "chưa có tiến độ".
- Đăng ký email nâng cấp tại chỗ user khách hiện tại (giữ nguyên toàn bộ
  XP/SRS đã có). Đăng nhập chuyển session sang tài khoản đã tồn tại.
- Mật khẩu băm bằng hashlib.scrypt (stdlib, không thêm dependency).
- Google OAuth sẵn code, chỉ hoạt động khi đặt env GOOGLE_CLIENT_ID +
  GOOGLE_CLIENT_SECRET + APP_ORIGIN (redirect URI phải đăng ký trong Google
  Cloud Console: {APP_ORIGIN}/api/auth/google/callback).
"""
import hashlib
import hmac
import os
import re
import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Request, Response

SESSION_COOKIE = "hn_session"
SESSION_MAX_AGE_DAYS = 180
# Secure cookie ở môi trường https (Render đặt sẵn env RENDER); dev http tắt.
COOKIE_SECURE = bool(os.environ.get("RENDER") or os.environ.get("COOKIE_SECURE"))

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "")
# Origin công khai của frontend (vd https://hsk-1-2.vercel.app) — dùng dựng
# redirect_uri cho Google OAuth (đi qua rewrite /api/* của Next).
APP_ORIGIN = os.environ.get("APP_ORIGIN", "").rstrip("/")

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# PBKDF2-HMAC-SHA256: luôn có trong stdlib mọi build (scrypt phụ thuộc bản
# OpenSSL). 600k vòng theo khuyến nghị OWASP 2023 cho PBKDF2-SHA256.
_PBKDF2_ITERATIONS = 600_000


def google_enabled() -> bool:
    return bool(GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET and APP_ORIGIN)


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _PBKDF2_ITERATIONS)
    return f"pbkdf2${_PBKDF2_ITERATIONS}${salt.hex()}${h.hex()}"


def verify_password(password: str, stored: str) -> bool:
    try:
        algo, iterations, salt_hex, hash_hex = stored.split("$")
        if algo != "pbkdf2":
            return False
        h = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt_hex), int(iterations)
        )
        return hmac.compare_digest(h.hex(), hash_hex)
    except (ValueError, AttributeError):
        return False


def _expiry() -> str:
    return (datetime.utcnow() + timedelta(days=SESSION_MAX_AGE_DAYS)).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def create_session(conn, user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    conn.execute(
        "INSERT INTO sessions (token, user_id, expires_at) VALUES (?, ?, ?)",
        (token, user_id, _expiry()),
    )
    return token


def set_session_cookie(response: Response, token: str):
    response.set_cookie(
        SESSION_COOKIE, token,
        max_age=SESSION_MAX_AGE_DAYS * 86400,
        httponly=True, samesite="lax", secure=COOKIE_SECURE, path="/",
    )


def clear_session_cookie(response: Response):
    response.delete_cookie(SESSION_COOKIE, path="/")


def session_user_id(conn, request: Request) -> Optional[int]:
    """user_id của session hợp lệ trong cookie, hoặc None."""
    token = request.cookies.get(SESSION_COOKIE)
    if not token:
        return None
    row = conn.execute(
        "SELECT user_id, expires_at FROM sessions WHERE token = ?", (token,)
    ).fetchone()
    if not row:
        return None
    if row["expires_at"] < datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"):
        conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        conn.commit()
        return None
    return row["user_id"]


def create_guest(conn) -> int:
    cur = conn.execute(
        "INSERT INTO users (is_guest, display_name) VALUES (1, '')"
    )
    return cur.lastrowid


def ensure_user_state(conn, user_id: int):
    conn.execute(
        "INSERT OR IGNORE INTO user_state (user_id) VALUES (?)", (user_id,)
    )


# ---- FastAPI dependencies ----
# Import get_db tại chỗ để tránh vòng import (database -> auth không tồn tại,
# nhưng giữ auth.py không phụ thuộc lúc import giúp test dễ hơn).

def current_user_id(request: Request, response: Response) -> int:
    """Cho endpoint GHI: luôn trả về một user_id — tạo khách nếu chưa có."""
    from database import get_db
    conn = get_db()
    uid = session_user_id(conn, request)
    if uid is None:
        uid = create_guest(conn)
        ensure_user_state(conn, uid)
        token = create_session(conn, uid)
        conn.commit()
        set_session_cookie(response, token)
    conn.close()
    return uid


def optional_user_id(request: Request) -> Optional[int]:
    """Cho endpoint ĐỌC: user_id nếu có session, None nếu chưa (không tạo khách)."""
    from database import get_db
    conn = get_db()
    uid = session_user_id(conn, request)
    conn.close()
    return uid
