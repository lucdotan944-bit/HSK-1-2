"""Gamification: XP, streak, huy hiệu — single-user singleton state.

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


def award_xp(conn, amount, reason):
    """Cộng XP vào user_state (singleton id=1) và ghi log."""
    conn.execute("UPDATE user_state SET xp = xp + ? WHERE id = 1", (amount,))
    conn.execute("INSERT INTO xp_log (amount, reason) VALUES (?, ?)", (amount, reason))


def touch_streak(conn):
    """Gọi mỗi khi có hoạt động học. Cập nhật streak theo ngày (strict: bỏ 1 ngày là reset)."""
    row = conn.execute(
        "SELECT last_active_date, current_streak, longest_streak FROM user_state WHERE id=1"
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
        "UPDATE user_state SET current_streak=?, longest_streak=?, last_active_date=? WHERE id=1",
        (new_streak, longest, today),
    )


def check_badges(conn):
    """Kiểm tra điều kiện huy hiệu, ghi huy hiệu mới đạt. Trả về list badge_id mới."""
    newly_earned = []
    already = {r["badge_id"] for r in conn.execute("SELECT badge_id FROM badges_earned").fetchall()}

    state = conn.execute("SELECT xp, current_streak FROM user_state WHERE id=1").fetchone()
    total_reviews = conn.execute(
        "SELECT COUNT(*) FROM quiz_results WHERE quiz_type='review'"
    ).fetchone()[0]
    mastered_words = conn.execute(
        "SELECT COUNT(*) FROM user_words WHERE repetitions >= 5"
    ).fetchone()[0]
    writing_practiced = conn.execute("SELECT COUNT(*) FROM writing_practice").fetchone()[0]

    def award_if_new(badge_id, condition):
        if badge_id not in already and condition:
            conn.execute("INSERT INTO badges_earned (badge_id) VALUES (?)", (badge_id,))
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

    return newly_earned
