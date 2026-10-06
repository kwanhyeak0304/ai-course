from flask import Flask, render_template, request, redirect, abort, url_for
import db

app = Flask(__name__)
app.config["DATABASE"] = db.DEFAULT_DB


def get_db_path():
    return app.config.get("DATABASE", db.DEFAULT_DB)


@app.route("/")
def index():
    todos = db.get_todos(get_db_path())
    return render_template("index.html", todos=todos)


@app.route("/add", methods=["POST"])
def add():
    raw_title = request.form.get("title", "")
    title = raw_title.strip()
    if not title:
        abort(400, "제목을 입력해주세요.")
    if len(title) > 100:
        abort(400, "제목은 100자 이하여야 합니다.")
    db.add_todo(title, get_db_path())
    return redirect(url_for("index"))


@app.route("/toggle/<int:id>", methods=["POST"])
def toggle(id):
    success = db.toggle_todo(id, get_db_path())
    if not success:
        abort(404, "존재하지 않는 할 일입니다.")
    return redirect(url_for("index"))


@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    success = db.delete_todo(id, get_db_path())
    if not success:
        abort(404, "존재하지 않는 할 일입니다.")
    return redirect(url_for("index"))


if __name__ == "__main__":
    db.init_db(get_db_path())
    app.run(debug=True, port=5000)
