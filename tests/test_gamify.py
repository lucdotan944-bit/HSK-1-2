from datetime import date, timedelta

import gamify

UID = 42  # user bất kỳ — gamify giờ theo user_id


def _set_user_state(conn, **fields):
    conn.execute("INSERT OR IGNORE INTO user_state (user_id) VALUES (?)", (UID,))
    for key, value in fields.items():
        conn.execute(f"UPDATE user_state SET {key}=? WHERE user_id=?", (value, UID))
    conn.commit()


def test_touch_streak_first_activity_sets_streak_to_1(db_conn):
    _set_user_state(db_conn, last_active_date="")
    gamify.touch_streak(db_conn, UID)
    db_conn.commit()
    row = db_conn.execute("SELECT current_streak, longest_streak FROM user_state WHERE user_id=?", (UID,)).fetchone()
    assert row["current_streak"] == 1
    assert row["longest_streak"] == 1


def test_touch_streak_same_day_is_a_noop(db_conn):
    today = date.today().isoformat()
    _set_user_state(db_conn, last_active_date=today, current_streak=5, longest_streak=5)
    gamify.touch_streak(db_conn, UID)
    db_conn.commit()
    row = db_conn.execute("SELECT current_streak FROM user_state WHERE user_id=?", (UID,)).fetchone()
    assert row["current_streak"] == 5  # unchanged, not double-counted


def test_touch_streak_consecutive_day_increments(db_conn):
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    _set_user_state(db_conn, last_active_date=yesterday, current_streak=3, longest_streak=3)
    gamify.touch_streak(db_conn, UID)
    db_conn.commit()
    row = db_conn.execute("SELECT current_streak, longest_streak FROM user_state WHERE user_id=?", (UID,)).fetchone()
    assert row["current_streak"] == 4
    assert row["longest_streak"] == 4


def test_touch_streak_gap_day_resets_to_1(db_conn):
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()
    _set_user_state(db_conn, last_active_date=two_days_ago, current_streak=10, longest_streak=10)
    gamify.touch_streak(db_conn, UID)
    db_conn.commit()
    row = db_conn.execute("SELECT current_streak, longest_streak FROM user_state WHERE user_id=?", (UID,)).fetchone()
    assert row["current_streak"] == 1
    assert row["longest_streak"] == 10  # longest is a high-water mark, not reset


def test_award_xp_accumulates_and_logs(db_conn):
    _set_user_state(db_conn, xp=0)
    gamify.award_xp(db_conn, UID, gamify.XP_REVIEW_CORRECT, "review")
    gamify.award_xp(db_conn, UID, gamify.XP_QUIZ_CORRECT, "quiz")
    db_conn.commit()
    row = db_conn.execute("SELECT xp FROM user_state WHERE user_id=?", (UID,)).fetchone()
    assert row["xp"] == gamify.XP_REVIEW_CORRECT + gamify.XP_QUIZ_CORRECT
    log_count = db_conn.execute("SELECT COUNT(*) FROM xp_log WHERE user_id=?", (UID,)).fetchone()[0]
    assert log_count == 2


def test_xp_and_badges_are_isolated_per_user(db_conn):
    other = UID + 1
    _set_user_state(db_conn, xp=0)
    gamify.award_xp(db_conn, UID, 100, "review")
    db_conn.commit()
    row = db_conn.execute("SELECT xp FROM user_state WHERE user_id=?", (other,)).fetchone()
    assert row is None or row["xp"] == 0


def test_check_badges_awards_streak_badge_once(db_conn):
    _set_user_state(db_conn, current_streak=3, xp=0)
    first = gamify.check_badges(db_conn, UID)
    db_conn.commit()
    assert "streak_3" in first

    # Re-checking without any state change must not re-award it.
    second = gamify.check_badges(db_conn, UID)
    assert "streak_3" not in second


def test_check_badges_xp_threshold(db_conn):
    _set_user_state(db_conn, xp=500, current_streak=0)
    earned = gamify.check_badges(db_conn, UID)
    assert "xp_500" in earned
    assert "xp_2000" not in earned
