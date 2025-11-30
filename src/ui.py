from services import *
from models import *
from datetime import datetime, date
import pandas as pd

nv_service = NhanVienService()
dept_service = DepartmentService()
pos_service = PositionService()
att_service = AttendanceService()
ot_service = OvertimeService()
salary_service = SalaryService()

def nhap_khong_trong(label):
    while True:
        val = input(f"{label}: ").strip()
        if val == "":
            print("Không được để trống! Nhập lại.")
            continue
        return val

def nhap_ngay(label):
    while True:
        s = input(f"{label} (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(s, "%Y-%m-%d")
            return s
        except:
            print("Sai định dạng ngày (YYYY-MM-DD). Hãy nhập lại!")

def nhap_float(label):
    while True:
        s = input(f"{label}: ").strip()
        if s == "":
            print("Không được để trống!")
            continue
        try:
            return float(s)
        except:
            print("Giá trị phải là số! Nhập lại.")

# MENU QUẢN LÝ NHÂN VIÊN
def menu_nhan_vien():
    while True:
        print("\n=== QUẢN LÝ NHÂN VIÊN ===")
        print("1. Thêm nhân viên")
        print("2. Danh sách nhân viên")
        print("3. Tìm theo ID")
        print("4. Xóa")
        print("5. Cập nhật")
        print("0. Quay lại")
        ch = input("Chọn: ").strip()

        if ch == "1":
            print("\n--- Thêm nhân viên ---")
            employee_id = nhap_khong_trong("ID")
            ho_ten = nhap_khong_trong("Họ tên")
            ngay_sinh = nhap_ngay("Ngày sinh")
            gioi_tinh = nhap_khong_trong("Giới tính")
            dept_id = nhap_khong_trong("Mã phòng ban")
            position_id = nhap_khong_trong("Mã chức vụ")
            ngay_vao_lam = nhap_ngay("Ngày vào làm")
            email = nhap_khong_trong("Email")
            phone = nhap_khong_trong("SĐT")
            address = nhap_khong_trong("Địa chỉ")

            nv = NhanVien(employee_id, ho_ten, ngay_sinh, gioi_tinh,dept_id, position_id, ngay_vao_lam, email, phone, address)

            nv_service.them_nhan_vien(nv)

        elif ch == "2":
            print("\n--- Danh sách nhân viên ---")
            ds = nv_service.lay_ds_nhan_vien()
            if ds:
                df = pd.DataFrame(ds)
                print(df.to_string(index=False))
            else:
                print("Không có dữ liệu!")

        elif ch == "3":
            eid = nhap_khong_trong("Nhập ID")
            print(nv_service.tim_theo_id(eid))

        elif ch == "4":
            eid = nhap_khong_trong("Nhập ID để xóa")
            nv_service.xoa_nhan_vien(eid)

        elif ch == "5":
            eid = nhap_khong_trong("ID nhân viên cần cập nhật")
            field = nhap_khong_trong("Trường cần sửa")
            value = nhap_khong_trong("Giá trị mới")
            nv_service.cap_nhat_nhan_vien(eid, {field: value})

        elif ch == "0":
            break

        else:
            print("Lựa chọn không hợp lệ!")

# MENU PHÒNG BAN
def menu_phong_ban():
    while True:
        print("\n=== PHÒNG BAN ===")
        print("1. Thêm phòng ban")
        print("2. Danh sách phòng ban")
        print("0. Quay lại")
        ch = input("Chọn: ").strip()

        if ch == "1":
            dept_id = nhap_khong_trong("ID phòng ban")
            name = nhap_khong_trong("Tên phòng ban")
            manager_id = nhap_khong_trong("ID trưởng phòng")
            created_date = nhap_ngay("Ngày tạo")
            budget = nhap_float("Ngân sách")

            dept = Department(dept_id, name, manager_id, created_date, budget)
            dept_service.them_phong_ban(dept)

        elif ch == "2":
            ds = dept_service.lay_ds_phong_ban()
            if ds:
                df = pd.DataFrame(ds)
                print(df.to_string(index=False))
            else:
                print("Không có dữ liệu!")

        elif ch == "0":
            break

        else:
            print("Lựa chọn không hợp lệ!")


# MENU CHỨC VỤ
def menu_chuc_vu():
    while True:
        print("\n=== CHỨC VỤ ===")
        print("1. Thêm chức vụ")
        print("2. Danh sách chức vụ")
        print("0. Quay lại")
        ch = input("Chọn: ").strip()

        if ch == "1":
            pid = nhap_khong_trong("ID chức vụ")
            title = nhap_khong_trong("Tên chức vụ")
            level = nhap_khong_trong("Level")
            min_salary = nhap_float("Lương tối thiểu")
            max_salary = nhap_float("Lương tối đa")

            pos = Position(pid, title, level, min_salary, max_salary)
            pos_service.them_chuc_vu(pos)

        elif ch == "2":
            ds = pos_service.lay_ds_chuc_vu()
            if ds:
                df = pd.DataFrame(ds)
                print(df.to_string(index=False))
            else:
                print("📭 Không có dữ liệu!")

        elif ch == "0":
            break

        else:
            print("Lựa chọn không hợp lệ!")

# MENU CHẤM CÔNG
def menu_cham_cong():
    while True:
        print("\n=== CHẤM CÔNG ===")
        print("1. Check-in")
        print("2. Check-out")
        print("3. Xem chấm công nhân viên")
        print("0. Quay lại")

        ch = input("Chọn: ").strip()

        if ch == "1":
            eid = nhap_khong_trong("ID nhân viên")
            today = str(date.today())
            time_in = nhap_khong_trong("Check-in (HH:MM)")

            a = Attendance("AT" + eid + today, eid, today, time_in, None, "Present")
            att_service.check_in(a)

        elif ch == "2":
            eid = nhap_khong_trong("ID nhân viên")
            today = str(date.today())
            time_out = nhap_khong_trong("Check-out (HH:MM)")

            att_service.check_out(eid, today, time_out)

        elif ch == "3":
            eid = nhap_khong_trong("ID nhân viên")
            ds = att_service.lay_cham_cong(eid)
            if ds:
                df = pd.DataFrame(ds)
                if '_id' in df.columns:
                    df = df.drop('_id', axis=1)
                print(df.to_string(index=False))
            else:
                print("Không có dữ liệu!")

        elif ch == "0":
            break

        else:
            print("Lựa chọn không hợp lệ!")

# ================================
# MENU QUẢN LÝ LƯƠNG (MỚI)
# ================================
def menu_luong():
    while True:
        print("\n=== QUẢN LÝ LƯƠNG ===")
        print("1. Tính lương tháng")
        print("2. Xem bảng lương nhân viên")
        print("0. Quay lại")
        ch = input("Chọn: ").strip()

        if ch == "1":
            eid = nhap_khong_trong("Nhập ID nhân viên")
            
            # 1. Lấy thông tin lương cơ bản từ Chức vụ
            nv = nv_service.tim_theo_id(eid)
            if not nv:
                print("Không tìm thấy nhân viên!")
                continue

            # 2. Quét dữ liệu chấm công để đếm ngày công và phút muộn
            thang = nhap_khong_trong("Nhập tháng (MM)")
            nam = nhap_khong_trong("Nhập năm (YYYY)")
            
            ds_cc = att_service.lay_cham_cong(eid)
            ngay_cong = 0
            tong_muon = 0
            
            for cc in ds_cc:
                # cc['date'] dạng YYYY-MM-DD
                y, m, d = cc['date'].split('-')
                if y == nam and m == thang and cc.get('check_out'):
                    ngay_cong += 1
                    tong_muon += cc.get('late_minutes', 0)

            print(f"📊 Thống kê: {ngay_cong} ngày công, {tong_muon} phút đi muộn.")

            # 3. Nhập các chỉ số khác
            ot_hours = nhap_float("Số giờ OT")
            bonus = nhap_float("Thưởng")
            kpi = nhap_float("Thưởng KPI")
            allowance = nhap_float("Phụ cấp")

            # 4. Tính toán
            salary_id = f"SAL-{eid}-{nam}{thang}"
            rec = SalaryRecord(salary_id, eid, int(thang), int(nam), ngay_cong, ot_hours, bonus, kpi, allowance, tax=0)
            
            gross = rec.calculate_gross_salary()
            net = rec.calculate_net_salary(tong_muon) # Trừ tiền phạt đi muộn ở đây

            print("-" * 30)
            print(f"💰 LƯƠNG THÁNG {thang}/{nam}")
            print(f"   Lương Gross: {gross:,.0f}")
            print(f"   Phạt đi muộn: -{tong_muon * 2000:,.0f}")
            print(f"   Lương NET:   {net:,.0f}")
            print("-" * 30)

            if input("Lưu bảng lương? (y/n): ").lower() == 'y':
                salary_service.luu_bang_luong(rec)

        elif ch == "2":
            eid = nhap_khong_trong("Nhập ID nhân viên")
            ds = salary_service.lay_luong_nhan_vien(eid)
            if ds:
                df = pd.DataFrame(ds)
                if '_id' in df.columns:
                    df = df.drop('_id', axis=1)
                print(df.to_string(index=False))
            else:
                print("Không có dữ liệu!")

        elif ch == "0":
            break

# MENU CHÍNH
def menu_chinh():
    while True:
        print("\n===== MENU CHÍNH =====")
        print("1. Quản lý nhân viên")
        print("2. Quản lý phòng ban")
        print("3. Quản lý chức vụ")
        print("4. Quản lý lương")
        print("5. Chấm công")
        print("0. Thoát")
        ch = input("Chọn: ").strip()

        if ch == "1": menu_nhan_vien()
        elif ch == "2": menu_phong_ban()
        elif ch == "3": menu_chuc_vu()
        elif ch == "4": menu_luong()
        elif ch == "5": menu_cham_cong()
        elif ch == "0": break
        else: print("Lựa chọn không hợp lệ!")