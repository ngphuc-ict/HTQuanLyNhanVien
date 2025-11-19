from database import get_database
from models import *
from datetime import datetime, date

class NhanVienService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["nhanvien"]

    def them_nhan_vien(self, nv: NhanVien):
       
        data = nv.__dict__.copy()
        
        # CHUYỂN ĐỔI DATE/DATETIME SANG CHUỖI AN TOÀN TRƯỚC KHI INSERT
        for key, value in data.items():
            if isinstance(value, (datetime, date)):
                data[key] = value.isoformat()
        
       
        self.col.insert_one(nv.__dict__)
        print("Thêm nhân viên thành công!")

    def lay_ds_nhan_vien(self):
        return list(self.col.find())

    def tim_theo_id(self, employee_id):
        return self.col.find_one({"employee_id": employee_id})

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
  
        data = dept.__dict__.copy()

        # CHUYỂN ĐỔI DATE/DATETIME SANG CHUỖI AN TOÀN TRƯỚC KHI INSERT
        for key, value in data.items():
            if isinstance(value, (datetime, date)):
                data[key] = value.isoformat()
        self.col.insert_one(dept.__dict__)
        print("Thêm phòng ban thành công!")

    def lay_ds_phong_ban(self):
        return list(self.col.find())


class PositionService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["chucvu"]

    def them_chuc_vu(self, pos: Position):
        self.col.insert_one(pos.__dict__)
        print("Thêm chức vụ thành công!")

    def lay_ds_chuc_vu(self):
        return list(self.col.find())


class AttendanceService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["chamcong"]

    def check_in(self, attendance: Attendance):
        self.col.insert_one(attendance.__dict__)
        print("Check-in thành công!")

    def check_out(self, employee_id, date, check_out_time):
        self.col.update_one(
            {"employee_id": employee_id, "date": date},
            {"$set": {"check_out": check_out_time}}
        )
        print("Check-out thành công!")

    def lay_cham_cong(self, employee_id):
        return list(self.col.find({"employee_id": employee_id}))


class OvertimeService:
    def __init__(self):
        self.db = get_database()
        self.col = self.db["overtime"]

    def gui_don_ot(self, ot: OvertimeRequest):
        self.col.insert_one(ot.__dict__)
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
        self.col.insert_one(salary.__dict__)
        print("Lưu bảng lương thành công!")

    def lay_luong_nhan_vien(self, employee_id):
        return list(self.col.find({"employee_id": employee_id}))
