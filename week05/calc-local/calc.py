"""사칙연산 계산기 로직 (Calculator 클래스)."""


class Calculator:
    def __init__(self):
        self.display = "0"
        self._accumulator = None
        self._pending_op = None
        self._is_new_number = True
        self._just_evaluated = False
        self._error = False

    def press(self, key: str) -> None:
        if self._error:
            if key == "C":
                self._reset()
            return

        if key == "C":
            self._reset()
            return

        if key in "0123456789":
            self._handle_digit(key)
        elif key == ".":
            self._handle_dot()
        elif key == "+/-":
            self._handle_sign()
        elif key == "%":
            self._handle_percent()
        elif key == "BS":
            self._handle_backspace()
        elif key in ("+", "-", "*", "/"):
            self._handle_operator(key)
        elif key == "=":
            self._handle_equals()

    def _reset(self) -> None:
        self.display = "0"
        self._accumulator = None
        self._pending_op = None
        self._is_new_number = True
        self._just_evaluated = False
        self._error = False

    def _format_number(self, val: float) -> str:
        val = round(val, 10)
        if val == int(val):
            return str(int(val))
        s = f"{val:.10f}".rstrip("0").rstrip(".")
        if s == "-0":
            s = "0"
        return s

    def _count_digits(self, s: str) -> int:
        return sum(1 for c in s if c.isdigit())

    def _handle_digit(self, digit: str) -> None:
        if self._just_evaluated:
            self._accumulator = None
            self._pending_op = None
            self._just_evaluated = False
            self.display = digit
            self._is_new_number = False
            return

        if self._is_new_number:
            self.display = digit
            self._is_new_number = False
            return

        # 12자리 제한 (소수점, 부호 제외)
        if self._count_digits(self.display) >= 12:
            return

        if self.display == "0":
            self.display = digit
        elif self.display == "-0":
            self.display = "-" + digit
        else:
            self.display += digit

    def _handle_dot(self) -> None:
        if self._just_evaluated or self._is_new_number:
            self.display = "0."
            self._is_new_number = False
            self._just_evaluated = False
            return

        if "." not in self.display:
            if self._count_digits(self.display) < 12:
                self.display += "."

    def _handle_sign(self) -> None:
        if self.display == "0":
            return
        if self.display.startswith("-"):
            self.display = self.display[1:]
        else:
            self.display = "-" + self.display

    def _handle_percent(self) -> None:
        try:
            curr = float(self.display)
        except ValueError:
            return
        val = curr / 100.0
        self.display = self._format_number(val)
        self._is_new_number = True

    def _handle_backspace(self) -> None:
        if self._just_evaluated:
            return

        if self._is_new_number:
            return

        if len(self.display) <= 1 or (len(self.display) == 2 and self.display.startswith("-")):
            self.display = "0"
            self._is_new_number = True
        else:
            self.display = self.display[:-1]
            if self.display in ("", "-"):
                self.display = "0"
                self._is_new_number = True

    def _execute_op(self, op: str, a: float, b: float):
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            return a * b
        elif op == "/":
            if b == 0:
                return None
            return a / b
        return b

    def _handle_operator(self, op: str) -> None:
        if self._just_evaluated:
            self._accumulator = float(self.display)
            self._pending_op = op
            self._is_new_number = True
            self._just_evaluated = False
            return

        if self._pending_op is not None and self._is_new_number:
            # 연산자 연속 입력 시 교체
            self._pending_op = op
            return

        curr = float(self.display)
        if self._accumulator is not None and self._pending_op is not None:
            res = self._execute_op(self._pending_op, self._accumulator, curr)
            if res is None:
                self.display = "0으로 나눌 수 없습니다"
                self._error = True
                return
            self.display = self._format_number(res)
            self._accumulator = float(self.display)
        else:
            self._accumulator = curr

        self._pending_op = op
        self._is_new_number = True
        self._just_evaluated = False

    def _handle_equals(self) -> None:
        if self._just_evaluated:
            return

        if self._pending_op is not None and self._accumulator is not None:
            curr = float(self.display)
            res = self._execute_op(self._pending_op, self._accumulator, curr)
            if res is None:
                self.display = "0으로 나눌 수 없습니다"
                self._error = True
                return
            self.display = self._format_number(res)
            self._accumulator = None
            self._pending_op = None

        self._just_evaluated = True
        self._is_new_number = True
