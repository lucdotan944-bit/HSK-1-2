"""Bảng quy đổi tương đối giữa chuẩn HSK cũ (1-6) và HSK 3.0 (1-9 cấp).

Đây là bảng quy đổi tham khảo dựa trên các so sánh phổ biến giữa hai chuẩn
(không phải bảng chính thức của Bộ Giáo dục Trung Quốc), dùng để hiển thị
song song hai hệ thống cho học viên, không dùng để tính điểm.
"""

HSK_MAPPING = [
    {"old": 1, "new_range": [1, 2], "desc": "HSK 1 cũ ≈ Cấp 1-2 (HSK 3.0)"},
    {"old": 2, "new_range": [2, 3], "desc": "HSK 2 cũ ≈ Cấp 2-3 (HSK 3.0)"},
    {"old": 3, "new_range": [3, 4], "desc": "HSK 3 cũ ≈ Cấp 3-4 (HSK 3.0)"},
    {"old": 4, "new_range": [4, 5], "desc": "HSK 4 cũ ≈ Cấp 4-5 (HSK 3.0)"},
    {"old": 5, "new_range": [5, 6], "desc": "HSK 5 cũ ≈ Cấp 5-6 (HSK 3.0)"},
    {"old": 6, "new_range": [6, 9], "desc": "HSK 6 cũ ≈ Cấp 6-9 (HSK 3.0)"},
]


def map_old_to_new(old_level: int):
    for row in HSK_MAPPING:
        if row["old"] == old_level:
            return row
    return None
