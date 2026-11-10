---
name: minutes-docx
description: 회의, 미팅, 스터디 모임의 내용을 회의록 워드(docx) 파일로 만들 때 쓴다. 일시, 참석자, 안건, 결정 사항, 할 일이 들어간다. 보고서나 엑셀, PDF에는 쓰지 않는다.
---

# 회의록 docx 만들기

## 규칙

- 파일 이름은 `minutes_YYYYMMDD.docx`이고 날짜는 회의 날짜다. 오늘 날짜가 아니다.
- 문서 맨 위에 "회의록"을 'Title' 스타일로 넣는다.
- 제목 아래에 회의 정보 표(2열, 'Table Grid')를 둔다. 행은 일시, 장소, 참석자 순서다.
- 절 제목은 'Heading 1' 스타일을 쓰고 순서는 안건, 논의 내용, 결정 사항, 할 일이다.
- 안건, 논의 내용, 결정 사항은 'List Number' 스타일 문단으로 한 항목씩 쓴다. 번호 문자를 직접 쓰지 않는다.
- 할 일은 표('Table Grid')로 쓴다. 머리글은 담당자, 할 일, 기한이다.
- 본문 글꼴은 맑은 고딕 11pt다. 한글 글꼴은 `w:eastAsia`를 따로 지정해야 바뀐다.
- 받은 내용을 그대로 쓴다. 없는 결정이나 할 일을 지어내지 않는다. 받은 내용에 없는 칸은 "-"로 둔다.

## 코드

python-docx를 쓴다. 아래는 함수 없이 위에서 아래로 그대로 실행되는 완성본이다. 대문자 변수 값만 받은 내용으로 바꾸고 나머지 줄은 그대로 둔다.

```python
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn

DATE = "2026-11-10"
PLACE = "-"
PEOPLE = "-"
AGENDA = ["안건1"]
DISCUSS = ["논의1"]
DECIDE = ["결정1"]
TODO = [("담당자", "할 일", "기한")]

doc = Document()
style = doc.styles["Normal"]
style.font.name = "맑은 고딕"
style.font.size = Pt(11)
style.element.rPr.rFonts.set(qn("w:eastAsia"), "맑은 고딕")

doc.add_paragraph("회의록", style="Title")
info = doc.add_table(rows=0, cols=2)
info.style = "Table Grid"
for k, v in [("일시", DATE), ("장소", PLACE), ("참석자", PEOPLE)]:
    cells = info.add_row().cells
    cells[0].text = k
    cells[1].text = v

for head, items in [("안건", AGENDA), ("논의 내용", DISCUSS), ("결정 사항", DECIDE)]:
    doc.add_paragraph(head, style="Heading 1")
    for it in items:
        doc.add_paragraph(it, style="List Number")

doc.add_paragraph("할 일", style="Heading 1")
t = doc.add_table(rows=1, cols=3)
t.style = "Table Grid"
for i, h in enumerate(["담당자", "할 일", "기한"]):
    t.rows[0].cells[i].text = h
for row in TODO:
    cells = t.add_row().cells
    for i, v in enumerate(row):
        cells[i].text = v

name = "minutes_" + DATE.replace("-", "") + ".docx"
doc.save(name)
print("saved", name)
```

## 확인

저장한 뒤 `python check_minutes.py 폴더`로 규칙을 지켰는지 검사한다.
