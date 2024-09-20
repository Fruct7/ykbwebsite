from flask import request, render_template, url_for, session, redirect
from app_school.xu_ly.Xu_ly_Form import Form_Create_Class
from app_school.xu_ly.nien_khoa.XL_Nien_khoa import doc_danh_sach_nien_khoa_select
from app_school.xu_ly.khoi.XL_Khoi import doc_danh_sach_khoi_select
from app_school.xu_ly.giao_vien.XL_Giao_vien import doc_danh_sach_gv_select, Profile_Giao_Vien
from app_school.xu_ly.lop_hoc.XL_Lop_hoc import doc_danh_sach_lop_hoc, doc_danh_sach_lop_hoc_theo_giao_vien
from app_school.xu_ly.hoc_sinh.XL_Hoc_sinh import doc_danh_sach_hoc_sinh_theo_lop, doc_danh_sach_bang_diem_hoc_sinh_theo_lop
from app_school.xu_ly.mon_hoc.XL_Mon_hoc import doc_danh_sach_mon_hoc
from app_school.xu_ly.Xu_ly_Model import Lop
from app_school import app, db_session

@app.route('/danh-sach-lop', methods=['GET','POST'])
def danh_sach_lop():
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    message = ''
    ds_lop_hoc = []
    giaovien = session['giaovien']
    giao_vien = Profile_Giao_Vien(giaovien)
    ds_nien_khoa = doc_danh_sach_nien_khoa_select()
    if giao_vien['Quyen'] == '1':
        ds_lop_hoc = doc_danh_sach_lop_hoc_theo_giao_vien(giao_vien['ID_GV'])
    elif giao_vien['Quyen'] == '2':
        ds_lop_hoc = doc_danh_sach_lop_hoc()
    if request.form.get('nien_khoa'):
        nien_khoa = request.form.get('nien_khoa')
        if nien_khoa != 'all':
            ds_lop_hoc_moi = list(ds_lop_hoc)
            for lop_hoc in ds_lop_hoc_moi:
                print(lop_hoc)
                if str(lop_hoc['ID_nien_khoa']) != nien_khoa:
                    del ds_lop_hoc[ds_lop_hoc.index(lop_hoc)]
    if request.args.get('message'):
        message = request.args.get('message')
        print(message)
    return render_template('lop_hoc/l_danh_sach_lop.html', ds_lop_hoc = ds_lop_hoc, ds_nien_khoa=ds_nien_khoa, message=message, quyen = giao_vien['Quyen'])

    
@app.route('/chi-tiet-lop/<string:lop>', methods=['GET','POST'])
def danh_sach_hoc_sinh(lop):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    message = ''
    giaovien = session['giaovien']
    giao_vien = Profile_Giao_Vien(giaovien)
    ds_hoc_sinh = doc_danh_sach_hoc_sinh_theo_lop(lop)
    if request.args.get('message'):
        message = request.args.get('message')
        print(message)
    return render_template('lop_hoc/l_chi_tiet_lop.html', IDLop = lop, ds_hoc_sinh=ds_hoc_sinh, message=message, quyen = giao_vien['Quyen'])

    
@app.route('/bang-diem-lop/<string:lop>', methods=['GET', 'POST'])
def bang_diem_lop(lop):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    giaovien = session['giaovien']
    giao_vien = Profile_Giao_Vien(giaovien)
    ds_hoc_sinh = doc_danh_sach_bang_diem_hoc_sinh_theo_lop(lop)
    ds_mon = doc_danh_sach_mon_hoc()
    return render_template('lop_hoc/l_bang_diem_lop.html', ds_hoc_sinh = ds_hoc_sinh, ds_mon=ds_mon)


@app.route('/them-lop-hoc', methods=['GET','POST'])
def them_lop_hoc():
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    giaovien = session['giaovien']
    giao_vien = Profile_Giao_Vien(giaovien)
    form = Form_Create_Class()
    ds_nien_khoa = doc_danh_sach_nien_khoa_select()
    ds_khoi = doc_danh_sach_khoi_select()
    ds_gv = doc_danh_sach_gv_select()
    form.Th_Nien_khoa.choices = ds_nien_khoa
    form.Th_Khoi.choices = ds_khoi
    form.Th_GV_Chu_nhiem.choices = ds_gv
    error = ''
    if form.validate_on_submit():
        TenLop = request.form['Th_Lop']
        DiaDiem = request.form['Th_Dia_diem']
        TongSoHS = 0
        NamNienKhoa = int(request.form['Th_Nien_khoa'])
        GV_CN = int(request.form['Th_GV_Chu_nhiem'])
        IDKhoi  = int(request.form['Th_Khoi'])
        lop_hoc = Lop(TenLop=TenLop, DiaDiem=DiaDiem, TongSoHS=TongSoHS, NamNienKhoa=NamNienKhoa, GV_CN=GV_CN, IDKhoi=IDKhoi)
        try:
            db_session.add(lop_hoc)
            db_session.commit()
            return redirect(url_for('danh_sach_lop', message='Thêm lớp thành công'))
        except:
            db_session.rollback()
            error = 'Lớp học đã tồn tại'
            pass
    return render_template('lop_hoc/l_them_lop.html', form=form, error=error)

