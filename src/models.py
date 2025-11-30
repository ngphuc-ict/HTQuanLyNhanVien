from datetime import *

# 1. NHÂN VIÊN

class NhanVien:
    def __init__(self, employee_id, ho_ten, ngay_sinh, gioi_tinh, dept_id, position_id, ngay_vao_lam, email, phone, address, status="Active"):
        self.employee_id = employee_id
        self.ho_ten = ho_ten
        self.ngay_sinh = ngay_sinh
        self.gioi_tinh = gioi_tinh
        self.dept_id = dept_id
        self.position_id = position_id
        self.ngay_vao_lam = ngay_vao_lam
        self.email = email
        self.phone = phone
        self.address = address
        self.status = status

    def hien_thi_thong_tin(self):
        print("----- THÔNG TIN NHÂN VIÊN -----")
        print("ID:", self.employee_id)
        print("Họ tên:", self.ho_ten)
        print("Giới tính:", self.gioi_tinh)
        print("Ngày sinh:", self.ngay_sinh)
        print("Phòng ban:", self.dept_id)
        print("Chức vụ:", self.position_id)
        print("Ngày vào làm:", self.ngay_vao_lam)
        print("Email:", self.email)
        print("SĐT:", self.phone)
        print("Địa chỉ:", self.address)
        print("Trạng thái:", self.status)

    def tinh_tuoi(self):
        today = date.today()
        ns = datetime.strptime(self.ngay_sinh, "%Y-%m-%d").date()
        return today.year - ns.year - ((today.month, today.day) < (ns.month, ns.day))

    def tinh_tham_nien(self):
        today = date.today()
        nvl = datetime.strptime(self.ngay_vao_lam, "%Y-%m-%d").date()
        return today.year - nvl.year - ((today.month, today.day) < (nvl.month, nvl.day))

# 2. PHÒNG BAN

class Department:
    def __init__(self, dept_id, name, manager_id, created_date, budget):
        self.dept_id = dept_id
        self.name = name
        self.manager_id = manager_id
        self.created_date = created_date
        self.budget = budget

    def get_employee_count(self, employees):
        count = 0
        for e in employees:
            if e.dept_id == self.dept_id:
                count += 1
        return count

    def get_manager_info(self, employees):
        for e in employees:
            if e.employee_id == self.manager_id:
                return e.ho_ten
        return "Không tìm thấy"

    def get_department_salary_budget(self, salaries):
        total = 0
        for s in salaries:
            if s.employee_id == self.manager_id:
                total += s.calculate_net_salary(0)
        return total

# 3. CHỨC VỤ

class Position:
    def __init__(self, position_id, title, level, min_salary, max_salary, basic_salary):
        self.position_id = position_id
        self.title = title
        self.level = level
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.basic_salary = basic_salary

# 4. CHẤM CÔNG

class Attendance:
   class Attendance:
    """`Attendance` đại diện cho một bản ghi chấm công một ngày của nhân viên.

    Những cải tiến chính trong lớp này nhằm đáp ứng yêu cầu hệ thống:
    - Phân tích (parse) linh hoạt cho `check_in`/`check_out` chấp nhận định dạng
        `HH:MM` hoặc chuỗi datetime đầy đủ. Tương thích ngược với mã hiện tại.
    - Hàm trợ giúp `mark_check_in` / `mark_check_out` để ghi thời gian hiện tại
        (hoặc thời gian được truyền vào), ngăn trùng và kiểm tra thứ tự thời gian.
    - Định nghĩa `SHIFTS` để hỗ trợ nhiều ca (sáng/chiều/tối).
    - Tự động tính `late_minutes` và `leave_minutes` theo giờ bắt đầu/kết thúc ca
        (xử lý cả ca qua đêm).
    - `calculate_working_hours` xử lý tốt ca qua đêm và giá trị thiếu.
    - `is_duplicate` hỗ trợ kiểm tra trùng lặp bản ghi ở mức bản ghi đơn.
    - `to_csv_row` trả về dữ liệu theo hàng để xuất CSV/DB.

    Lưu ý: lớp này tập trung vào logic trên một bản ghi; việc kiểm tra trùng lặp
    ở mức cao hơn (ví dụ kiểm tra trên DB) nên kết hợp `is_duplicate` với truy
    vấn lưu trữ ở tầng dịch vụ.
    """

        # Định nghĩa ca mặc định (có thể mở rộng khi chạy)
    SHIFTS = {
        "morning": {"start": "08:00", "end": "12:00"},
        "afternoon": {"start": "13:00", "end": "17:00"}
    }

    def __init__(self, attendance_id, employee_id, date, check_in, check_out, status,
                 late_minutes=0, leave_minutes=0):
        self.attendance_id = attendance_id
        self.employee_id = employee_id
        self.date = date
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.late_minutes = late_minutes
        self.leave_minutes = leave_minutes

    @staticmethod
    def _parse_time(time_str, day=None):
        """Chuyển chuỗi thời gian thành `datetime` trên ngày `day`.

        Chấp nhận các định dạng: "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%H:%M".
        Nếu chỉ cung cấp giờ (`"HH:MM"`), cần truyền `day` (dạng "YYYY-MM-DD")
        để tạo một `datetime` cụ thể. Trả về `None` nếu không parse được.
        """
        if not time_str:
            return None
        # Thử các định dạng datetime đầy đủ trước
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
            try:
                return datetime.strptime(time_str, fmt)
            except Exception:
                continue

        # Thử định dạng chỉ giờ
        try:
            t = datetime.strptime(time_str, "%H:%M").time()
            if day:
                day_date = datetime.strptime(day, "%Y-%m-%d").date()
                return datetime.combine(day_date, t)
            # Nếu không có `day`, trả về datetime trên một ngày mặc định (1900-01-01)
            return datetime.combine(date(1900, 1, 1), t)
        except Exception:
            return None

    def detect_shift(self):
        """Xác định ca làm việc dựa trên thời gian `check_in`; mặc định trả về 'morning'."""
        ci = self._parse_time(self.check_in, self.date)
        if not ci:
            return "morning"
        time_only = ci.time()
        for name, s in self.SHIFTS.items():
            start = datetime.strptime(s["start"], "%H:%M").time()
            end = datetime.strptime(s["end"], "%H:%M").time()
            # Xử lý ca qua đêm
            if start <= end:
                if start <= time_only <= end:
                    return name
            else:
                # Ví dụ ca qua đêm: 22:00 - 06:00
                if time_only >= start or time_only <= end:
                    return name
        return "morning"

    def mark_check_in(self, time_str=None):
        """Ghi nhận thời gian check-in. Nếu `time_str` là None thì dùng thời gian hiện tại.

        Ném `ValueError` nếu đã có thời gian check-in trước đó.
        """
        if self.check_in:
            raise ValueError("Check-in already recorded")
        if time_str is None:
            self.check_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.check_in = time_str
        # By default, persist the check-in to DB if AttendanceService is available.
        # Use runtime import to avoid circular import issues and catch exceptions
        # so a missing/incorrect DB config won't crash the app.
        try:
            from services import AttendanceService
            service = AttendanceService()
            # attempt to save; if no DB config exists this will be caught
            service.check_in(self)
        except Exception:
            # keep silent/fallback: application can continue even when DB not available
            # In a production app you'd probably log the exception
            pass

    def mark_check_in_now(self, time_only=False):
        """Ghi thời gian check-in hiện tại.

        time_only = False (mặc định) -> lưu chuỗi full datetime "YYYY-MM-DD HH:MM:SS".
        time_only = True -> lưu chỉ giờ: "HH:MM". Việc này hữu dụng khi UI chỉ cần
        một thời gian ngắn gọn cho thao tác chấm công (không lưu ngày lúc client tự
        động chọn ngày khác).
        """
        if self.check_in:
            raise ValueError("Check-in already recorded")
        if time_only:
            self.check_in = datetime.now().strftime("%H:%M")
        else:
            self.check_in = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status = "Present"
        # Auto-persist into DB using AttendanceService if available.
        # We do a runtime import and catch exceptions to avoid hard dependency
        # on a configured database for local runs / tests.
        try:
            from services import AttendanceService
            AttendanceService().check_in(self)
        except Exception:
            pass

    def mark_check_out(self, time_str=None):
        """Ghi nhận thời gian check-out.

        Kiểm tra rằng đã có check-in trước đó và cập nhật `late_minutes` và
        `leave_minutes` bằng cách gọi `compute_late_and_early`.
        """
        if not self.check_in:
            raise ValueError("Cannot check out without a check-in")
        if self.check_out:
            raise ValueError("Check-out already recorded")

        if time_str is None:
            self.check_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self.check_out = time_str

        # Kiểm tra thứ tự thời gian và tính trễ/về sớm
        shift = self.detect_shift()
        late, early = self.compute_late_and_early(shift)
        self.late_minutes = late
        self.leave_minutes = early
        # Try to persist check-out to DB (update existing record). Use runtime import
        # and swallow exceptions to remain robust without DB runtime.
        try:
            from services import AttendanceService
            service = AttendanceService()
            # service.check_out expects (employee_id, date, check_out_time)
            service.check_out(self.employee_id, self.date, self.check_out)
        except Exception:
            pass

    def mark_check_out_now(self, time_only=False):
        """Ghi thời gian check-out hiện tại.

        Thao tác tương tự `mark_check_in_now` nhưng còn tính `late_minutes` và
        `leave_minutes` dựa trên ca làm việc hiện tại.
        """
        if not self.check_in:
            raise ValueError("Cannot check out without a check-in")
        if self.check_out:
            raise ValueError("Check-out already recorded")

        if time_only:
            self.check_out = datetime.now().strftime("%H:%M")
        else:
            self.check_out = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Tính trễ/về sớm theo ca
        shift = self.detect_shift()
        late, early = self.compute_late_and_early(shift)
        self.late_minutes = late
        self.leave_minutes = early
        # Auto-persist check_out as well (update existing DB record)
        try:
            from services import AttendanceService
            AttendanceService().check_out(self.employee_id, self.date, self.check_out)
        except Exception:
            pass

    def compute_late_and_early(self, shift_name="morning"):
        """Tính số phút đi muộn và về sớm so với ca làm việc.

        Trả về tuple: (late_minutes:int, early_leave_minutes:int)
        """
        s = self.SHIFTS.get(shift_name)
        if not s:
            return 0, 0

        ci = self._parse_time(self.check_in, self.date)
        co = self._parse_time(self.check_out, self.date)
        if not ci or not co:
            return 0, 0

        # Tạo datetime cho thời điểm bắt đầu ca trên cùng ngày `self.date`.
        shift_start = datetime.combine(datetime.strptime(self.date, "%Y-%m-%d").date(),
                                       datetime.strptime(s["start"], "%H:%M").time())
        shift_end_time = datetime.strptime(s["end"], "%H:%M").time()
        # Nếu thời gian kết thúc <= thời gian bắt đầu thì xem là ca qua đêm -> cộng thêm 1 ngày
        if datetime.strptime(s["end"], "%H:%M").time() <= datetime.strptime(s["start"], "%H:%M").time():
            shift_end = datetime.combine(shift_start.date(), shift_end_time) + timedelta(days=1)
            # Nếu check-out nhỏ hơn check-in (ví dụ do ca qua đêm), cộng thêm 1 ngày cho check-out
            if co < ci:
                co = co + timedelta(days=1)
        else:
            shift_end = datetime.combine(shift_start.date(), shift_end_time)

        late = max(0, int((ci - shift_start).total_seconds() // 60))
        early = max(0, int((shift_end - co).total_seconds() // 60))
        return late, early

    def calculate_working_hours(self):
        """Tính tổng số giờ làm việc giữa thời gian check-in và check-out.

        Hỗ trợ đầu vào ở định dạng `HH:MM` hoặc định dạng ngày giờ đầy đủ.
        Đối với ca qua đêm (check-out rơi vào ngày kế tiếp), phép tính trả về
        kết quả dương.
        """
        if not self.check_in or not self.check_out:
            return 0.0

        ci = self._parse_time(self.check_in, self.date)
        co = self._parse_time(self.check_out, self.date)
        if not ci or not co:
            return 0.0

        # Nếu check-out trước check-in, giả sử là ca qua đêm -> cộng thêm 1 ngày cho check-out
        if co < ci:
            co += timedelta(days=1)

        diff = co - ci
        return diff.total_seconds() / 3600.0

    def is_duplicate(self, other):
        """hàm check trùng lặp
        """
        if not isinstance(other, Attendance):
            return False
        return (self.employee_id == other.employee_id and
                self.date == other.date and
                (self.check_in == other.check_in))

    def to_csv_row(self):
        """trả về file csv(Phúc sửa đoạn này cho anh để nó trả về database nhé)."""
        return [
            self.attendance_id,
            self.employee_id,
            self.date,
            self.check_in or "",
            self.check_out or "",
            str(self.calculate_working_hours()),
            str(self.late_minutes),
            str(self.leave_minutes),
            self.status
        ]
    


# ===============================
# 6. BẢNG LƯƠNG
# ===============================

class SalaryRecord:
    def __init__(self, salary_id, employee_id, month, year,
                 basic_salary, working_days, overtime_hours,
                 bonus, kpi, allowance, tax):
        self.salary_id = salary_id
        self.employee_id = employee_id
        self.month = month
        self.year = year
        self.basic_salary = basic_salary
        self.working_days = working_days
        self.overtime_hours = overtime_hours
        self.bonus = bonus
        self.kpi = kpi
        self.allowance = allowance
        self.tax = tax  # thuế khác nếu có

    def calculate_overtime_pay(self):
        # OT: số giờ × 1.5 × (lương / 8)
        return self.overtime_hours * 1.5 * (self.basic_salary / 8)

    def calculate_basic_salary_by_workdays(self):
        # Lương cơ bản theo ngày công (giả sử 26 ngày chuẩn)
        return (self.basic_salary / 26) * self.working_days

    def calculate_gross_salary(self):
        gross = (
            self.calculate_basic_salary_by_workdays()
            + self.calculate_overtime_pay()
            + self.bonus
            + self.kpi
            + self.allowance
        )
        return gross

    def calculate_net_salary(self, late_minutes):
        gross = self.calculate_gross_salary()

        # Khấu trừ theo báo cáo
        bhxh = 0.101 * self.basic_salary
        cong_doan = 0.01 * self.basic_salary
        thue_tncn = 0.05 * self.basic_salary
        phat_di_muon = 2000 * late_minutes

        deductions = bhxh + cong_doan + thue_tncn + phat_di_muon + self.tax

        return gross - deductions
