from flask import request, render_template, url_for, session, redirect
from app_school.xu_ly.Xu_ly_Form import *
from app_school.xu_ly.lop_hoc.XL_Lop_hoc import lay_nien_khoa_theo_lop, cap_nhat_si_so
from app_school.xu_ly.giao_vien.XL_Giao_vien import Profile_Giao_Vien
from app_school.xu_ly.bang_diem.XL_Bang_diem import tao_bang_diem_cho_hoc_sinh, doc_bang_diem_theo_hoc_sinh
from app_school.xu_ly.hoc_sinh.XL_Hoc_sinh import Profile_hoc_sinh
from app_school.xu_ly.Xu_ly_Model import HocSinh, Lop
from app_school.xu_ly.hoc_sinh.XL_Hoc_sinh import *
from app_school.xu_ly.lich_thi.XL_lich_thi import *
from app_school.xu_ly.thoi_khoa_bieu.XL_TKB import *
from app_school import app, db_session
from datetime import date

@app.route('/them-hoc-sinh/<string:lop>', methods=['GET', 'POST'])
def them_hoc_sinh(lop):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    giaovien = session['giaovien']
    giao_vien = Profile_Giao_Vien(giaovien)
    form = Form_Update_Hs()
    error = ''
    message = ''
    if form.validate_on_submit():
        HoVaTen = request.form['Th_Ho_ten']
        GioiTinh = request.form['Th_Gioi_tinh']
        DiaChi = request.form['Th_Dia_chi']
        Email = request.form['Th_Email']
        NgaySinh = request.form['Th_Ngay_sinh']
        SoDienThoai = request.form['Th_Sdt']
        SoDienThoaiPhuHuynh = request.form['Th_Sdt_PH']
        MatKhau = request.form['Th_Mat_khau']
        if MatKhau == '':
            MatKhau = '1234'
        IDLop = int(lop)
        nien_khoa = lay_nien_khoa_theo_lop(lop)
        IDNienKhoa = int(nien_khoa.ID)
        hoc_sinh = HocSinh(HoVaTen=HoVaTen, GioiTinh=GioiTinh, DiaChi=DiaChi, Email=Email, NgaySinh=NgaySinh,
                           SoDienThoai=SoDienThoai, SoDienThoaiPhuHuynh=SoDienThoaiPhuHuynh, IDLop=IDLop, IDNienKhoa=IDNienKhoa, MatKhau=MatKhau)
        try:
            db_session.add(hoc_sinh)
            db_session.commit()
            if cap_nhat_si_so(lop):
                message += 'Đã cập nhật sỉ số lớp; '
            else: 
                error += 'Không thể cập nhật sỉ số lớp'
            if tao_bang_diem_cho_hoc_sinh(hoc_sinh.IDHocSinh):
                message += 'Đã thêm học sinh ' + HoVaTen + ';'
                return redirect(url_for('danh_sach_hoc_sinh', lop=lop, message=message))
            else:
                db_session.rollback()
                error += 'Không thể tạo bảng điểm'
                pass
        except:
            error = 'Học sinh đã tồn tại'
            db_session.rollback()
            pass
        print(error)
    return render_template('hoc_sinh/hs_them_hoc_sinh.html', form=form, error=error)


@app.route('/thong-tin-diem-so/<string:id_hoc_sinh>', methods=['GET','POST'])
def thong_tin_diem_so(id_hoc_sinh):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    giaovien = session['giaovien']
    giao_vien = Profile_Giao_Vien(giaovien)
    hs = Profile_hoc_sinh(id_hoc_sinh)
    ds_bang_diem = doc_bang_diem_theo_hoc_sinh(id_hoc_sinh)
    return render_template('hoc_sinh/gv_bang_diem_hoc_sinh.html', ds_bang_diem=ds_bang_diem, ten_hs=hs['HoVaTen'], id_hoc_sinh = id_hoc_sinh)

@app.route('/thong-tin-hoc-sinh/<string:hoc_sinh>', methods=['GET','POST'])
def thong_tin_hoc_sinh(hoc_sinh):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    message = ''
    giaovien = session['giaovien']
    giao_vien = Profile_Giao_Vien(giaovien)
    id_hoc_sinh = hoc_sinh
    HocSinh = Profile_hoc_sinh(id_hoc_sinh)
    if request.args.get('message'):
        message = request.args.get('message')
        print(message)
    return render_template('hoc_sinh/hs_thong_tin_hoc_sinh.html',HocSinh=HocSinh, message=message)

@app.route('/thong-tin-hoc-sinh/<string:hoc_sinh>/sua-hoc-sinh', methods=['GET','POST'])
def sua_thong_tin_hoc_sinh(hoc_sinh):
    form = Form_Update_Hs()
    id_hoc_sinh = hoc_sinh
    Hoc_Sinh = Profile_hoc_sinh(id_hoc_sinh)
    value = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == id_hoc_sinh).first()
    if form.validate_on_submit():
        HocVaTen = request.form['Th_Ho_ten']
        GioiTinh = request.form['Th_Gioi_tinh']
        NgaySinh = request.form['Th_Ngay_sinh']
        DiaChi = request.form['Th_Dia_chi']
        Email = request.form['Th_Email']
        SoDienThoai = request.form['Th_Sdt']
        SoDienThoaiPhuHuynh = request.form['Th_Sdt_PH']
        
        value = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == id_hoc_sinh).first()
        value.HoVaTen = HocVaTen
        value.GioiTinh = GioiTinh
        value.NgaySinh =  datetime.strptime(NgaySinh,'%Y-%m-%d' ).date()
        value.Email = Email
        value.DiaChi = DiaChi
        value.SoDienThoai = SoDienThoai
        value.SoDienThoaiPhuHuynh = SoDienThoaiPhuHuynh
        db_session.flush()
        db_session.commit()
        return redirect('/thong-tin-hoc-sinh/'+id_hoc_sinh)
    form.Th_Gioi_tinh.default = Hoc_Sinh['GioiTinh']
    form.process()  
    return render_template('hoc_sinh/hs_sua_thong_tin.html',HocSinh=Hoc_Sinh,form=form )

@app.route('/hoc-sinh/dang-xuat', methods=['GET', 'POST'])
def dang_xuat_hs():
    if session.get("hocsinh") != None:
        session.pop("hocsinh", None)
    return redirect('/')

@app.route('/hoc-sinh', methods=['GET','POST'])
def hoc_sinh():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    error = ''
    message = ''
    hocsinh = session['hocsinh']
    hoc_sinh = Profile_hoc_sinh(hocsinh)
    if request.args.get('message'):
        message = request.args.get('message')
        print(message)
    return render_template('hoc_sinh/thong_tin.html',HocSinh=hoc_sinh, message=message )

@app.route('/hoc-sinh/sua-hoc-sinh', methods=['GET','POST'])
def cap_nhat_hoc_sinh():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    error = ''
    message = ''
    hocsinh = session['hocsinh']
    form = Form_Update_Hs()
    id_hoc_sinh = hocsinh
    Hoc_Sinh = Profile_hoc_sinh(id_hoc_sinh)

    value = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == id_hoc_sinh).first()
    if form.validate_on_submit():
        HocVaTen = request.form['Th_Ho_ten']
        GioiTinh = request.form['Th_Gioi_tinh']
        NgaySinh = request.form['Th_Ngay_sinh']
        DiaChi = request.form['Th_Dia_chi']
        Email = request.form['Th_Email']
        SoDienThoai = request.form['Th_Sdt']
        SoDienThoaiPhuHuynh = request.form['Th_Sdt_PH']
        
        
        value = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == id_hoc_sinh).first()
        value.HoVaTen = HocVaTen
        value.GioiTinh = GioiTinh
        value.NgaySinh =  datetime.strptime(NgaySinh,'%Y-%m-%d' ).date()
        value.Email = Email
        value.DiaChi = DiaChi
        value.SoDienThoai = SoDienThoai
        value.SoDienThoaiPhuHuynh = SoDienThoaiPhuHuynh
        db_session.flush()
        db_session.commit()
        return redirect(url_for('hoc_sinh', message='Cập nhật thành công'))
    form.Th_Gioi_tinh.default = Hoc_Sinh['GioiTinh']
    form.process()   
    return render_template('hoc_sinh/cap_nhat_thong_tin.html',HocSinh=Hoc_Sinh , form = form)

@app.route('/hoc-sinh/bang_diem', methods=['GET','POST'])
def bang_diem_hoc_sinh():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    error = ''
    hocsinh = session['hocsinh']

    return render_template('hoc_sinh/bang_diem.html')

@app.route('/hoc-sinh/doi-mat-khau', methods=['GET', 'POST'])
def doi_mat_khau_hs():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    hocsinh = session['hocsinh']
    
    hs = Profile_hoc_sinh(hocsinh)
    ThongBao = ""
    form = Form_Reset_pw()

    if form.validate_on_submit():
        MatkhauCu = request.form['Th_MatkhauCu']
        MatkhauMoi = request.form['Th_MatkhauMoi']
        ThongBao = hs_doi_mat_khau(hocsinh, MatkhauCu, MatkhauMoi)
        if ThongBao == "Đổi Mật Khẩu Thành Công":
            return redirect(url_for('hoc_sinh', message='Đổi mật khẩu thành công'))
    return render_template('hoc_sinh/doi_mat_khau.html', form=form, ThongBao=ThongBao)

@app.route('/hoc-sinh/lich-thi', methods=['GET', 'POST'])
def lich_thi_hs():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    hocsinh = session['hocsinh']
    lt = load_lich_thi_hs(hocsinh)
    
    return render_template('hoc_sinh/xem_lich_thi.html',lich_thi = lt)

@app.route('/hoc-sinh/bangdiem', methods=['GET', 'POST'])
def bang_diem_hs():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    hocsinh = session['hocsinh']
    DiemTB = 0
    so_mon  = 0
    bangdiem = db_session.query(BangDiem).filter(BangDiem.IDHocSinh == hocsinh).all()
    for i in bangdiem:
        i.IDMon = Ten_Mon(i.IDMon)
        if i.TrungBinhMon != None:
            DiemTB += i.TrungBinhMon
            so_mon = so_mon + 1
    DiemTB = DiemTB / so_mon
    return render_template('hoc_sinh/xem_bang_diem.html',bangdiem = bangdiem, DiemTB = DiemTB)

@app.route('/hoc-sinh/thoi-khoa-bieu', methods=['GET', 'POST'])
def thoi_khoa_bieu_hs():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    hocsinh = session['hocsinh']
    hs  = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == hocsinh).first()
    tkb = doc_thoi_khoa_bieu_hs(hs.IDLop,hs.IDNienKhoa)
    return render_template('hoc_sinh/xem_thoi_khoa_bieu.html',tkb=tkb)