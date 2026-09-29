"""calc.py 검증 테스트 스위트."""

import sys
from calc import Calculator

TEST_CASES = [
    ("", "0"),
    ("1 2 + 3 =", "15"),
    ("2 + 3 * 4 =", "20"),
    ("5 + - 3 =", "2"),
    ("0 . 1 + 0 . 2 =", "0.3"),
    ("6 / 3 =", "2"),
    ("7 / 2 =", "3.5"),
    ("5 / 0 =", "0으로 나눌 수 없습니다"),
    ("5 / 0 = 7", "0으로 나눌 수 없습니다"),
    ("5 / 0 = C", "0"),
    ("1 . . 5", "1.5"),
    (".", "0."),
    ("0 0 7", "7"),
    ("1 2 3 BS", "12"),
    ("5 BS", "0"),
    ("9 +/-", "-9"),
    ("5 0 %", "0.5"),
    ("2 + 3 = 4", "4"),
    ("2 + 3 = + 4 =", "9"),
    ("2 + 3 = =", "5"),
]


def run_tests():
    passed = 0
    total = len(TEST_CASES)

    for expr, expected in TEST_CASES:
        calc = Calculator()
        if expr:
            keys = expr.split()
            for k in keys:
                calc.press(k)

        actual = calc.display
        if actual == expected:
            passed += 1
        else:
            print(f"테스트 실패: 입력 [{expr}] -> 기대값 '{expected}', 실제값 '{actual}'")
            sys.exit(1)

    print(f"모든 테스트 통과 ({passed}개)")


if __name__ == "__main__":
    run_tests()
