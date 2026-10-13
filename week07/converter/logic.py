"""단위 변환기 계산 및 유효성 검사 로직 (Flet 미사용 순수 파이썬 모듈)"""

LENGTH_FACTORS = {
    "mm": 0.001,
    "cm": 0.01,
    "m": 1.0,
    "km": 1000.0,
}

TEMPERATURE_UNITS = {"°C", "°F"}

ALL_UNITS = ["mm", "cm", "m", "km", "°C", "°F"]


def convert_units(value_str: str, from_unit: str, to_unit: str) -> tuple[str, str | None]:
    """입력값과 출발/도착 단위를 받아 변환 결과와 에러 메시지를 반환합니다.
    
    Returns:
        tuple[str, str | None]: (변환 결과 문자열, 에러 메시지(성공 시 None))
    """
    if value_str is None or not value_str.strip():
        return ("", "값을 입력해 주세요")

    try:
        val = float(value_str.strip())
    except ValueError:
        return ("", "숫자만 입력할 수 있습니다")

    is_from_len = from_unit in LENGTH_FACTORS
    is_to_len = to_unit in LENGTH_FACTORS
    is_from_temp = from_unit in TEMPERATURE_UNITS
    is_to_temp = to_unit in TEMPERATURE_UNITS

    # 길이와 온도를 교차 변환하려는 경우
    if (is_from_len and is_to_temp) or (is_from_temp and is_to_len):
        return ("", "길이와 온도는 서로 변환할 수 없습니다")

    # 미지원 단위
    if not (is_from_len or is_from_temp) or not (is_to_len or is_to_temp):
        return ("", "지원하지 않는 단위입니다")

    if from_unit == to_unit:
        res_num = val
    elif is_from_len and is_to_len:
        # 미터 기준으로 환산 후 대상 단위로 변환
        meters = val * LENGTH_FACTORS[from_unit]
        res_num = meters / LENGTH_FACTORS[to_unit]
    elif is_from_temp and is_to_temp:
        if from_unit == "°C" and to_unit == "°F":
            res_num = val * 9.0 / 5.0 + 32.0
        elif from_unit == "°F" and to_unit == "°C":
            res_num = (val - 32.0) * 5.0 / 9.0
        else:
            res_num = val
    else:
        return ("", "길이와 온도는 서로 변환할 수 없습니다")

    res_num = round(res_num, 6)
    if res_num == int(res_num):
        res_str = str(int(res_num))
    else:
        # 불필요한 뒷자리 0 제거
        res_str = f"{res_num:.6f}".rstrip("0").rstrip(".")

    return (res_str, None)
