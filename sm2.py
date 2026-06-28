"""SM-2 Spaced Repetition Algorithm (super-memo 2)"""
import math
from datetime import datetime

def sm2(quality: int, repetitions: int, easiness: float, interval: int):
    """
    SM-2 algorithm: tính lịch ôn tập dựa trên quality (0-5)
    
    Args:
        quality: 0=quên hoàn toàn, 3=nhớ nhưng khó, 5=hoàn hảo
        repetitions: số lần nhớ liên tiếp
        easiness: EF (easiness factor)
        interval: ngày đến lần ôn tiếp theo
    
    Returns:
        (new_repetitions, new_easiness, new_interval, next_review_date)
    """
    if quality < 3:
        # Quên → reset
        repetitions = 0
        interval = 1
    else:
        if repetitions == 0:
            interval = 1
        elif repetitions == 1:
            interval = 6
        else:
            interval = round(interval * easiness)
        repetitions += 1
    
    # Update easiness factor
    easiness = easiness + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if easiness < 1.3:
        easiness = 1.3
    
    return repetitions, easiness, interval
