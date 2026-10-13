"""logic.py의 단위 변환 및 유효성 검사 로직을 검증하는 테스트 스크립트"""

from logic import convert_units

# SPEC.md 4절의 테스트 케이스 목록
TEST_CASES = [
    # (입력값, 출발단위, 도착단위, 기대결과값, 기대에러메시지)
    ("100", "cm", "m", "1", None),
    ("1", "km", "m", "1000", None),
    ("500", "mm", "cm", "50", None),
    ("0", "°C", "°F", "32", None),
    ("100", "°C", "°F", "212", None),
    ("32", "°F", "°C", "0", None),
    ("2.5", "m", "cm", "250", None),
    ("10", "m", "m", "10", None),
    ("", "cm", "m", "", "값을 입력해 주세요"),
    ("   ", "m", "km", "", "값을 입력해 주세요"),
    ("abc", "cm", "m", "", "숫자만 입력할 수 있습니다"),
    ("100", "cm", "°C", "", "길이와 온도는 서로 변환할 수 없습니다"),
    ("50", "°F", "km", "", "길이와 온도는 서로 변환할 수 없습니다"),
]


def run_tests():
    passed = 0
    failed = 0

    print("=== 단위 변환기 logic.py 테스트 시작 ===")
    for i, (val, from_u, to_u, exp_res, exp_err) in enumerate(TEST_CASES, start=1):
        actual_res, actual_err = convert_units(val, from_u, to_u)
        is_ok = (actual_res == exp_res) and (actual_err == exp_err)

        if is_ok:
            passed += 1
            print(f"[{i:02d}] 통과: {val} {from_u} -> {to_u} => 결과: '{actual_res}', 에러: '{actual_err}'")
        else:
            failed += 1
            print(f"[{i:02d}] 실패: {val} {from_u} -> {to_u}")
            print(f"     기대값: 결과='{exp_res}', 에러='{exp_err}'")
            print(f"     실제값: 결과='{actual_res}', 에러='{actual_err}'")

    print("========================================")
    if failed == 0:
        print(f"모든 테스트 통과 ({passed}개)")
    else:
        print(f"테스트 결과: 통과 {passed}개, 실패 {failed}개")

    return failed == 0


if __name__ == "__main__":
    import sys
    success = run_tests()
    sys.exit(0 if success else 1)
