from datetime import *

# Cấu hình mặc định cho tính lương
WORKDAYS_PER_MONTH = 26
HOURS_PER_DAY = 8
POSITION_RULES = {
    "Intern": {
        "allowance_rate": 0.05,   
        "bonus_rate": 0.0,        
        "overtime_multiplier": 1.0
    },
    "Nhân viên": {
        "allowance_rate": 0.1,    
        "bonus_rate": 0.05,       
        "overtime_multiplier": 1.5
    },
    "Trưởng phòng": {
        "allowance_rate": 0.2,    
        "bonus_rate": 0.1,        
        "overtime_multiplier": 1.2
    },
    "Giám đốc": {
        "allowance_rate": 0.3,    
        "bonus_rate": 0.2,        
        "overtime_multiplier": 0 
    }
}

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
    def __init__(self, position_id, title, level, min_salary, max_salary):
        self.position_id = position_id
        self.title = title
        self.level = level
        self.min_salary = min_salary
        self.max_salary = max_salary

# 4. CHẤM CÔNG
class Attendance:
    SHIFTS = {
        "morning": {"start": "08:00", "end": "12:00"},
        "afternoon": {"start": "13:00", "end": "17:00"}
    }

    def __init__(self, attendance_id, employee_id, date):
        self.attendance_id = attendance_id
        self.employee_id = employee_id
        self.date = date
        self.check_in = None
        self.check_out = None
        self.late_minutes = 0
        self.leave_minutes = 0

    def mark_check_in(self):
        if self.check_in:
            raise ValueError("Đã có check-in")
        self.check_in = datetime.now()

    def mark_check_out(self):
        if not self.check_in:
            raise ValueError("Chưa check-in")
        if self.check_out:
            raise ValueError("Đã có check-out")
        self.check_out = datetime.now()
        self._compute_late_and_early()

    def _compute_late_and_early(self):
        """Tính đi muộn và về sớm theo ca"""
        shift = self.detect_shift()
        s = self.SHIFTS[shift]
        shift_start = datetime.combine(datetime.strptime(self.date, "%Y-%m-%d").date(),
                                       datetime.strptime(s["start"], "%H:%M").time())
        shift_end = datetime.combine(datetime.strptime(self.date, "%Y-%m-%d").date(),
                                     datetime.strptime(s["end"], "%H:%M").time())

        self.late_minutes = max(0, int((self.check_in - shift_start).total_seconds() // 60))
        self.leave_minutes = max(0, int((shift_end - self.check_out).total_seconds() // 60))

    def detect_shift(self):
        """Xác định ca dựa trên giờ check-in"""
        time_only = self.check_in.time()
        for name, s in self.SHIFTS.items():
            start = datetime.strptime(s["start"], "%H:%M").time()
            end = datetime.strptime(s["end"], "%H:%M").time()
            if start <= time_only <= end:
                return name
        return "morning"

    def calculate_working_hours(self):
        if not self.check_in or not self.check_out:
            return 0.0
        diff = self.check_out - self.check_in
        return round(diff.total_seconds() / 3600, 2)

    

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
                 bonus, kpi, allowance, tax, position):
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
        self.position = position
    def calculate_salary_by_position(self, late_minutes):
        rules = POSITION_RULES.get(self.position, {})
        
        # Phụ cấp và thưởng theo vị trí
        allowance = rules.get("allowance_rate", 0) * self.basic_salary
        bonus = rules.get("bonus_rate", 0) * self.basic_salary
        
        # Overtime theo vị trí
        try:
            hourly = self.basic_salary / (WORKDAYS_PER_MONTH * HOURS_PER_DAY)
        except Exception:
            hourly = 0
        overtime_pay = self.overtime_hours * rules.get("overtime_multiplier", 1.5) * hourly
        
        # Tổng lương gộp
        gross = (
            self.calculate_basic_salary_by_workdays()
            + overtime_pay
            + bonus
            + self.kpi
            + allowance
        )
        
        # Khấu trừ
        bhxh = 0.101 * self.basic_salary
        cong_doan = 0.01 * self.basic_salary
        thue_tncn = 0.05 * self.basic_salary
        phat_di_muon = 2000 * late_minutes
        
        deductions = bhxh + cong_doan + thue_tncn + phat_di_muon + self.tax
        
        return gross - deductions
    

# 5. LÀM THÊM GIỜ (Overtime)
class OvertimeRequest:
    def __init__(self, request_id, employee_id, date, start_time, end_time, reason, request_status="Pending", approver_id=None):
        self.request_id = request_id
        self.employee_id = employee_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.reason = reason
        self.request_status = request_status
        self.approver_id = approver_id
    
    def calculate_overtime_hours(self):
        """Tính số giờ làm thêm"""
        try:
            start = datetime.strptime(self.start_time, "%H:%M")
            end = datetime.strptime(self.end_time, "%H:%M")
            hours = (end - start).seconds / 3600
            return max(0, hours)
        except:
            return 0
    
    def approve(self, approver_id):
        """Duyệt đơn làm thêm"""
        self.approver_id = approver_id
        self.request_status = "Approved"
    
    def reject(self, approver_id):
        """Từ chối đơn làm thêm"""
        self.approver_id = approver_id
        self.request_status = "Rejected"
    
    def is_approved(self):
        """Kiểm tra đã được duyệt chưa"""
        return self.request_status == "Approved"