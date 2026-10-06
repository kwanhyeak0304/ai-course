def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        return "에러: 0으로 나눌 수 없습니다."
    return a / b


def main():
    try:
        raw1 = input("첫 번째 숫자를 입력하세요: ").strip()
        num1 = float(raw1)
        op = input("연산자(+ - * /)를 입력하세요: ").strip()
        raw2 = input("두 번째 숫자를 입력하세요: ").strip()
        num2 = float(raw2)
    except ValueError:
        print("에러: 올바른 숫자를 입력하세요.")
        return

    if op == "+":
        result = add(num1, num2)
    elif op == "-":
        result = sub(num1, num2)
    elif op == "*":
        result = mul(num1, num2)
    elif op == "/":
        result = div(num1, num2)
    else:
        print(f"에러: 지원하지 않는 연산자입니다 ({op})")
        return

    if isinstance(result, float) and result.is_integer():
        result = int(result)
    print(f"결과: {result}")


if __name__ == "__main__":
    main()
