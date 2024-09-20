from flask import request, render_template, url_for, session, redirect, current_app
from app_school.xu_ly.Xu_ly_Form import *
from app_school.xu_ly.lop_hoc.XL_Lop_hoc import lay_nien_khoa_theo_lop, cap_nhat_si_so
from app_school.xu_ly.giao_vien.XL_Giao_vien import Profile_Giao_Vien
from app_school.xu_ly.bang_diem.XL_Bang_diem import tao_bang_diem_cho_hoc_sinh, doc_bang_diem_theo_hoc_sinh
from app_school.xu_ly.hoc_sinh.XL_Hoc_sinh import Profile_hoc_sinh
from app_school.xu_ly.lop_hoc.XL_Lop_hoc import doc_danh_sach_lop_hoc, doc_danh_sach_lop_hoc_theo_giao_vien
from app_school.xu_ly.Xu_ly_Model import HocSinh, Lop
from app_school.xu_ly.hoc_sinh.XL_Hoc_sinh import *
from app_school.xu_ly.quan_li.xu_ly_doc_lien_he import *
from app_school import app, db_session
from datetime import date
from flask_mail import Mail , Message
import os
import uuid
import json
@app.route("/quan-li" , methods = ['GET','POST'])
def trang_quan_li() :
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    quanli = session['quanli']
    message = ''
    quan_li = Profile_Quan_li(quanli)
    if request.args.get('message'):
        message = request.args.get('message')
        print(message)
    return render_template('quan_ly/thong_tin_quan_li.html',quan_li=quan_li,message=message)


@app.route("/quan-li/doc-lien-he" , methods = ['GET','POST'])
def trang_doc_lien_he() :
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    Danh_sach_lh = Doc_danh_sach_lh()
    form = Form_Feedback()
    return render_template("quan_ly/doc_lien_he.html" , Danh_sach_lh=Danh_sach_lh)

@app.route("/quan-li/doc-lien-he/<string:Chuoi_tra_cuu>/" , methods=['GET','POST'])
def trang_tra_loi_lien_he(Chuoi_tra_cuu) :
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    danh_sach = Doc_danh_sach_lh()
    danh_sach_chon = Lay_info_theo_Email(Chuoi_tra_cuu , danh_sach)
    noi_dung = ""
    if request.form.get("Th_noi_dung") :
        noi_dung = request.form.get("Th_noi_dung")

        app.config['MAIL_SERVER'] = "smtp.gmail.com"
        app.config['MAIL_PORT'] = 465
        app.config['MAIL_USERNAME'] = 'thanhhoa6621@gmail.com'    #Muốn test thì thay email vào nhe
        app.config['MAIL_PASSWORD'] = 'password'                #Pass email
        app.config['MAIL_USE_TLS'] = False  
        app.config['MAIL_USE_SSL'] = True
        mail = Mail(app)

        msg = Message("Thông tin liên hệ", sender='thanhhoa6621@gmail.com', recipients=[Chuoi_tra_cuu])
        msg.body= "Kính chào " + danh_sach_chon['Người gửi'] + "\nChúng tôi đã nhận được liên hệ của bạn với nội dung " + danh_sach_chon['Nội dung'] + "\n Chúng tôi đã có những hồi đáp như sau : " + noi_dung
        mail.send(msg)

    return render_template("quan_ly/tra_loi_lien_he.html" ,danh_sach_chon=danh_sach_chon)


@app.route("/quan-li/tao-tai-khoan" , methods=['GET','POST'])
def trang_tao_tai_khoan() :
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    id_giao_vien = ""
    ten_dang_nhap = ""
    mat_khau = ""
    ho_ten = ""
    email = ""
    Danh_sach = []
    if request.form.get('Th_Ten_dang_nhap') :
        ten_dang_nhap = request.form.get('Th_Ten_dang_nhap')
        mat_khau = request.form.get('Th_Mat_khau')
        ho_ten = request.form.get('Th_Ho_va_ten')
        email = request.form.get('Th_email')
        Danh_sach.append(ten_dang_nhap)
        Danh_sach.append(mat_khau)
        Danh_sach.append(ho_ten)
        Danh_sach.append(email)
        Them_tai_khoan(Danh_sach)
    return render_template("quan_ly/tao_tai_khoan.html")

@app.route("/quan-li/tao-tai-khoan-hs" , methods=['GET','POST'])
def trang_tao_tai_khoan_hs() :
    if session.get("quanli") == None:
        return redirect(url_for('login'))

    id_hoc_sinh = ""
    mat_khau = ""
    ho_ten = ""
    email = ""
    id_lop = ""
    id_nien_khoa = ""
    Danh_sach = []
    if request.form.get('Th_Id_hoc_sinh') :
        id_hoc_sinh = request.form.get('Th_Id_hoc_sinh')
        mat_khau = request.form.get('Th_Mat_khau')
        ho_ten = request.form.get('Th_Ho_va_ten')
        email = request.form.get('Th_email')
        id_lop = request.form.get('Th_Lop')
        id_nien_khoa = request.form.get('Th_Nien_khoa')
        Danh_sach.append(id_hoc_sinh)
        Danh_sach.append(mat_khau)
        Danh_sach.append(ho_ten)
        Danh_sach.append(email)
        Danh_sach.append(id_lop)
        Danh_sach.append(id_nien_khoa)
        Them_tai_khoan_HS(Danh_sach)
    return render_template("quan_ly/tao_tai_khoan_hs.html")

@app.route('/quan-li/doi-mat-khau', methods=['GET', 'POST'])
def doi_mat_khau_ql():
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    quanli = session['quanli']
    
    ql = Profile_Quan_li(quanli)
    ThongBao = ""
    form = Form_Reset_pw()

    if form.validate_on_submit():
        MatkhauCu = request.form['Th_MatkhauCu']
        MatkhauMoi = request.form['Th_MatkhauMoi']
        ThongBao = hs_doi_mat_khau(quanli, MatkhauCu, MatkhauMoi)
        if ThongBao == "Đổi Mật Khẩu Thành Công":
            return redirect(url_for('trang_quan_li', message='Đổi mật khẩu thành công'))
    return render_template('quan_ly/doi_mat_khau.html', form=form, ThongBao=ThongBao)

@app.route('/quan-li/sua-quan-li', methods=['GET','POST'])
def cap_nhat_quan_li():
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    error = ''
    quanli = session['quanli']
    quan_li = Profile_Quan_li(quanli)
    form = Form_Update_Ql()
    if form.validate_on_submit():
        HoVaTen = request.form['Th_Ho_ten']
        GioiTinh = request.form['Th_Gioi_tinh']
        NgaySinh = request.form['Th_Ngay_sinh']
        DiaChi = request.form['Th_Dia_chi']
        Email = request.form['Th_Email']
        SoDienThoai = request.form['Th_Sdt']

        ql = {"HoVaTen": HoVaTen, "GioiTinh": GioiTinh, "NgaySinh": NgaySinh, "Email": Email, "DiaChi": DiaChi,
              "SoDienThoai": SoDienThoai}

        value = db_session.query(QuanLi).filter(
            QuanLi.TenDangNhap == quanli).first()

        value.HoVaTen = ql['HoVaTen']
        value.GioiTinh = ql['GioiTinh']
        value.NgaySinh = datetime.strptime(ql['NgaySinh'], '%Y-%m-%d').date()
        value.Email = ql['Email']
        value.DiaChi = ql['DiaChi']
        value.SoDienThoai = ql['SoDienThoai']
        db_session.flush()
        db_session.commit()
        return redirect(url_for('trang_quan_li', message='Cập nhật thành công'))

    form.Th_Gioi_tinh.default = quan_li['GioiTinh']
    form.process()
    return render_template('quan_ly/cap_nhat_thong_tin.html', quan_li=quan_li, form=form, error=error)

@app.route("/quan-li/xem-tai-khoan-gv",methods=['GET','POST'])
def trang_xem_tai_khoan() :
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    Danh_sach_gv = Doc_danh_sach_gv()
    return render_template("quan_ly/xem_tai_khoan_gv.html", Danh_sach_gv=Danh_sach_gv)

@app.route("/quan-li/xem-tai-khoan-gv/<string:Chuoi_Tra_cuu>/",methods=['GET','POST'])
def trang_xem_tai_khoan_chon(Chuoi_Tra_cuu) :
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    Danh_sach_gv = Doc_danh_sach_gv()
    Danh_sach_gv_chon = Lay_info_theo_TK(Chuoi_Tra_cuu,Danh_sach_gv)
    return render_template("quan_ly/xem_tai_khoan_gv_chon.html", Danh_sach_gv_chon=Danh_sach_gv_chon)

@app.route("/quan-li/xem-tai-khoan-hs",methods=['GET','POST']) #
def trang_xem_tai_khoan_hs() :
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    Danh_sach_hs = Doc_danh_sach_hs()
    return render_template("quan_ly/xem_tai_khoan_hs.html", Danh_sach_hs=Danh_sach_hs)

@app.route("/quan-li/xem-tai-khoan-hs/<string:Chuoi_Tra_cuu>/",methods=['GET','POST'])
def trang_xem_tai_khoan_hs_chon(Chuoi_Tra_cuu) :
    if session.get("quanli") == None:
        return redirect(url_for('login'))
    Danh_sach_hs = Doc_danh_sach_hs()
    Danh_sach_hs_chon = Lay_info_theo_ID(Chuoi_Tra_cuu,Danh_sach_hs)
    return render_template("quan_ly/xem_tai_khoan_hs_chon.html", Danh_sach_hs_chon=Danh_sach_hs_chon)

@app.route("/quan-li/xem-cac-lop" , methods = ['GET','POST'])
def trang_them_tkb() :
    danh_sach_lop = doc_danh_sach_lop_hoc()
    return render_template("quan_ly/xem_cac_lop.html",danh_sach_lop=danh_sach_lop)

@app.route('/quan-li/dang-xuat', methods=['GET', 'POST'])
def dang_xuat_ql():
    if session.get("quanli") != None:
        session.pop("quanli", None)
    return redirect('/')

@app.route("/quan-li/dang-bai", methods=['GET', 'POST'])
def dang_bai():
    if session.get("quanli") is None:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        tieu_de = request.form.get('title', '')
        noi_dung = request.form.get('content', '')
        
        if tieu_de and noi_dung:
            files = request.files.getlist('files')
            has_files = any(file and file.filename for file in files)
            
            bai_dang_id = str(uuid.uuid4())
            if has_files:
                bai_dang_id += "_file_uploaded"
            
            bai_dang = {
                'id': bai_dang_id,
                'tieu_de': tieu_de,
                'noi_dung': noi_dung,
                'ngay_dang': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            bai_dang_file = os.path.join(current_app.root_path, './du_lieu/bai_dang.json')
            
            try:
                if os.path.exists(bai_dang_file):
                    with open(bai_dang_file, 'r', encoding='utf-8') as f:
                        bai_dang_list = json.load(f)
                else:
                    bai_dang_list = []
                
                bai_dang_list.append(bai_dang)
                
                with open(bai_dang_file, 'w', encoding='utf-8') as f:
                    json.dump(bai_dang_list, f, indent=4, ensure_ascii=False)
                
                print(f"Bài đăng mới đã được lưu: {tieu_de}")  
                
                for file in files:
                    if file and file.filename:
                        file_extension = os.path.splitext(file.filename)[1]
                        if file_extension.lower() in ['.jpg', '.png', '.jpeg', '.gif', '.bmp']:
                            folder = 'images'
                        elif file_extension.lower() == '.pdf':
                            folder = 'pdf'
                        elif file_extension.lower() == '.docx':
                            folder = 'words'
                        elif file_extension.lower() == '.txt':
                            folder = 'txt'
                        elif file_extension.lower() in ['.mp4', '.avi', '.mkv']:
                            folder = 'videos'
                        else:
                            folder = 'cac_file_khac'
                        folder_path = os.path.join(current_app.root_path, f'./du_lieu/files_upload/{folder}')
                        if not os.path.exists(folder_path):
                            os.makedirs(folder_path)
                        new_filename = f"{bai_dang['id']}{file_extension}"
                        file_path = os.path.join(folder_path, new_filename)
                        file.save(file_path)
                        print(f"File {new_filename} đã được lưu vào {folder_path}")
                
                # Xóa các file không còn liên kết với bài đăng nào
                for folder in ['images', 'pdf', 'words', 'txt', 'videos', 'cac_file_khac']:
                    folder_path = os.path.join(current_app.root_path, f'./du_lieu/files_upload/{folder}')
                    if os.path.exists(folder_path):
                        for file_name in os.listdir(folder_path):
                            file_id = os.path.splitext(file_name)[0]
                            if not any(bai_dang['id'] == file_id for bai_dang in bai_dang_list):
                                file_path = os.path.join(folder_path, file_name)
                                try:
                                    os.remove(file_path)
                                    print(f"Đã xóa file {file_name} từ {folder_path}")
                                except Exception as e:
                                    print(f"Lỗi khi xóa file {file_name}: {str(e)}")
                
                return redirect(url_for('trang_quan_li', message='Đăng bài thành công'))
            except json.JSONDecodeError as e:
                print(f"Lỗi phân tích cú pháp JSON: {str(e)}")  
                return render_template("quan_ly/bai_dang_trang_chu.html", error="Có lỗi xảy ra khi phân tích dữ liệu. Vui lòng thử lại.")
            except Exception as e:
                print(f"Lỗi khi lưu bài đăng: {str(e)}") 
                return render_template("quan_ly/bai_dang_trang_chu.html", error="Có lỗi xảy ra khi đăng bài. Vui lòng thử lại.")
    return render_template("quan_ly/bai_dang_trang_chu.html")

@app.route("/quan-li/quan-ly-dang-bai", methods=['GET', 'POST'])
def trang_dang_bai():
    if session.get("quanli") is None:
        return redirect(url_for('login'))
    
    bai_dang_file = os.path.join(current_app.root_path, './du_lieu/bai_dang.json')
    
    if request.method == 'POST':
        action = request.form.get('action')
        bai_dang_id = request.form.get('id')
        
        with open(bai_dang_file, 'r', encoding='utf-8') as file:
            bai_dang_list = json.load(file)
        
        for bai_dang in bai_dang_list:
            if bai_dang['id'] == bai_dang_id:
                if action == 'edit':
                    bai_dang['tieu_de'] = request.form.get('tieu_de')
                    bai_dang['noi_dung'] = request.form.get('noi_dung')
                elif action == 'delete':
                    bai_dang_list.remove(bai_dang)
                elif action == 'hide':
                    bai_dang['an'] = True
                elif action == 'show':
                    bai_dang['an'] = False
                break
        
        with open(bai_dang_file, 'w', encoding='utf-8') as file:
            json.dump(bai_dang_list, file, indent=4, ensure_ascii=False)
        
        return redirect(url_for('trang_dang_bai'))
    
    with open(bai_dang_file, 'r', encoding='utf-8') as file:
        bai_dang_list = json.load(file)
    
    return render_template("quan_ly/quan_ly_dang_bai.html", bai_dang_list=bai_dang_list)

