import base64, json, re
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None


RECEIPT_PROMPT = """이 사진은 영수증이다. 구매한 항목의 이름과 금액(원)을 읽어라.
다른 설명 없이 아래 형식의 JSON으로만 답하라. 금액은 쉼표 없는 정수로 적는다.
합계, 부가세, 받은 돈, 거스름돈 줄은 항목에 넣지 않는다.
영수증이 아니거나 글자를 읽을 수 없으면 {"items": []} 로 답하라.
{"items": [{"name": "항목 이름", "price": 12000}]}"""


def to_int(value):
    """'17,000' 이나 '17000원' 같은 값을 정수로 바꾼다. 못 바꾸면 None."""
    if value is None:
        return None
    digits = re.sub(r"[^\d]", "", str(value))
    return int(digits) if digits else None


def split_amount(total, people):
    """1인당 금액과 남는 금액을 계산한다."""
    base = total // people
    remainder = total % people
    return {
        "total": total,
        "people": people,
        "base": base,          # 모두가 내는 기본 금액
        "remainder": remainder,  # 나누어떨어지지 않고 남는 금액
        "ceil": base + (1 if remainder else 0),  # 올림해서 내면 1인당 금액
        "extra": (base + 1) * people - total if remainder else 0,  # 올림했을 때 더 걷히는 금액
    }


def normalize_items(data):
    """모델이 돌려준 JSON에서 이름과 금액이 있는 항목만 꺼낸다."""
    if isinstance(data, dict):
        data = data.get("items")
    if not isinstance(data, list):
        return []
    items = []
    for it in data:
        if not isinstance(it, dict):
            continue
        name = str(it.get("name") or it.get("item") or "").strip()
        price = to_int(it.get("price", it.get("amount")))
        if name and price is not None and price > 0:
            items.append({"name": name, "price": price})
    return items


@app.route("/", methods=["GET", "POST"])
def index():
    ctx = {"amount": "", "people": "", "result": None, "error": None,
           "items": None, "receipt_error": None}
    if request.method == "GET":
        return render_template("index.html", **ctx)

    action = request.form.get("action", "calc")
    people_raw = request.form.get("people", "").strip()
    ctx["people"] = people_raw
    people = to_int(people_raw)

    if action == "receipt":
        # 영수증 사진 읽기
        photo = request.files.get("photo")
        if not photo or not photo.filename:
            ctx["receipt_error"] = "사진을 골라 주세요."
            return render_template("index.html", **ctx)
        try:
            answer = ask(RECEIPT_PROMPT, photo.read(), photo.mimetype or "image/jpeg")
            items = normalize_items(parse_json(answer))
        except Exception as e:  # 모델 서버 연결 실패 등
            app.logger.warning("gemma4 호출 실패: %s", e)
            items = []
        if not items:
            ctx["receipt_error"] = "읽지 못했습니다"
            return render_template("index.html", **ctx)
        ctx["items"] = items
        total = sum(i["price"] for i in items)
        ctx["amount"] = f"{total}"
    elif action == "recalc":
        # 화면에서 고친 항목 금액으로 다시 계산
        names = request.form.getlist("item_name")
        prices = request.form.getlist("item_price")
        items = []
        for n, p in zip(names, prices):
            v = to_int(p)
            if n.strip() and v is not None and v > 0:
                items.append({"name": n.strip(), "price": v})
        ctx["items"] = items
        if not items:
            ctx["receipt_error"] = "항목이 없습니다. 금액을 확인해 주세요."
            return render_template("index.html", **ctx)
        ctx["amount"] = f"{sum(i['price'] for i in items)}"
    else:
        ctx["amount"] = request.form.get("amount", "").strip()

    total = to_int(ctx["amount"])
    if total is None or total <= 0:
        ctx["error"] = "금액을 1원 이상 입력해 주세요."
    elif people is None or people <= 0:
        ctx["error"] = "인원수를 1명 이상 입력해 주세요."
    elif people > 1000:
        ctx["error"] = "인원수가 너무 많습니다."
    else:
        ctx["result"] = split_amount(total, people)
    return render_template("index.html", **ctx)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
