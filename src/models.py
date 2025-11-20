from datetime import *


# ===============================
# 1. NHÂN VIÊN
# ===============================

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


# ===============================
# 2. PHÒNG BAN
# ===============================

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


# ===============================
# 3. CHỨC VỤ
# ===============================

class Position:
    def __init__(self, position_id, title, level, min_salary, max_salary, basic_salary):
        self.position_id = position_id
        self.title = title
        self.level = level
        self.min_salary = min_salary
        self.max_salary = max_salary
        self.basic_salary = basic_salary


# ===============================
# 4. CHẤM CÔNG
# ===============================

class Attendance:
    # Định nghĩa các ca làm việc (Giờ vào - Giờ ra)
    SHIFTS = {
        "Sáng": ("08:00", "17:00"),
        "Chiều": ("13:00", "22:00"),
        "Tối": ("22:00", "06:00")
    }

    def __init__(self, attendance_id, employee_id, date, check_in, check_out=None, status="Present",
                 late_minutes=0, leave_minutes=0):
        self.attendance_id = attendance_id
        self.employee_id = employee_id
        self.date = date
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.late_minutes = late_minutes
        self.leave_minutes = leave_minutes

    def detect_shift(self):
        """Đoán ca làm việc dựa trên giờ check-in"""
        check_in_time = datetime.strptime(self.check_in, "%H:%M")
        
        if 7 <= check_in_time.hour < 12:
            return "Sáng"
        elif 12 <= check_in_time.hour < 18:
            return "Chiều"
        else:
            return "Tối"

    def compute_late_and_early(self, check_out_str):
        """Tính toán đi muộn về sớm"""
        self.check_out = check_out_str
        shift_name = self.detect_shift()
        std_in, std_out = self.SHIFTS[shift_name]

        # Chuyển đổi sang datetime để so sánh
        fmt = "%H:%M"
        t_in = datetime.strptime(self.check_in, fmt)
        t_out = datetime.strptime(self.check_out, fmt)
        std_in_dt = datetime.strptime(std_in, fmt)
        std_out_dt = datetime.strptime(std_out, fmt)

        # Xử lý ca qua đêm (nếu giờ ra nhỏ hơn giờ vào, tức là sang ngày hôm sau)
        if t_out < t_in:
            t_out += timedelta(days=1)
        if std_out_dt < std_in_dt:
            std_out_dt += timedelta(days=1)

        # Tính đi muộn
        late = (t_in - std_in_dt).total_seconds() / 60
        self.late_minutes = int(late) if late > 0 else 0

        # Tính về sớm
        early = (std_out_dt - t_out).total_seconds() / 60
        self.leave_minutes = int(early) if early > 0 else 0
# ===============================
# 5. ĐƠN LÀM THÊM GIỜ
# ===============================

class OvertimeRequest:
    def __init__(self, request_id, employee_id, ot_date, hours_requested, reason, request_status="Pending",
                 approver_id=None, approval_date=None):
        self.request_id = request_id
        self.employee_id = employee_id
        self.ot_date = ot_date
        self.hours_requested = hours_requested
        self.reason = reason
        self.request_status = request_status
        self.approver_id = approver_id
        self.approval_date = approval_date

    def submit_request(self):
        self.request_status = "Pending"

    def approve(self, approver_id):
        self.request_status = "Approved"
        self.approver_id = approver_id
        self.approval_date = str(date.today())

    def deny(self, approver_id):
        self.request_status = "Denied"
        self.approver_id = approver_id
        self.approval_date = str(date.today())


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
