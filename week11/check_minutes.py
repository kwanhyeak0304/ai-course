# minutes-docx 스킬 규칙 검사. 사용법: python check_minutes.py out
import glob, os, re, sys
from docx import Document
from docx.oxml.ns import qn

for f in sorted(glob.glob(sys.argv[1] + "/**/minutes_*.docx", recursive=True)):
    d = Document(f)
    rpr = d.styles["Normal"].element.rPr
    east = rpr.rFonts.get(qn("w:eastAsia")) if rpr is not None and rpr.rFonts is not None else None
    paras = [p for p in d.paragraphs if p.text.strip()]
    styles = [p.style.name for p in paras]
    heads = [p.text for p in paras if p.style.name == "Heading 1"]
    first_col = [r.cells[0].text for r in d.tables[0].rows] if d.tables else []
    todo_head = [c.text for c in d.tables[-1].rows[0].cells] if len(d.tables) >= 2 else []
    checks = {
        "파일명": re.search(r"minutes_\d{8}\.docx$", f) is not None,
        "Title": styles[:1] == ["Title"] and paras[0].text == "회의록",
        "정보 표": first_col == ["일시", "장소", "참석자"],
        "절 순서": heads == ["안건", "논의 내용", "결정 사항", "할 일"],
        "번호 목록": "List Number" in styles,
        "할 일 표": todo_head == ["담당자", "할 일", "기한"],
        "Table Grid": bool(d.tables) and all(t.style.name == "Table Grid" for t in d.tables),
        "맑은 고딕": east == "맑은 고딕",
    }
    failed = " ".join(k for k, v in checks.items() if not v)
    print(f"{sum(checks.values())}/{len(checks)}", os.path.relpath(f, sys.argv[1]), failed)
