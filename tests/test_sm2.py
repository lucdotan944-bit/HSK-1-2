from sm2 import sm2


def test_forgetting_resets_repetitions_and_interval():
    reps, ef, interval = sm2(quality=1, repetitions=5, easiness=2.3, interval=20)
    assert reps == 0
    assert interval == 1


def test_first_two_repetitions_use_fixed_intervals():
    reps, ef, interval = sm2(quality=4, repetitions=0, easiness=2.5, interval=0)
    assert reps == 1
    assert interval == 1

    reps, ef, interval = sm2(quality=4, repetitions=1, easiness=2.5, interval=1)
    assert reps == 2
    assert interval == 6


def test_later_repetitions_scale_interval_by_easiness():
    reps, ef, interval = sm2(quality=4, repetitions=2, easiness=2.0, interval=6)
    assert reps == 3
    assert interval == round(6 * 2.0)


def test_easiness_has_a_floor_of_1_3():
    ef = 1.3
    for _ in range(10):
        _, ef, _ = sm2(quality=0, repetitions=0, easiness=ef, interval=1)
    assert ef == 1.3


def test_perfect_quality_increases_easiness():
    _, ef, _ = sm2(quality=5, repetitions=2, easiness=2.5, interval=6)
    assert ef > 2.5


def test_quality_boundary_3_still_counts_as_remembered():
    """quality=3 is the pass/fail cutoff used by submit_review (main.py)."""
    reps, _, interval = sm2(quality=3, repetitions=0, easiness=2.5, interval=0)
    assert reps == 1
    assert interval == 1
