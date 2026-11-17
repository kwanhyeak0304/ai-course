from flask import Flask, render_template, request

app = Flask(__name__)
# 아이폰 사진은 한 장에 수 MB라서 여유 있게 20MB까지 받는다.
app.config["MAX_CONTENT_LENGTH"] = 20 * 1024 * 1024


def get_photo():
    """카메라 버튼과 앨범 버튼 중 실제로 파일이 담긴 쪽을 돌려준다. 없으면 None."""
    for f in request.files.getlist("photo"):
        if f and f.filename:
            return f
    return None


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", step="upload")

    photo = get_photo()
    if photo is None:
        return render_template("index.html", step="upload", error="사진을 먼저 골라 주세요.")

    data = photo.read()
    mime = photo.mimetype or "image/jpeg"
    print(f"[1단계] 사진 받음: {photo.filename}, {mime}, {len(data):,} bytes")
    return render_template(
        "index.html",
        step="received",
        filename=photo.filename,
        mime=mime,
        size_kb=round(len(data) / 1024),
    )


@app.errorhandler(413)
def too_large(e):
    return render_template("index.html", step="upload", error="사진이 너무 큽니다. 20MB 이하로 올려 주세요."), 413


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
