
from datetime import *
from datetime import datetime, timedelta

# Cấu hình mặc định cho tính lương
WORKDAYS_PER_MONTH = 26
HOURS_PER_DAY = 8
PHAT_DI_MUON_MOT_PHUT = 2000 # Hằng số phạt đi muộn (2000 VNĐ/phút)
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

# NHÂN VIÊN
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

# PHÒNG BAN
class Department:
    def __init__(self, dept_id, name, manager_id, created_date, budget):
        self.dept_id = dept_id
        self.name = name
        self.manager_id = manager_id
        self.created_date = created_date
        self.budget = budget

# CHỨC VỤ

class Position:
    def __init__(self, position_id, title, level, min_salary, max_salary):
        self.position_id = position_id
        self.title = title
        self.level = level
        self.min_salary = min_salary
        self.max_salary = max_salary

# 4. CHẤM CÔNG
class Attendance:
    # Định nghĩa ca mặc định
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
        self.status = "Absent"
        self.late_minutes = 0
        self.leave_minutes = 0

    def mark_check_in(self):
        """Check-in tự động lấy giờ hiện tại (chỉ nhận nút bấm, không nhập thủ công)"""
        if self.check_in:
            raise ValueError("Check-in đã tồn tại")
        # Kiểm tra ngày hiện tại khớp với self.date
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.date:
            raise ValueError(f"Ngày không khớp: hôm nay là {today} nhưng record cho ngày {self.date}")
        self.check_in = datetime.now()
        self.status = "Present"

    def mark_check_out(self):
        """Check-out tự động lấy giờ hiện tại và tính muộn/về sớm (chỉ nhận nút bấm, không nhập thủ công)"""
        if not self.check_in:
            raise ValueError("Chưa check-in")
        if self.check_out:
            raise ValueError("Check-out đã tồn tại")
        # Kiểm tra ngày hiện tại khớp với self.date
        today = datetime.now().strftime("%Y-%m-%d")
        if today != self.date:
            raise ValueError(f"Ngày không khớp: hôm nay là {today} nhưng record cho ngày {self.date}")
        self.check_out = datetime.now()
        self._compute_late_and_early()

    def detect_shift(self):
        """Xác định ca dựa trên giờ check-in"""
        if not self.check_in:
            return "morning"
        time_only = self.check_in.time()
        for name, s in self.SHIFTS.items():
            start = datetime.strptime(s["start"], "%H:%M").time()
            end = datetime.strptime(s["end"], "%H:%M").time()
            if start <= time_only <= end:
                return name
        return "morning"

    def _compute_late_and_early(self):
        """Tính số phút đi muộn và về sớm theo ca"""
        shift = self.detect_shift()
        s = self.SHIFTS[shift]
        shift_start = datetime.combine(datetime.strptime(self.date, "%Y-%m-%d").date(),
                                       datetime.strptime(s["start"], "%H:%M").time())
        shift_end = datetime.combine(datetime.strptime(self.date, "%Y-%m-%d").date(),
                                     datetime.strptime(s["end"], "%H:%M").time())

        self.late_minutes = max(0, int((self.check_in - shift_start).total_seconds() // 60))
        self.leave_minutes = max(0, int((shift_end - self.check_out).total_seconds() // 60))

    def calculate_working_hours(self):
        """Tính tổng số giờ làm việc"""
        if not self.check_in or not self.check_out:
            return 0.0
        diff = self.check_out - self.check_in
        return round(diff.total_seconds() / 3600, 2)

    def to_dict(self):
        """Xuất dữ liệu dạng dictionary"""
        return {
            "attendance_id": self.attendance_id,
            "employee_id": self.employee_id,
            "date": self.date,
            "check_in": self.check_in.strftime("%Y-%m-%d %H:%M:%S") if self.check_in else "",
            "check_out": self.check_out.strftime("%Y-%m-%d %H:%M:%S") if self.check_out else "",
            "working_hours": self.calculate_working_hours(),
            "late_minutes": self.late_minutes,
            "leave_minutes": self.leave_minutes,
            "status": self.status
        }



# ===============================
# 6. BẢNG LƯƠNG
# ===============================

class SalaryRecord:
    def __init__(self, salary_id, employee_id, month, year,
                 working_days, overtime_hours, bonus, kpi, allowance, tax): # Đã sửa constructor
        self.salary_id = salary_id
        self.employee_id = employee_id
        self.month = month
        self.year = year
        self.working_days = working_days
        self.overtime_hours = overtime_hours
        self.bonus = bonus # Thưởng nhập thêm
        self.kpi = kpi
        self.allowance = allowance # Phụ cấp nhập thêm
        self.tax = tax  # thuế khác nếu có
        self.gross_salary = 0.0
        self.deductions = 0.0
        self.net_salary = 0.0
        
    # Đổi tên hàm và thêm tham số basic_salary, position vào hàm tính toán
    def calculate_net_salary(self, basic_salary, position, late_minutes):
        rules = POSITION_RULES.get(position, POSITION_RULES["Nhân viên"]) # Lấy rules theo position
        
        # 1. Tính Lương Gross
        
        # Lương theo ngày công (Giả định basic_salary là lương trọn gói/tháng)
        try:
            salary_by_workdays = (basic_salary / WORKDAYS_PER_MONTH) * self.working_days
        except Exception:
            salary_by_workdays = 0

        # Phụ cấp và thưởng cố định theo quy tắc
        allowance_by_rule = rules.get("allowance_rate", 0) * basic_salary
        bonus_by_rule = rules.get("bonus_rate", 0) * basic_salary
        
        # Overtime theo quy tắc
        try:
            hourly_rate = basic_salary / (WORKDAYS_PER_MONTH * HOURS_PER_DAY)
        except Exception:
            hourly_rate = 0
            
        overtime_pay = self.overtime_hours * rules.get("overtime_multiplier", 1.5) * hourly_rate
        
        # Tổng lương Gross
        gross = (
            salary_by_workdays
            + overtime_pay
            + bonus_by_rule
            + self.kpi  # Thưởng KPI nhập tay
            + allowance_by_rule # Phụ cấp theo quy tắc
            + self.allowance # Phụ cấp nhập tay khác
            + self.bonus # Thưởng nhập tay khác
        )
        
        # 2. Tính Khấu trừ
        
        # Các khoản khấu trừ cố định (tính trên basic_salary)
        bhxh = 0.101 * basic_salary
        cong_doan = 0.01 * basic_salary
        thue_tncn = 0.05 * basic_salary
        
        # Phạt
        phat_di_muon = PHAT_DI_MUON_MOT_PHUT * late_minutes
        
        deductions = bhxh + cong_doan + thue_tncn + phat_di_muon + self.tax
        
        self.gross_salary = gross
        self.deductions = deductions
        self.net_salary = gross - deductions
        
        return self.net_salary
    

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