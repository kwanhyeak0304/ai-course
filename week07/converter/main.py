# main.py
import flet as ft
from logic import ALL_UNITS, convert_units


def main(page: ft.Page):
    page.title = "단위 변환기"
    page.window.width = 360
    page.window.height = 440
    page.window.resizable = False

    # 입력 컨트롤 및 단위 드롭다운 (6개 단위 모두 포함)
    value_input = ft.TextField(label="값", value="100", width=150)
    from_unit = ft.Dropdown(
        label="단위",
        value="cm",
        width=150,
        options=[ft.dropdown.Option(u) for u in ALL_UNITS],
    )

    # 결과 컨트롤 및 대상 단위 드롭다운
    result_field = ft.TextField(label="결과", value="", width=150)
    to_unit = ft.Dropdown(
        label="단위",
        value="m",
        width=150,
        options=[ft.dropdown.Option(u) for u in ALL_UNITS],
    )

    # 에러 및 안내 문구 텍스트
    notice = ft.Text(value="", color=ft.Colors.RED)

    # 변환 기록 목록 (추가 기능)
    items = ft.ListView(expand=True, spacing=4)

    def on_delete(e):
        items.controls.pop(e.control.data)
        for i, row in enumerate(items.controls):
            row.controls[1].data = i
        page.update()

    def on_convert(e):
        notice.value = ""
        res, err = convert_units(value_input.value, from_unit.value, to_unit.value)
        if err:
            notice.value = err
            result_field.value = ""
        else:
            result_field.value = res
            record = f"{value_input.value} {from_unit.value} = {res} {to_unit.value}"
            items.controls.append(
                ft.Row(
                    controls=[
                        ft.Text(value=record, expand=True),
                        ft.Button(
                            content="삭제",
                            data=len(items.controls),
                            on_click=on_delete,
                        ),
                    ]
                )
            )
        page.update()

    def on_swap(e):
        # 출발 단위와 도착 단위 맞바꾸기
        from_val = from_unit.value
        to_val = to_unit.value
        from_unit.value = to_val
        to_unit.value = from_val
        notice.value = ""
        page.update()

    page.add(
        ft.Row(controls=[value_input, from_unit]),
        ft.Row(
            controls=[
                ft.Text(value="↓", size=20, weight=ft.FontWeight.BOLD),
                ft.Button(content="단위 맞바꾸기 ⇄", on_click=on_swap),
            ]
        ),
        ft.Row(controls=[result_field, to_unit]),
        ft.Button(
            content="변환",
            on_click=on_convert,
            expand=True,
            height=44,
            bgcolor=ft.Colors.BLUE,
            color=ft.Colors.WHITE,
        ),
        notice,
        items,
    )


if __name__ == "__main__":
    ft.run(main)
