from flask import request, render_template, url_for, session, redirect
from app_school.xu_ly.giao_vien.XL_Giao_vien import *
from app_school.xu_ly.bang_diem.XL_Bang_diem import doc_bang_diem_theo_id_bang_diem, cap_nhat_bang_diem
from app_school.xu_ly.hoc_sinh.XL_Hoc_sinh import Profile_hoc_sinh
from app_school.xu_ly.thoi_khoa_bieu.XL_TKB import *
from app_school.xu_ly.nien_khoa.XL_Nien_khoa import doc_danh_sach_nien_khoa_select
from app_school.xu_ly.mon_hoc.XL_Mon_hoc import doc_danh_sach_mon_hoc
from app_school.xu_ly.lop_hoc.XL_Lop_hoc import doc_danh_sach_lop_hoc_select, doc_danh_sach_lop_hoc_nien_khoa_select
from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import GiaoVien, Mon, HocSinh, BangDiem
from app_school.xu_ly.Xu_ly_Form import *
import json

ds_thu = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7']
ds_tiet = ['Tiết 1', 'Tiết 2', 'Tiết 3', 'Tiết 4']
ds_buoi = ['Buổi sáng', 'Buổi chiều']


@app.route('/thoi-khoa-bieu', methods=['GET', 'POST'])
def thoi_khoa_bieu():
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    giaovien = session['giaovien']
    giao_vien = Profile_Giao_Vien(giaovien)
    nien_khoa = ''
    lop = ''
    ds_nien_khoa = doc_danh_sach_nien_khoa_select()
    ds_lop = doc_danh_sach_lop_hoc_nien_khoa_select()
    lop = ds_lop[0][0]
    nien_khoa = ds_nien_khoa[0][0]
    # TKB = db_session.query(ThoiKhoaBieu).first()
    if int(giao_vien['Quyen']) == 2:
        if request.form.get('lop_nien_khoa'):
            lop = request.form.get('lop_nien_khoa').split('-')[1]
            nien_khoa = request.form.get('lop_nien_khoa').split('-')[0]
        tkb = doc_thoi_khoa_bieu(nien_khoa, lop)
    elif int(giao_vien['Quyen']) == 1:
        if request.form.get('nien_khoa'):
            nien_khoa = request.form.get('nien_khoa')
        tkb = doc_thoi_khoa_bieu_gv(nien_khoa, giao_vien['ID_GV'])
    else:
        tkb = tao_thoi_khoa_bieu_rong()
    return render_template('thoi_khoa_bieu/tkb_hien_thi.html', tkb=tkb, id_nien_khoa=nien_khoa,
                           ds_nien_khoa=ds_nien_khoa, id_lop=lop, ds_lop=ds_lop, Quyen=giao_vien['Quyen'])


@app.route('/cap-nhat-tkb/<string:id_nien_khoa>/<string:id_lop>/<string:id_thu>/<string:id_buoi>/<string:id_tiet>', methods=['GET', 'POST'])
def cap_nhat_tkb(id_nien_khoa, id_lop, id_thu, id_buoi, id_tiet):
    if session.get("giaovien") == None:
        return redirect(url_for('index'))
    giaovien = session['giaovien']
    chi_tiet = {}
    chi_tiet_tkb = doc_thong_tin_chi_tiet_tkb(
        id_nien_khoa, id_lop, id_thu, id_buoi, id_tiet)
    ds_mon = doc_danh_sach_mon_hoc()
    ds_giao_vien = doc_danh_sach_gv_select()
    # xu ly form
    form = Form_Cap_nhat_TKB()
    form.Th_Mon.choices = ds_mon
    form.Th_Giao_vien.choices = ds_giao_vien
    chi_tiet['nien_khoa'] = ten_nien_khoa(id_nien_khoa)
    chi_tiet['lop'] = ten_lop(id_lop)
    chi_tiet['thu'] = ds_thu[int(id_thu) - 2]
    chi_tiet['buoi'] = ds_buoi[int(id_buoi) - 1]
    chi_tiet['tiet'] = ds_tiet[int(id_tiet) - 1]
    # dieu chinh thong tin
    for tkb in chi_tiet_tkb:
        form.Th_Giao_vien.default = tkb.ID_Giao_vien
        form.Th_Mon.default = tkb.ID_Mon
        if str(id_lop) != str(tkb.ID_Lop):
            form.Th_Giao_vien.choices = doc_danh_sach_gv_loai_tru_select(
                tkb.ID_Giao_vien)
    if form.validate_on_submit():
        id_giao_vien = request.form['Th_Giao_vien']
        id_mon = request.form['Th_Mon']
        tkb = ThoiKhoaBieu(ID_Nien_khoa=id_nien_khoa, ID_Giao_vien=id_giao_vien,
                     Thu=id_thu, Buoi=id_buoi, Tiet=id_tiet, ID_Lop=id_lop, ID_Mon=id_mon)
        tkb_chi_tiet = doc_thong_tin_chi_tiet_tkb_theo_lop(id_nien_khoa, id_lop, id_thu, id_buoi, id_tiet)
        if tkb_chi_tiet:
            print('exist')
            tkb_chi_tiet.ID_Giao_vien = id_giao_vien
            tkb_chi_tiet.ID_Mon = id_mon
            try:
                db_session.flush()
                db_session.commit()
                return redirect(url_for('thoi_khoa_bieu'))
            except:
                db_session.rollback()
                pass
        elif them_thoi_khoa_bieu(tkb):
            print('add')
            return redirect(url_for('thoi_khoa_bieu'))
    return render_template('thoi_khoa_bieu/tkb_cap_nhat.html', form=form, chi_tiet=chi_tiet)
