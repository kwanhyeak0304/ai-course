import math
from datetime import datetime, timedelta

def parse_time(time_str):
    """시:분 형식을 datetime 객체로 변환"""
    # 9:30 -> 09:30 처리
    if ":" in time_str:
        try:
            h, m = time_str.split(":")
            time_str = f"{int(h):02d}:{int(m):02d}"
        except ValueError:
            raise ValueError("시간 형식이 올바르지 않습니다. (예: 09:30)")
    
    return datetime.strptime(time_str, "%H:%M")

def calculate_logic(arrival_time_str, departure_time_str):
    """요금 계산 핵심 로직"""
    try:
        arr = parse_time(arrival_time_str)
        dep = parse_time(departure_time_str)
    except ValueError as e:
        raise ValueError(str(e) if str(e) else "시간 형식이 잘못되었습니다. (예: 09:30)")

    # 자정을 넘기는 경우 처리 (출차가 입차보다 빠른 경우 다음 날로 간주)
    if dep <= arr:
        dep += timedelta(days=1)

    duration = dep - arr
    duration_minutes = int(duration.total_seconds() / 60)

    # 요금 규칙: 30분 무료, 이후 10분마다 500원 (나머지 10분 포함)
    if duration_minutes <= 30:
        fee = 0
    else:
        extra_minutes = duration_minutes - 30
        intervals = math.ceil(extra_minutes / 10)
        fee = intervals * 500

    # 하루 최대 요금 20,000원 제한
    if fee > 20000:
        fee = 20000

    # 지속 시간 포맷팅
    hours = duration_minutes // 60
    mins = duration_minutes % 60
    if hours > 0:
        duration_display = f"{hours}시간 {mins}분"
    else:
        duration_display = f"{mins}분"

    return duration_display, fee

# --- GUI 부분 ---
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

if GUI_AVAILABLE:
    class ParkingCalculatorApp:
        def __init__(self, root):
            self.root = root
            self.root.title("주차 요금 계산기")
            self.root.geometry("600x500")

            # 데이터 저장용 리스트 (Treeview의 item ID와 요금을 매핑)
            self.record_fees = {}

            # UI 설정
            self._setup_ui()

        def _setup_ui(self):
            # 1. 입력 프레임
            input_frame = ttk.LabelFrame(self.root, text="주차 정보 입력 (HH:MM)", padding=10)
            input_frame.pack(fill="x", padx=10, pady=10)

            ttk.Label(input_frame, text="입차 시각:").grid(row=0, column=0, padx=5, pady=5)
            self.entry_arrival = ttk.Entry(input_frame, width=10)
            self.entry_arrival.grid(row=0, column=1, padx=5, pady=5)
            self.entry_arrival.insert(0, "09:00")

            ttk.Label(input_frame, text="출차 시각:").grid(row=0, column=2, padx=5, pady=5)
            self.entry_departure = ttk.Entry(input_frame, width=10)
            self.entry_departure.grid(row=0, column=3, padx=5, pady=5)
            self.entry_departure.insert(0, "10:00")

            btn_calculate = ttk.Button(input_frame, text="계산 및 추가", command=self.add_record)
            btn_calculate.grid(row=0, column=4, padx=10, pady=5)

            # 2. 목록 프레임 (Treeview)
            list_frame = ttk.LabelFrame(self.root, text="주차 기록 목록", padding=10)
            list_frame.pack(fill="both", expand=True, padx=10, pady=5)

            columns = ("arrival", "departure", "duration", "fee")
            self.tree = ttk.Treeview(list_frame, columns=columns, show="headings")
            
            self.tree.heading("arrival", text="입차 시각")
            self.tree.heading("departure", text="출차 시각")
            self.tree.heading("duration", text="주차 시간")
            self.tree.heading("fee", text="요금")

            self.tree.column("arrival", width=100, anchor="center")
            self.tree.column("departure", width=100, anchor="center")
            self.tree.column("duration", width=120, anchor="center")
            self.tree.column("fee", width=100, anchor="center")

            self.tree.pack(side="left", fill="both", expand=True)

            scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
            self.tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # 3. 하단 제어 프레임
            bottom_frame = ttk.Frame(self.root, padding=10)
            bottom_frame.pack(fill="x")

            btn_delete = ttk.Button(bottom_frame, text="선택 삭제", command=self.delete_selected)
            btn_delete.pack(side="left", padx=5)

            self.label_total = ttk.Label(bottom_frame, text="총 합계: 0원", font=("Helvetica", 12, "bold"))
            self.label_total.pack(side="right", padx=5)

        def add_record(self):
            arr_str = self.entry_arrival.get().strip()
            dep_str = self.entry_departure.get().strip()

            if not arr_str or not dep_str:
                messagebox.showwarning("입력 오류", "입차 및 출차 시각을 모두 입력해주세요.")
                return

            try:
                duration_display, fee = calculate_logic(arr_str, dep_str)
                
                item_id = self.tree.insert("", "end", values=(arr_str, dep_str, duration_display, f"{fee:,}원"))
                self.record_fees[item_id] = fee
                self.update_total()

            except ValueError as e:
                messagebox.showerror("오류", str(e))

        def delete_selected(self):
            selected_items = self.tree.selection()
            if not selected_items:
                messagebox.showwarning("삭제 오류", "삭제할 항목을 선택해주세요.")
                return

            for item_id in selected_items:
                self.tree.delete(item_id)
                if item_id in self.record_fees:
                    del self.record_fees[item_id]
            
            self.update_total()

        def update_total(self):
            total_fee = sum(self.record_fees.values())
            self.label_total.config(text=f"총 합계: {total_fee:,}원")

else:
    print("GUI 모듈을 사용할 수 없습니다. 로직 테스트만 가능합니다.")

if __name__ == "__main__":
    if GUI_AVAILABLE:
        root = tk.Tk()
        app = ParkingCalculatorApp(root)
        root.mainloop()
