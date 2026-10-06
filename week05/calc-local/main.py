"""Flet 1.0 기반 사칙연산 계산기 UI."""

import flet as ft
from calc import Calculator


def main(page: ft.Page):
    page.title = "계산기"
    page.window.width = 340
    page.window.height = 520
    page.window.resizable = False

    calculator = Calculator()

    display = ft.Text(
        value=calculator.display,
        size=40,
        text_align=ft.TextAlign.RIGHT,
    )

    def update_display():
        display.value = calculator.display
        page.update()

    def on_button_click(e):
        key = e.control.data
        calculator.press(key)
        update_display()

    def on_keyboard_event(e: ft.KeyboardEvent):
        key = e.key
        if key in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ".", "+", "-", "*", "/"):
            calculator.press(key)
        elif key in ("Enter", "NumpadEnter"):
            calculator.press("=")
        elif key == "Backspace":
            calculator.press("BS")
        elif key == "Escape":
            calculator.press("C")
        update_display()

    page.on_keyboard_event = on_keyboard_event

    def make_button(label: str, key: str, bgcolor):
        return ft.Button(
            content=label,
            data=key,
            on_click=on_button_click,
            expand=1,
            height=60,
            bgcolor=bgcolor,
            color=ft.Colors.WHITE,
        )

    # 5줄 x 4칸 버튼 레이아웃
    # C, +/-, %, ÷
    row1 = ft.Row(
        controls=[
            make_button("C", "C", ft.Colors.GREY_600),
            make_button("+/-", "+/-", ft.Colors.GREY_600),
            make_button("%", "%", ft.Colors.GREY_600),
            make_button("÷", "/", ft.Colors.ORANGE),
        ]
    )

    # 7, 8, 9, ×
    row2 = ft.Row(
        controls=[
            make_button("7", "7", ft.Colors.GREY_800),
            make_button("8", "8", ft.Colors.GREY_800),
            make_button("9", "9", ft.Colors.GREY_800),
            make_button("×", "*", ft.Colors.ORANGE),
        ]
    )

    # 4, 5, 6, −
    row3 = ft.Row(
        controls=[
            make_button("4", "4", ft.Colors.GREY_800),
            make_button("5", "5", ft.Colors.GREY_800),
            make_button("6", "6", ft.Colors.GREY_800),
            make_button("−", "-", ft.Colors.ORANGE),
        ]
    )

    # 1, 2, 3, +
    row4 = ft.Row(
        controls=[
            make_button("1", "1", ft.Colors.GREY_800),
            make_button("2", "2", ft.Colors.GREY_800),
            make_button("3", "3", ft.Colors.GREY_800),
            make_button("+", "+", ft.Colors.ORANGE),
        ]
    )

    # 0, ., ⌫, =
    row5 = ft.Row(
        controls=[
            make_button("0", "0", ft.Colors.GREY_800),
            make_button(".", ".", ft.Colors.GREY_800),
            make_button("⌫", "BS", ft.Colors.GREY_800),
            make_button("=", "=", ft.Colors.ORANGE),
        ]
    )

    page.add(
        ft.Container(
            content=display,
            alignment=ft.Alignment.CENTER_RIGHT,
            padding=10,
            height=90,
        ),
        row1,
        row2,
        row3,
        row4,
        row5,
    )


if __name__ == "__main__":
    ft.run(main)
