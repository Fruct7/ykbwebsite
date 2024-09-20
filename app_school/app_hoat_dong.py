from flask import request, render_template, url_for, session, redirect
from app_school.xu_ly.Xu_ly_Form import *
from app_school.xu_ly.Xu_ly_Model import *
from app_school.xu_ly.hoc_sinh.XL_Hoc_sinh import * 
from app_school.xu_ly.hoat_dong.XL_Hoat_dong import *
from app_school.xu_ly.nien_khoa.XL_Nien_khoa import *
from sqlalchemy import func 
from app_school import app, db_session

@app.route('/hoc-sinh/hoat-dong', methods=['GET', 'POST'])
def hoat_dong_hs():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    hocsinh = session['hocsinh']    

    message = ''
    hs = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == hocsinh).one()
    hdong = load_danh_sach_hoat_dong(hs.IDNienKhoa,hs)
    if request.args.get('message_hoatdong'):
        message = request.args.get('message_hoatdong')
        
    return render_template('hoat_dong/hs_xem_hoat_dong.html',hoat_dong = hdong,message_hoatdong = message)

@app.route('/hoc-sinh/hoat-dong/tham-gia/<string:id_hoat_dong>', methods=['GET', 'POST'])
def tham_gia_hoat_dong_hs(id_hoat_dong):
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    hocsinh = session['hocsinh']   
    ngay_dang_ky = datetime.now()
    
    hd = db_session.query(Hoat_Dong).filter(Hoat_Dong.IDHoatDong == id_hoat_dong).first()
    HanDangKy = datetime.strptime( hd.ThoiHanDangKy, '%d-%m-%Y')
    if ngay_dang_ky > HanDangKy:
        return redirect(url_for('hoat_dong_hs', message_hoatdong='Đã Quá Hạn Đăng Ký'))
    else: 
        ngay_dang_ky = datetime.now().date()
        ngay_dang_ky = ngay_dang_ky.strftime("%d-%m-%Y")
        thamgia = Tham_Gia_Hoat_Dong(IDHoatDong = id_hoat_dong  ,IDHocSinh = hocsinh , NgayDangKy = ngay_dang_ky)
        hd.SoNguoiDaThamGia += 1
        db_session.add(thamgia)
        db_session.flush()
        db_session.commit()
        message = 'Đã Đăng Ký ' + hd.TieuDe
        return redirect(url_for('hoat_dong_hs', message_hoatdong= message))

@app.route('/hoc-sinh/hoat-dong/huy-tham-gia/<string:id_hoat_dong>', methods=['GET', 'POST'])
def huy_tham_gia_hoat_dong_hs(id_hoat_dong):
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    hocsinh = session['hocsinh']   
    hd = db_session.query(Hoat_Dong).filter(Hoat_Dong.IDHoatDong == id_hoat_dong).first()
    hd.SoNguoiDaThamGia -= 1 
    db_session.delete(db_session.query(Tham_Gia_Hoat_Dong).filter(Tham_Gia_Hoat_Dong.IDHoatDong == id_hoat_dong, Tham_Gia_Hoat_Dong.IDHocSinh == hocsinh).one())
    db_session.flush()
    db_session.commit()
    message = 'Đã Hủy Đăng Ký ' + hd.TieuDe
    return redirect(url_for('hoat_dong_hs', message_hoatdong= message))


@app.route('/hoc-sinh/hoat-dong-da-tham-gia', methods=['GET', 'POST'])
def hoat_dong_da_tham_gia_hs():
    if session.get("hocsinh") == None:
        return redirect(url_for('index'))
    hocsinh = session['hocsinh'] 

    ds_hd = hoat_dong_da_tham_gia(hocsinh)
    return render_template('hoat_dong/hs_hoat_dong_da_tham_gia.html',hoat_dong = ds_hd)

@app.route('/giao-vien/hoat-dong', methods=['GET', 'POST'])
def hoat_dong_gv():
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    giaovien = session['giaovien']
    ds_hd = []

    form = Form_Xem_Hoat_Dong()
    ds_nien_khoa = doc_danh_sach_nien_khoa_select()
    nien_khoa = ds_nien_khoa[0][0]
    form.Th_Nien_khoa.choices = ds_nien_khoa
    message = ''
    if request.args.get('message_hoatdong'):
        message = request.args.get('message_hoatdong')

    if form.validate_on_submit():
        nien_khoa = request.form['Th_Nien_khoa']
        form.Th_Nien_khoa.default = nien_khoa
    ds_hd =  load_danh_sach_hoat_dong_gv(nien_khoa)
    return render_template('hoat_dong/gv_xem_hoat_dong.html', hoat_dong=ds_hd, form = form,message_hoatdong = message)

@app.route('/giao-vien/hoat-dong/danh-sach-nguoi-tham-gia/<string:id_hoat_dong>', methods=['GET', 'POST'])
def danh_sach_nguoi_tham_gia(id_hoat_dong):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))   
    giaovien = session['giaovien']

    hdong = db_session.query(Tham_Gia_Hoat_Dong).filter(Tham_Gia_Hoat_Dong.IDHoatDong == id_hoat_dong).all()
    ds = []
    for i in hdong:
        hs = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == i.IDHocSinh).first()
        t = {}
        t['HocSinh'] = hs.HoVaTen
        t['Lop'] = ten_lop(hs.IDLop)
        t['NgayDangKy'] = datetime.strptime(i.NgayDangKy, '%d-%m-%Y')
        ds.append(t)
    
    danhsach = ds
    So_nguoi = len(danhsach)
    return render_template('hoat_dong/gv_xem_danh_sach_nguoi_tham_gia.html',danhsach=danhsach,So_nguoi=So_nguoi)

@app.route('/giao-vien/hoat-dong/xoa-hoat-dong/<string:id_hoat_dong>', methods=['GET', 'POST'])
def xoa_hoat_dong(id_hoat_dong):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))   
    giaovien = session['giaovien']
    if db_session.query(Tham_Gia_Hoat_Dong).filter(Tham_Gia_Hoat_Dong.IDHoatDong == id_hoat_dong).count() > 0 :
        db_session.query(Tham_Gia_Hoat_Dong).filter(Tham_Gia_Hoat_Dong.IDHoatDong == id_hoat_dong).delete()
        db_session.commit()
    hd = db_session.query(Hoat_Dong).filter(Hoat_Dong.IDHoatDong == id_hoat_dong).one()
    db_session.delete(db_session.query(Hoat_Dong).filter(Hoat_Dong.IDHoatDong == id_hoat_dong).one()) 
    db_session.commit()
   
    message = "Đã xóa hoạt động " + hd.TieuDe
    return redirect(url_for('hoat_dong_gv', message_hoatdong= message))

@app.route('/giao-vien/hoat-dong/them-hoat-dong', methods=['GET', 'POST'])
def them_hoat_dong():
    if session.get("giaovien") == None:
        return redirect(url_for('index'))   
    giaovien = session['giaovien']
    ds_nienkhoa = doc_danh_sach_nien_khoa_select()
    
    form = Form_Them_Hoat_Dong()
    form.Th_Nien_khoa.choices = ds_nienkhoa

    if form.validate_on_submit():
        ds_doi_tuong = request.form.getlist('Th_Khoi')

        khoi10 = 0
        khoi11 = 0
        khoi12 = 0

        if '1' in ds_doi_tuong:
            khoi10 = 1
        if '2' in ds_doi_tuong:
            khoi11 = 1
        if '3' in ds_doi_tuong:
            khoi12 = 1

        nien_khoa = request.form['Th_Nien_khoa']
        tieu_de = request.form['Th_TieuDe']
        noi_dung = request.form['Th_NoiDung']

        thoi_han = request.form['Th_HanDangKy']
        thoi_han = datetime.strptime(thoi_han, '%Y-%m-%d')
        thoi_han = thoi_han.strftime("%d-%m-%Y")
        
        IDHoat_Dong = db_session.query(func.max(Hoat_Dong.IDHoatDong)).first()
        ID  = IDHoat_Dong[0] + 1

        hd = Hoat_Dong(IDHoatDong = ID, GiaoVienTao = giaovien ,TieuDe = tieu_de, NoiDung = noi_dung,ThoiHanDangKy = thoi_han, Khoi_10 = khoi10 , Khoi_11 = khoi11, Khoi_12 = khoi12, NienKhoa = nien_khoa, SoNguoiDaThamGia = 0)
        db_session.add(hd)
        db_session.commit()
        message = "Đã thêm hoạt động " + hd.TieuDe
        return redirect(url_for('hoat_dong_gv', message_hoatdong= message))
    return render_template('hoat_dong/gv_them_hoat_dong.html',form=form)

@app.route('/giao-vien/hoat-dong/sua-hoat-dong/<string:ID_hoat_dong>', methods=['GET', 'POST'])
def sua_hoat_dong(ID_hoat_dong):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))   
    giaovien = session['giaovien']

    form = Form_Them_Hoat_Dong()

    ds_nienkhoa = doc_danh_sach_nien_khoa_select()
    form = Form_Sua_Hoat_Dong()
    form.Th_Nien_khoa.choices = ds_nienkhoa

    hd = db_session.query(Hoat_Dong).filter(Hoat_Dong.IDHoatDong ==  ID_hoat_dong).first()
    hd.ThoiHanDangKy = datetime.strptime(hd.ThoiHanDangKy,'%d-%m-%Y' ).date()
    form.Th_Nien_khoa.default = ds_nienkhoa[0][0]

    if hd.GiaoVienTao != giaovien:
            message = "Bạn không phải giáo viên tạo hoạt động ^_^"
            return redirect(url_for('hoat_dong_gv', message_hoatdong= message))
    else:
        if form.validate_on_submit():
            ds_doi_tuong = request.form.getlist('Th_Khoi')

            khoi10 = 0
            khoi11 = 0
            khoi12 = 0

            if '1' in ds_doi_tuong:
                khoi10 = 1
            if '2' in ds_doi_tuong:
                khoi11 = 1
            if '3' in ds_doi_tuong:
                khoi12 = 1        

            nien_khoa = request.form['Th_Nien_khoa']
            tieu_de = request.form['Th_TieuDe']
            noi_dung = request.form['Th_NoiDung']

            thoi_han = request.form['Th_HanDangKy']
            thoi_han = datetime.strptime(thoi_han, '%Y-%m-%d')
            thoi_han = thoi_han.strftime("%d-%m-%Y")   

            value = db_session.query(Hoat_Dong).filter(Hoat_Dong.IDHoatDong == ID_hoat_dong).first()     
            value.TieuDe = tieu_de
            value.NoiDung = noi_dung
            value.ThoiHanDangKy = thoi_han
            value.Khoi_10 = khoi10
            value.Khoi_11 = khoi11
            value.Khoi_12 = khoi12
            value.NienKhoa = nien_khoa
            db_session.flush()
            db_session.commit()
            message = "Đã Sửa hoạt động " + hd.TieuDe
            return redirect(url_for('hoat_dong_gv', message_hoatdong= message))
    return render_template('hoat_dong/gv_sua_hoat_dong.html',form=form, hoat_dong= hd)  