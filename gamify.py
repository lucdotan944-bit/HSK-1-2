"""Gamification: XP, streak, huy hiệu — theo từng người dùng (user_id).

Các hàm nhận conn đang mở và KHÔNG tự commit — caller chịu trách nhiệm commit
để có thể gộp chung transaction với ghi dữ liệu của endpoint.
"""
from datetime import date

# XP cho từng hành động
XP_LESSON_WORD = 2
XP_REVIEW_CORRECT = 5
XP_REVIEW_WRONG = 1
XP_QUIZ_CORRECT = 10
XP_THEME_QUIZ_COMPLETE = 25
XP_WRITING_ATTEMPT = 15
XP_WRITING_PERFECT = 30
XP_PLACEMENT_TEST = 50
XP_AI_CHAT_TURN = 3


def ensure_state(conn, user_id):
    """Bảo đảm user có dòng user_state (user mới tạo giữa chừng, DB cũ...)."""
    conn.execute("INSERT OR IGNORE INTO user_state (user_id) VALUES (?)", (user_id,))


def award_xp(conn, user_id, amount, reason):
    """Cộng XP vào user_state của user và ghi log."""
    ensure_state(conn, user_id)
    conn.execute("UPDATE user_state SET xp = xp + ? WHERE user_id = ?", (amount, user_id))
    conn.execute(
        "INSERT INTO xp_log (user_id, amount, reason) VALUES (?, ?, ?)",
        (user_id, amount, reason),
    )


def touch_streak(conn, user_id):
    """Gọi mỗi khi có hoạt động học. Cập nhật streak theo ngày (strict: bỏ 1 ngày là reset)."""
    ensure_state(conn, user_id)
    row = conn.execute(
        "SELECT last_active_date, current_streak, longest_streak FROM user_state WHERE user_id=?",
        (user_id,),
    ).fetchone()
    today = date.today().isoformat()
    last = row["last_active_date"]
    if last == today:
        return  # hôm nay đã tính rồi
    if last == "":
        new_streak = 1
    else:
        gap_days = (date.today() - date.fromisoformat(last)).days
        new_streak = row["current_streak"] + 1 if gap_days == 1 else 1
    longest = max(row["longest_streak"], new_streak)
    conn.execute(
        "UPDATE user_state SET current_streak=?, longest_streak=?, last_active_date=? WHERE user_id=?",
        (new_streak, longest, today, user_id),
    )


def check_badges(conn, user_id):
    """Kiểm tra điều kiện huy hiệu, ghi huy hiệu mới đạt. Trả về list badge_id mới."""
    ensure_state(conn, user_id)
    newly_earned = []
    already = {
        r["badge_id"]
        for r in conn.execute(
            "SELECT badge_id FROM badges_earned WHERE user_id=?", (user_id,)
        ).fetchall()
    }

    state = conn.execute(
        "SELECT xp, current_streak FROM user_state WHERE user_id=?", (user_id,)
    ).fetchone()
    total_reviews = conn.execute(
        "SELECT COUNT(*) FROM quiz_results WHERE quiz_type='review' AND user_id=?",
        (user_id,),
    ).fetchone()[0]
    mastered_words = conn.execute(
        "SELECT COUNT(*) FROM user_words WHERE repetitions >= 5 AND user_id=?",
        (user_id,),
    ).fetchone()[0]
    writing_practiced = conn.execute(
        "SELECT COUNT(*) FROM writing_practice WHERE user_id=?", (user_id,)
    ).fetchone()[0]
    exam_passed_levels = {
        r["hsk_level"]
        for r in conn.execute(
            "SELECT DISTINCT hsk_level FROM exam_sessions WHERE passed=1 AND user_id=?",
            (user_id,),
        ).fetchall()
    }

    def award_if_new(badge_id, condition):
        if badge_id not in already and condition:
            conn.execute(
                "INSERT INTO badges_earned (user_id, badge_id) VALUES (?, ?)",
                (user_id, badge_id),
            )
            newly_earned.append(badge_id)

    award_if_new("streak_3", state["current_streak"] >= 3)
    award_if_new("streak_7", state["current_streak"] >= 7)
    award_if_new("streak_30", state["current_streak"] >= 30)
    award_if_new("words_50", mastered_words >= 50)
    award_if_new("words_150", mastered_words >= 150)
    award_if_new("reviews_100", total_reviews >= 100)
    award_if_new("writer_10", writing_practiced >= 10)
    award_if_new("writer_50", writing_practiced >= 50)
    award_if_new("xp_500", state["xp"] >= 500)
    award_if_new("xp_2000", state["xp"] >= 2000)
    award_if_new("exam_first_pass", len(exam_passed_levels) >= 1)
    award_if_new("exam_tier_so_cap", any(l in (1, 2, 3) for l in exam_passed_levels))
    award_if_new("exam_tier_trung_cap", any(l in (4, 5, 6) for l in exam_passed_levels))
    award_if_new("exam_tier_cao_cap", any(l in (7, 8, 9) for l in exam_passed_levels))

    return newly_earned
