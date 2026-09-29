"""단위 변환기 콘솔 프로그램."""

# 변환 계수 표 (기준 단위: 길이-m, 무게-kg, 부피-L)
CONVERSION_FACTORS = {
    "길이": {
        "m": 1.0,
        "cm": 0.01,
        "mm": 0.001,
        "km": 1000.0,
        "inch": 0.0254,
        "ft": 0.3048,
    },
    "무게": {
        "kg": 1.0,
        "g": 0.001,
        "mg": 0.000001,
        "lb": 0.453592,
        "oz": 0.0283495,
    },
    "부피": {
        "L": 1.0,
        "mL": 0.001,
        "gal": 3.78541,
    },
}


def convert_length(value: float, from_unit: str, to_unit: str) -> float:
    """길이 단위를 다른 단위로 변환한다."""
    factors = CONVERSION_FACTORS["길이"]
    base_m = value * factors[from_unit]
    return base_m / factors[to_unit]


def convert_weight(value: float, from_unit: str, to_unit: str) -> float:
    """무게 단위를 다른 단위로 변환한다."""
    factors = CONVERSION_FACTORS["무게"]
    base_kg = value * factors[from_unit]
    return base_kg / factors[to_unit]


def convert_volume(value: float, from_unit: str, to_unit: str) -> float:
    """부피 단위를 다른 단위로 변환한다."""
    factors = CONVERSION_FACTORS["부피"]
    base_l = value * factors[from_unit]
    return base_l / factors[to_unit]


def convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """온도(섭씨, 화씨, 켈빈) 단위를 변환한다."""
    # 기준 단위는 섭씨(C)
    if from_unit == "C":
        celsius = value
    elif from_unit == "F":
        celsius = (value - 32) * 5 / 9
    elif from_unit == "K":
        celsius = value - 273.15
    else:
        raise ValueError(f"지원하지 않는 온도 단위입니다: {from_unit}")

    if to_unit == "C":
        return celsius
    elif to_unit == "F":
        return celsius * 9 / 5 + 32
    elif to_unit == "K":
        return celsius + 273.15
    else:
        raise ValueError(f"지원하지 않는 온도 단위입니다: {to_unit}")


def get_float_input(prompt: str) -> float:
    """사용자로부터 유효한 실수를 입력받을 때까지 다시 묻는다."""
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("잘못된 입력입니다. 올바른 숫자를 다시 입력해 주세요.")


def main():
    """콘솔 단위 변환기 메인 루프를 실행한다."""
    categories = {"1": "길이", "2": "무게", "3": "온도", "4": "부피"}

    print("=== 단위 변환기 프로그램 ===")
    while True:
        print("\n변환할 항목을 선택하세요:")
        for key, name in categories.items():
            print(f"[{key}] {name}")
        print("[q] 종료")

        choice = input("선택: ").strip().lower()
        if choice == "q":
            print("프로그램을 종료합니다.")
            break

        if choice not in categories:
            print("잘못된 선택입니다. 다시 선택해 주세요.")
            continue

        cat = categories[choice]
        if cat in CONVERSION_FACTORS:
            available_units = list(CONVERSION_FACTORS[cat].keys())
        else:
            available_units = ["C", "F", "K"]

        print(f"\n지원하는 단위: {', '.join(available_units)}")

        # 변환 전 단위 입력
        while True:
            from_unit = input("변환 전 단위: ").strip()
            if from_unit in available_units:
                break
            print(f"지원하지 않는 단위입니다. {available_units} 중에서 입력해 주세요.")

        # 변환 후 단위 입력
        while True:
            to_unit = input("변환 후 단위: ").strip()
            if to_unit in available_units:
                break
            print(f"지원하지 않는 단위입니다. {available_units} 중에서 입력해 주세요.")

        # 값 입력
        val = get_float_input("변환할 값: ")

        # 변환 실행
        if cat == "길이":
            res = convert_length(val, from_unit, to_unit)
        elif cat == "무게":
            res = convert_weight(val, from_unit, to_unit)
        elif cat == "부피":
            res = convert_volume(val, from_unit, to_unit)
        else:
            res = convert_temperature(val, from_unit, to_unit)

        print(f"\n=> 결과: {val} {from_unit} = {res:.4f} {to_unit}")


if __name__ == "__main__":
    main()
