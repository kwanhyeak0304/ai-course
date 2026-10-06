import gc
import os
import tempfile
import unittest
from app import app
import db


class TodoAppTestCase(unittest.TestCase):
    def setUp(self):
        # 임시 데이터베이스 파일 생성
        self.db_fd, self.temp_db_path = tempfile.mkstemp(suffix=".db")
        os.close(self.db_fd)
        app.config["DATABASE"] = self.temp_db_path
        app.config["TESTING"] = True
        self.client = app.test_client()

        # 데이터베이스 초기화
        db.init_db(self.temp_db_path)

    def tearDown(self):
        # 임시 데이터베이스 정리
        gc.collect()
        try:
            if os.path.exists(self.temp_db_path):
                os.remove(self.temp_db_path)
        except PermissionError:
            pass

    # 1. 목록 조회 (빈 목록)
    def test_01_index_empty(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("할 일 관리".encode("utf-8"), res.data)
        self.assertIn("등록된 할 일이 없습니다".encode("utf-8"), res.data)

    # 2. 할 일 추가 정상 동작
    def test_02_add_todo_success(self):
        res = self.client.post("/add", data={"title": "파이썬 공부"}, follow_redirects=False)
        self.assertEqual(res.status_code, 302)
        todos = db.get_todos(self.temp_db_path)
        self.assertEqual(len(todos), 1)
        self.assertEqual(todos[0]["title"], "파이썬 공부")
        self.assertEqual(todos[0]["done"], 0)

    # 3. 추가 후 목록에 표시되는지 확인
    def test_03_index_shows_added_todo(self):
        self.client.post("/add", data={"title": "파이썬 공부"})
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn("파이썬 공부".encode("utf-8"), res.data)

    # 4. 할 일 완료 토글 (0 -> 1)
    def test_04_toggle_to_done(self):
        self.client.post("/add", data={"title": "완료할 항목"})
        todos = db.get_todos(self.temp_db_path)
        todo_id = todos[0]["id"]

        res = self.client.post(f"/toggle/{todo_id}")
        self.assertEqual(res.status_code, 302)

        updated = db.get_todo(todo_id, self.temp_db_path)
        self.assertEqual(updated["done"], 1)

    # 5. 완료 후 목록 화면에 취소선 및 완료 클래스 확인
    def test_05_index_shows_completed_style(self):
        self.client.post("/add", data={"title": "취소선 테스트"})
        todos = db.get_todos(self.temp_db_path)
        todo_id = todos[0]["id"]
        self.client.post(f"/toggle/{todo_id}")

        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertIn(b"completed-text", res.data)

    # 6. 완료 재토글 (1 -> 0 미완료 복원)
    def test_06_toggle_back_to_undone(self):
        self.client.post("/add", data={"title": "재토글 항목"})
        todos = db.get_todos(self.temp_db_path)
        todo_id = todos[0]["id"]

        self.client.post(f"/toggle/{todo_id}")
        self.client.post(f"/toggle/{todo_id}")

        updated = db.get_todo(todo_id, self.temp_db_path)
        self.assertEqual(updated["done"], 0)

    # 7. 할 일 삭제 정상 동작
    def test_07_delete_todo(self):
        self.client.post("/add", data={"title": "삭제할 항목"})
        todos = db.get_todos(self.temp_db_path)
        todo_id = todos[0]["id"]

        res = self.client.post(f"/delete/{todo_id}")
        self.assertEqual(res.status_code, 302)

        todos_after = db.get_todos(self.temp_db_path)
        self.assertEqual(len(todos_after), 0)

    # 8. 삭제 후 화면에서 사라졌는지 확인
    def test_08_index_after_delete(self):
        self.client.post("/add", data={"title": "사라질 항목"})
        todos = db.get_todos(self.temp_db_path)
        todo_id = todos[0]["id"]
        self.client.post(f"/delete/{todo_id}")

        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        self.assertNotIn("사라질 항목".encode("utf-8"), res.data)

    # 9. 잘못된 입력 1: 빈 제목
    def test_09_add_empty_title_bad_request(self):
        res = self.client.post("/add", data={"title": ""})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(db.get_todos(self.temp_db_path)), 0)

    # 10. 잘못된 입력 2: 공백 문자열 제목
    def test_10_add_whitespace_title_bad_request(self):
        res = self.client.post("/add", data={"title": "     "})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(db.get_todos(self.temp_db_path)), 0)

    # 11. 잘못된 입력 3: 100자 초과 긴 제목
    def test_11_add_too_long_title_bad_request(self):
        long_title = "a" * 101
        res = self.client.post("/add", data={"title": long_title})
        self.assertEqual(res.status_code, 400)
        self.assertEqual(len(db.get_todos(self.temp_db_path)), 0)

    # 12. 없는 번호 토글 시 404
    def test_12_toggle_nonexistent_not_found(self):
        res = self.client.post("/toggle/99999")
        self.assertEqual(res.status_code, 404)

    # 13. 없는 번호 삭제 시 404
    def test_13_delete_nonexistent_not_found(self):
        res = self.client.post("/delete/99999")
        self.assertEqual(res.status_code, 404)


if __name__ == "__main__":
    unittest.main()
