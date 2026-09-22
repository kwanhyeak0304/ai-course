import json
import os
from datetime import datetime

def load_todos(filename):
    """todo.json 파일에서 할 일 목록을 불러옵니다."""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_todos(filename, todos):
    """할 일 목록을 todo.json 파일에 저장합니다."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(todos, f, ensure_ascii=False, indent=4)
    except IOError as e:
        print(f"파일 저장 중 오류가 발생했습니다: {e}")

def get_sort_key(todo):
    """마감일 기준으로 정렬하기 위한 키를 반환합니다. 마감일이 없으면 맨 뒤로 보냅니다."""
    if todo.get('due_date'):
        return (0, todo['due_date'])
    return (1, "")

def add_todo(todos):
    """새로운 할 일을 추가합니다 (마감일 포함)."""
    task = input("추가할 할 일을 입력하세요: ").strip()
    if not task:
        print("할 일 내용이 비어 있습니다.")
        return

    due_date_str = input("마감일을 입력하세요 (YYYY-MM-DD 형식, 없으면 엔터): ").strip()
    
    due_date = None
    if due_date_str:
        try:
            # 날짜 형식 검증
            datetime.strptime(due_date_str, "%Y-%m-%d")
            due_date = due_date_str
        except ValueError:
            print("날짜 형식이 잘못되었습니다. YYYY-MM-DD 형식을 사용해주세요.")
            print("할 일을 추가하지 않습니다.")
            return

    todos.append({
        "task": task, 
        "completed": False,
        "due_date": due_date
    })
    print(f"'{task}'(이)가 추가되었습니다.")

def list_todos(todos):
    """할 일 목록을 마감일 순으로 출력합니다."""
    if not todos:
        print("\n현재 할 일이 없습니다.")
        return

    # 마감일 기준으로 정렬하여 출력
    sorted_todos = sorted(todos, key=get_sort_key)

    print("\n--- 할 일 목록 (마감일 순) ---")
    for index, todo in enumerate(sorted_todos, start=1):
        status = "[V]" if todo['completed'] else "[ ]"
        due = f" | 마감: {todo['due_date']}" if todo.get('due_date') else ""
        print(f"{index}. {status} {todo['task']}{due}")
    print("------------------------------")
    return sorted_todos

def mark_todo_completed(todos):
    """할 일을 완료 상태로 표시합니다."""
    sorted_todos = list_todos(todos)
    if not sorted_todos:
        return

    try:
        choice = int(input("완료로 표시할 번호를 입력하세요: "))
        if 1 <= choice <= len(sorted_todos):
            # 정렬된 목록에서의 인덱스를 원본 리스트에서의 인덱스로 변환해야 함
            target_todo = sorted_todos[choice - 1]
            # 원본 리스트에서 해당 항목을 찾아 업데이트
            for todo in todos:
                if todo == target_todo:
                    todo['completed'] = True
                    break
            print(f"'{target_todo['task']}'(이)를 완료 처리했습니다.")
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해야 합니다.")

def delete_todo(todos):
    """할 일을 삭제합니다."""
    sorted_todos = list_todos(todos)
    if not sorted_todos:
        return

    try:
        choice = int(input("삭제할 번호를 입력하세요: "))
        if 1 <= choice <= len(sorted_todos):
            target_todo = sorted_todos[choice - 1]
            # 원본 리스트에서 해당 항목을 찾아 삭제
            for i, todo in enumerate(todos):
                if todo == target_todo:
                    removed = todos.pop(i)
                    print(f"'{removed['task']}'(이)가 삭제되었습니다.")
                    break
        else:
            print("잘못된 번호입니다.")
    except ValueError:
        print("숫자를 입력해야 합니다.")

def main():
    filename = 'todo.json'
    todos = load_todos(filename)

    while True:
        print("\n=== 할 일 관리 프로그램 ===")
        print("1. 할 일 추가")
        print("2. 목록 보기")
        print("3. 완료 표시")
        print("4. 삭제")
        print("5. 종료")
        
        choice = input("메뉴를 선택하세요 (1-5): ").strip()

        if choice == '1':
            add_todo(todos)
            save_todos(filename, todos)
        elif choice == '2':
            list_todos(todos)
        elif choice == '3':
            mark_todo_completed(todos)
            save_todos(filename, todos)
        elif choice == '4':
            delete_todo(todos)
            save_todos(filename, todos)
        elif choice == '5':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 선택입니다. 다시 입력해주세요.")

if __name__ == "__main__":
    main()
