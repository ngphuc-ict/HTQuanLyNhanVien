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
        print("4. Tìm theo tên")
        print("5. Xóa")
        print("6. Cập nhật")
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
                df = df.drop(columns= '_id')
                df = df.rename(columns={'employee_id': 'ID', 'ho_ten': 'Họ Tên', 'ngay_sinh': 'Ngày Sinh', 'gioi_tinh': 'Giới Tính', 'dept_id': 'Phòng Ban', 'position_id': 'Chức Vụ', 'ngay_vao_lam': 'Ngày Vào Làm', 'email': 'Email', 'phone': 'SĐT', 'address': 'Địa Chỉ', 'status': 'Trạng Thái'})
                print(df)
            else:
                print("Không có dữ liệu!")

        elif ch == "3":
            eid = nhap_khong_trong("Nhập ID")
            result = nv_service.tim_theo_id(eid)
            if result:
                df = pd.DataFrame(result)
                df = df.drop(columns='_id')
                df = df.rename(columns={'employee_id': 'ID', 'ho_ten': 'Họ Tên', 'ngay_sinh': 'Ngày Sinh', 'gioi_tinh': 'Giới Tính', 'dept_id': 'Phòng Ban', 'position_id': 'Chức Vụ', 'ngay_vao_lam': 'Ngày Vào Làm', 'email': 'Email', 'phone': 'SĐT', 'address': 'Địa Chỉ', 'status': 'Trạng Thái'})
                print(df)
            else:
                print("Không tìm thấy nhân viên với ID này!")
        
        elif ch == "4":
            name = nhap_khong_trong("Nhập tên")
            result = nv_service.tim_theo_ten(name)
            if result:
                df = pd.DataFrame(result)
                df = df.drop(columns='_id')
                df = df.rename(columns={'employee_id': 'ID', 'ho_ten': 'Họ Tên', 'ngay_sinh': 'Ngày Sinh', 'gioi_tinh': 'Giới Tính', 'dept_id': 'Phòng Ban', 'position_id': 'Chức Vụ', 'ngay_vao_lam': 'Ngày Vào Làm', 'email': 'Email', 'phone': 'SĐT', 'address': 'Địa Chỉ', 'status': 'Trạng Thái'})
                print(df)
            else:
                print("Không tìm thấy nhân viên với tên này!")
        elif ch == "5":
            eid = nhap_khong_trong("Nhập ID để xóa")
            nv_service.xoa_nhan_vien(eid)

        elif ch == "6":
            eid = nhap_khong_trong("ID nhân viên cần cập nhật")
            field = nhap_khong_trong("Cột cần sửa")
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
        print("3. Thống kê số nhân viên theo phòng ban")
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
                df = df.drop(columns= '_id')
                df = df.rename(columns={'dept_id': 'ID Phòng Ban', 'name': 'Tên Phòng Ban', 'manager_id': 'Trưởng Phòng', 'created_date': 'Ngày Tạo', 'budget': 'Ngân Sách'})
                print(df)
            else:
                print("Không có dữ liệu!")

        elif ch == "3":
            ds_dept = dept_service.lay_ds_phong_ban()
            ds_nv = nv_service.lay_ds_nhan_vien()
            if ds_dept:
                print("\n--- Thống kê số nhân viên theo phòng ban ---")
                for d in ds_dept:
                    count = dept_service.dem_so_nhan_vien(d['dept_id'], ds_nv)
                    manager_name = dept_service.thong_tin_truong_phong(d['manager_id'], ds_nv)
                    print(f"Phòng ban: {d['name']} | Số nhân viên: {count} | Trưởng phòng: {manager_name}")
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
                df = df.drop(columns= '_id')
                df = df.rename(columns={'position_id': 'ID Chức Vụ', 'title': 'Tên Chức Vụ', 'level': 'Level', 'min_salary': 'Lương Tối Thiểu', 'max_salary': 'Lương Tối Đa'})
                print(df)
            else:
                print("Không có dữ liệu!")

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
            
            # Tạo bản ghi attendance và gọi mark_check_in() - tự động lấy thời gian hiện tại
            a = Attendance("AT" + eid + today, eid, today)
            try:
                a.mark_check_in()
                att_service.check_in(a)
                print(f" Check-in thành công lúc {a.check_in.strftime('%H:%M:%S')}")
            except ValueError as e:
                print(f" Lỗi: {e}")

        elif ch == "2":
            eid = nhap_khong_trong("ID nhân viên")
            today = str(date.today())
            
            # Lấy danh sách attendance của nhân viên, tìm bản ghi hôm nay
            try:
                ds = att_service.lay_cham_cong(eid)
                # Tìm bản ghi với date=today
                record = None
                for r in ds:
                    if r.get("date") == today:
                        record = r
                        break
                
                if not record:
                    print("✗ Không tìm thấy bản ghi check-in hôm nay!")
                else:
                    # Tạo object Attendance từ bản ghi
                    a = Attendance(
                        record["attendance_id"],
                        record["employee_id"],
                        record["date"]
                    )
                    # Chuyển đổi chuỗi check_in thành đối tượng datetime
                    if record.get("check_in"):
                        a.check_in = datetime.strptime(record["check_in"], "%Y-%m-%d %H:%M:%S")
                    
                    # Gọi mark_check_out() - tự động lấy thời gian hiện tại
                    a.mark_check_out()
                    
                    # Cập nhật vào DB
                    att_service.col.update_one(
                        {"_id": record["_id"]},
                        {"$set": {
                            "check_out": a.check_out.strftime("%Y-%m-%d %H:%M:%S"),
                            "late_minutes": a.late_minutes,
                            "leave_minutes": a.leave_minutes,
                            "status": "Completed"
                        }}
                    )
                    
                    print(f" Check-out thành công lúc {a.check_out.strftime('%H:%M:%S')}")
                    print(f"  Muộn: {a.late_minutes} phút")
                    print(f"  Về sớm: {a.leave_minutes} phút")
                    print(f"  Giờ làm: {a.calculate_working_hours()} giờ")
            except ValueError as e:
                print(f" Lỗi: {e}")
            except Exception as e:
                print(f" Lỗi không mong muốn: {e}")

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

# MENU QUẢN LÝ LƯƠNG
def menu_luong():
    while True:
        print("\n=== QUẢN LÝ LƯƠNG ===")
        print("1. Tính lương tháng")
        print("2. Xem bảng lương nhân viên")
        print("0. Quay lại")
        ch = input("Chọn: ").strip() # Dòng này định nghĩa biến 'ch' (Khắc phục NameError)

        if ch == "1":
            eid = nhap_khong_trong("Nhập ID nhân viên")
            
            # 1. Lấy thông tin LƯƠNG CƠ BẢN và CHỨC VỤ
            nv_data = nv_service.tim_theo_id(eid)
            if not nv_data:
                print("Không tìm thấy nhân viên!")
                continue

            # Lấy thông tin nhân viên (chỉ lấy phần tử đầu tiên)
            nv = nv_data[0]
            
            # Lấy thông tin Chức vụ để tìm Lương cơ bản
            ds_cv = pos_service.lay_ds_chuc_vu()
            
            basic_salary = 0.0
            position_title = "Nhân viên" # Default position title
            
            for cv in ds_cv:
                if cv['position_id'] == nv['position_id']:
                    basic_salary = cv.get('min_salary', 0.0)
                    position_title = cv.get('title', "Nhân viên")
                    break
            
            if basic_salary == 0.0:
                print(f"Không tìm thấy Lương tối thiểu cho chức vụ: {nv['position_id']}! Dùng lương cơ bản = 0.")

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
                    # Sử dụng trực tiếp late_minutes đã tính và lưu trong DB
                    tong_muon += cc.get('late_minutes', 0)
                    ngay_cong += 1

            print(f"📊 Thống kê: {ngay_cong} ngày công, {tong_muon} phút đi muộn. Lương cơ bản: {basic_salary:,.0f} VNĐ")

            # 3. Nhập các chỉ số khác
            ot_hours = nhap_float("Số giờ OT")
            bonus_extra = nhap_float("Thưởng (nhập thêm)") 
            kpi = nhap_float("Thưởng KPI")
            allowance_extra = nhap_float("Phụ cấp (nhập thêm)") 

            # 4. Tính toán
            salary_id = f"SAL-{eid}-{nam}{thang}"
            rec = SalaryRecord(salary_id, eid, int(thang), int(nam), ngay_cong, ot_hours, bonus_extra, kpi, allowance_extra, tax=0)
            
            # Tính Lương Net bằng cách truyền Lương cơ bản, Chức vụ và phút muộn
            net = rec.calculate_net_salary(basic_salary, position_title, tong_muon) 
            gross = rec.gross_salary
            
            print("-" * 30)
            print(f"   LƯƠNG THÁNG {thang}/{nam} ({position_title})")
            print(f"   Lương Cơ Bản: {basic_salary:,.0f}")
            print(f"   Lương Gross: {gross:,.0f}")
            print(f"   Phạt đi muộn: -{tong_muon * PHAT_DI_MUON_MOT_PHUT:,.0f}")
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
        
        else:
            print("Lựa chọn không hợp lệ!")

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