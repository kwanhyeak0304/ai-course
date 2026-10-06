# 할 일 관리 웹앱 (Todo App) 스펙 문서

## 1. 개요
Python Flask와 SQLite를 사용하여 개발하는 경량 할 일 관리 웹 애플리케이션이다.

## 2. 기술
- Python 3
- Flask
- SQLite3 (표준 라이브러리)
- HTML5, CSS3 (외부 프레임워크 미사용)

## 3. 파일 구성
- `app.py`: 웹 서버 구동 및 HTTP 라우트 처리
- `db.py`: SQLite 데이터베이스 연동 함수 모음 (초기화, 조회, 추가, 토글, 삭제)
- `test_app.py`: Flask test_client 기반 자동화 단위/통합 테스트
- `templates/index.html`: 할 일 목록 및 입력 폼 화면 템플릿
- `static/style.css`: 사용자 인터페이스 스타일시트
- `.clinerules`: 에이전트 지침 및 규칙 파일
- `PROGRESS.md`: 프로젝트 진행 상황 기록 문서

## 4. 동작 규칙
| 메서드 | 주소 | 입력 | 결과 |
| --- | --- | --- | --- |
| GET | `/` | 없음 | 200 OK, 할 일 목록 페이지 렌더링 (미완료 항목 상단, 완료 항목 하단 취소선) |
| POST | `/add` | form 데이터 `title` | 정상 입력 시 302 리다이렉트 (`/`), 새 할 일 추가 |
| POST | `/add` | 빈 문자열 또는 공백만 있는 `title` | 400 Bad Request, 추가되지 않음 |
| POST | `/add` | 100자 초과 긴 `title` | 400 Bad Request, 추가되지 않음 |
| POST | `/toggle/<int:id>` | URL 파라미터 `id` | 존재하는 id: 302 리다이렉트 (`/`), 완료 여부(0/1) 반전 |
| POST | `/toggle/<int:id>` | 존재하지 않는 id | 404 Not Found |
| POST | `/delete/<int:id>` | URL 파라미터 `id` | 존재하는 id: 302 리다이렉트 (`/`), 항목 삭제 |
| POST | `/delete/<int:id>` | 존재하지 않는 id | 404 Not Found |

## 5. 화면
- 상단: 타이틀 ("할 일 관리") 및 새 할 일 입력창 + "추가" 버튼
- 중앙: 할 일 목록
  - 미완료 할 일: 체크박스/버튼 (완료 표시), 제목 텍스트, 삭제 버튼
  - 완료된 할 일: 체크박스/버튼 (완료 해제), 취소선 적용된 텍스트, 삭제 버튼
- 반응형 레이아웃 및 깔끔한 카드 형태 디자인

## 6. 테스트 (test_client 검증 항목)
| 번호 | 요청 | 기대하는 결과 |
| --- | --- | --- |
| 1 | GET `/` | 200 OK, HTML 본문 반환 |
| 2 | POST `/add` with `title="파이썬 공부"` | 302 리다이렉트, DB에 항목 1개 생성 |
| 3 | GET `/` (추가 후) | 200 OK, 본문에 "파이썬 공부" 포함 |
| 4 | POST `/toggle/1` | 302 리다이렉트, 완료 상태(done=1)로 변경 |
| 5 | GET `/` (완료 후) | 200 OK, 취소선 스타일 또는 완료 표시 클래스 확인 |
| 6 | POST `/toggle/1` (재토글) | 302 리다이렉트, 미완료 상태(done=0)로 복원 |
| 7 | POST `/delete/1` | 302 리다이렉트, 항목 삭제 확인 |
| 8 | GET `/` (삭제 후) | 200 OK, 본문에 "파이썬 공부" 없음 |
| 9 | POST `/add` with `title=""` (빈 제목) | 400 Bad Request |
| 10 | POST `/add` with `title="   "` (공백 제목) | 400 Bad Request |
| 11 | POST `/add` with `title="a" * 101` (100자 초과 제목) | 400 Bad Request |
| 12 | POST `/toggle/999` (없는 번호) | 404 Not Found |
| 13 | POST `/delete/999` (없는 번호) | 404 Not Found |

## 7. 완료 전 점검
- `python test_app.py` 실행 시 모든 테스트(13개) 통과 확인
- 브라우저에서 직접 추가, 완료/해제, 삭제가 매끄럽게 동작하는지 확인
- 데이터베이스 파일이 영속화되어 서버 재시작 후에도 유지되는지 확인

## 8. 하지 않는 것
- 사용자 로그인 및 회원가입 인증 기능
- 할 일 수정 (내용 변경) 기능
- 외부 CSS 프레임워크 (Bootstrap, Tailwind 등) 사용
- 자바스크립트 프레임워크 (React, Vue 등) 사용
