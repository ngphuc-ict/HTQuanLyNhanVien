from database import get_database
from models import *
from datetime import datetime, date

class NhanVienService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["nhanvien"]

    def them_nhan_vien(self, nv: NhanVien):

        return
        data = vars(nv).copy()
        for key, value in data.items():
            if isinstance(value, date):
                data[key] = value.isoformat()

        self.col.insert_one(data)
        print("Thêm nhân viên thành công!")

    def hien_thi_thong_tin(self, employee):
        print("----- THÔNG TIN NHÂN VIÊN -----")
        print("ID:", employee['employee_id'])
        print("Họ tên:", employee['ho_ten'])
        print("Giới tính:", employee['gioi_tinh'])
        print("Ngày sinh:", employee['ngay_sinh'])
        print("Phòng ban:", employee['dept_id'])
        print("Chức vụ:", employee['position_id'])
        print("Ngày vào làm:", employee['ngay_vao_lam'])
        print("Email:", employee['email'])
        print("SĐT:", employee['phone'])
        print("Địa chỉ:", employee['address'])
        print("Trạng thái:", employee['status'])

    def lay_ds_nhan_vien(self):
        return list(self.col.find())

    def tim_theo_id(self, employee_id):
        return list(self.col.find({"employee_id": employee_id}))

    def tim_theo_ten(self, name):
        employees = list(self.col.find())
        result = []
        for e in employees:
            if name.lower() in e['ho_ten'].lower():
                result.append(e)
        return result

    def xoa_nhan_vien(self, employee_id):
        self.col.delete_one({"employee_id": employee_id})
        print("Xóa nhân viên thành công!")

    def cap_nhat_nhan_vien(self, employee_id, data_update):
        self.col.update_one({"employee_id": employee_id}, {"$set": data_update})
        print("Cập nhật thành công!")


class DepartmentService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["phongban"]

    def them_phong_ban(self, dept: Department):
  
        data = vars(dept).copy()
        for key, value in data.items():
            if isinstance(value, date):
                data[key] = value.isoformat()
        self.col.insert_one(data)
        print("Thêm phòng ban thành công!")

    def lay_ds_phong_ban(self):
        return list(self.col.find())
    
    def dem_so_nhan_vien(self, dept_id, employees):
        count = 0
        for e in employees:
            if e['dept_id'] == dept_id:
                count += 1
        return count

    def thong_tin_truong_phong(self, manager_id, employees):
        for e in employees:
            if e['employee_id'] == manager_id:
                return e['ho_ten']
        return "Không tìm thấy"


class PositionService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["chucvu"]

    def them_chuc_vu(self, pos: Position):
        self.col.insert_one(vars(pos))
        print("Thêm chức vụ thành công!")

    def lay_ds_chuc_vu(self):
        return list(self.col.find())


class AttendanceService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["chamcong"]

    def check_in(self, attendance: Attendance):
        self.col.insert_one(vars(attendance))
        print("Check-in thành công!")

    def check_out(self, employee_id, date_str, check_out_time):
        # 1. Lấy dữ liệu check-in cũ
        record = self.col.find_one({"employee_id": employee_id, "date": date_str})
        if not record:
            print("Không tìm thấy dữ liệu Check-in!")
            return

        # 2. Tạo object để tính toán
        att = Attendance(
            attendance_id=record["attendance_id"],
            employee_id=record["employee_id"],
            date=record["date"],
            check_in=record["check_in"]
        )

        # 3. Tính toán đi muộn/về sớm
        try:
            att.compute_late_and_early(check_out_time)
        except Exception as e:
            print(f"Lỗi tính toán: {e}")
            return

        # 4. Cập nhật kết quả vào DB
        self.col.update_one(
            {"_id": record["_id"]},
            {"$set": {
                "check_out": check_out_time,
                "late_minutes": att.late_minutes,
                "leave_minutes": att.leave_minutes,
                "status": "Completed"
            }}
        )
        print(f"Check-out xong! Đi muộn: {att.late_minutes}p, Về sớm: {att.leave_minutes}p")

    def lay_cham_cong(self, employee_id):
        return list(self.col.find({"employee_id": employee_id}))


class OvertimeService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["overtime"]

    def gui_don_ot(self, ot: OvertimeRequest):
        self.col.insert_one(vars(ot))
        print("Gửi đơn OT thành công!")

    def duyet_ot(self, request_id, approver_id, status):
        self.col.update_one(
            {"request_id": request_id},
            {"$set": {"request_status": status, "approver_id": approver_id}}
        )
        print("Đã cập nhật trạng thái đơn OT!")


class SalaryService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["luong"]

    def luu_bang_luong(self, salary: SalaryRecord):
        self.col.insert_one(vars(salary))
        print("Lưu bảng lương thành công!")

    def lay_luong_nhan_vien(self, employee_id):
        return list(self.col.find({"employee_id": employee_id}))
