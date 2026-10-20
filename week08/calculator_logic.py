import math
from datetime import datetime, timedelta

def parse_time(time_str):
    """시:분 형식을 datetime 객체로 변환"""
    if ":" in time_str:
        try:
            parts = time_str.split(":")
            if len(parts) != 2:
                raise ValueError
            h, m = parts
            time_str = f"{int(h):02d}:{int(m):02d}"
        except ValueError:
            raise ValueError("시간 형식이 올바르지 않습니다. (예: 09:30)")
    
    return datetime.strptime(time_str, "%H:%M")

def calculate_logic(arrival_time_str, departure_time_str):
    """요금 계산 핵심 로직"""
    try:
        arr = parse_time(arrival_time_str)
        dep = parse_time(departure_time_str)
    except ValueError as e:
        raise ValueError(str(e) if str(e) else "시간 형식이 잘못되었습니다. (예: 09:30)")

    # 자정을 넘기는 경우 처리
    if dep <= arr:
        dep += timedelta(days=1)

    duration = dep - arr
    duration_minutes = int(duration.total_seconds() / 60)

    # 요금 규칙: 30분 무료, 이후 10분마다 500원 (올림)
    if duration_minutes <= 30:
        fee = 0
    else:
        extra_minutes = duration_minutes - 30
        intervals = math.ceil(extra_minutes / 10)
        fee = intervals * 500

    # 하루 최대 요금 20,000원 제한
    if fee > 20000:
        fee = 20000

    # 지속 시간 포맷팅
    hours = duration_minutes // 60
    mins = duration_minutes % 60
    if hours > 0:
        duration_display = f"{hours}시간 {mins}분"
    else:
        duration_display = f"{mins}분"

    return duration_display, fee
