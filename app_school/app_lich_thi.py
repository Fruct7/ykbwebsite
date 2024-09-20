from flask import request, render_template, url_for, session, redirect
from app_school.xu_ly.giao_vien.XL_Giao_vien import *
from app_school.xu_ly.bang_diem.XL_Bang_diem import doc_bang_diem_theo_id_bang_diem, cap_nhat_bang_diem
from app_school.xu_ly.hoc_sinh.XL_Hoc_sinh import Profile_hoc_sinh
from app_school.xu_ly.thoi_khoa_bieu.XL_TKB import *
from app_school.xu_ly.khoi.XL_Khoi import *
from app_school.xu_ly.mon_hoc.XL_Mon_hoc import *
from app_school.xu_ly.nien_khoa.XL_Nien_khoa import doc_danh_sach_nien_khoa_select
from app_school.xu_ly.lop_hoc.XL_Lop_hoc import doc_danh_sach_lop_hoc_select
from app_school.xu_ly.lich_thi.XL_lich_thi import *
from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import *
from app_school.xu_ly.Xu_ly_Form import *
import datetime


@app.route('/xem-lich-thi', methods=['GET', 'POST'])
def xem_lich_thi():
    ds_nien_khoa = doc_danh_sach_nien_khoa_select()
    ds_khoi = doc_danh_sach_khoi_select()

    khoi = ds_khoi[0][0]
    nien_khoa = ds_nien_khoa[0][0]

    form  = Form_Lich_Thi()
    form.Th_Nien_khoa.choices = ds_nien_khoa
    form.Th_Khoi.choices = ds_khoi
    if form.validate_on_submit():
        nien_khoa = request.form['Th_Nien_khoa']
        khoi = request.form['Th_Khoi']

        form.Th_Khoi.default = khoi
        form.Th_Nien_khoa.default = nien_khoa

    lichthi = load_lich_thi(nien_khoa,khoi)
    return render_template('lich_thi/lich_thi.html',lich_thi = lichthi, form=form)

@app.route('/them-lich-thi', methods=['GET', 'POST'])
def Them_lich_thi():
    error = ""
    date = datetime.date.today()
    ds_nien_khoa = doc_danh_sach_nien_khoa_select()
    ds_khoi = doc_danh_sach_khoi_select()
    ds_Mon = doc_danh_sach_mon_hoc()

    khoi = ds_khoi[0][0]
    nien_khoa = ds_nien_khoa[0][0]
    mon = ds_Mon[0][0]

    form  = Form_Them_Lich_Thi()
    form.Th_Nien_khoa.choices = ds_nien_khoa
    form.Th_Khoi.choices = ds_khoi
    form.Th_Khoi.choices = ds_khoi
    form.Th_Mon.choices = ds_Mon
    if form.validate_on_submit():
        nien_khoa = request.form['Th_Nien_khoa']
        khoi = request.form['Th_Khoi']
        Mon = request.form['Th_Mon']
        NgayThi = request.form['Th_NgayThi']
        Thoi_gian = request.form['Th_ThoiGian']
        lich_thi = LichThi(   ID_Nien_khoa = nien_khoa,   ID_Khoi = khoi, ID_Mon = Mon , ThoiGianThi = NgayThi , ThoiGianLamBai = Thoi_gian)
        error = Them_Lich_Thi(lich_thi)
    return render_template('lich_thi/them_lich_thi.html' ,form = form , date = date , loi = error)

@app.route('/sua-lich-thi/<string:id_nien_khoa>/<string:id_khoi>/<string:id_mon>', methods=['GET', 'POST'])
def Sua_lich_thi(id_nien_khoa,id_khoi,id_mon):
    lich_thi  = db_session.query(LichThi).filter(LichThi.ID_Nien_khoa == id_nien_khoa ,LichThi.ID_Khoi == id_khoi , LichThi.ID_Mon == id_mon).first()
  
    lich = {}
    lich['Mon'] = ten_mon(id_mon)
    lich['NienKhoa'] = ten_nien_khoa(id_nien_khoa)
    lich['Khoi'] = ten_nien_khoa(id_khoi)
    lich['NgayThi'] = lich_thi.ThoiGianThi
    lich['ThoiGian'] = lich_thi.ThoiGianLamBai

    form = Form_Sua_Lich_Thi()
    if form.validate_on_submit():
        NgayThi = request.form['Th_NgayThi']
        ThoiGian = request.form['Th_ThoiGian']

        lich_thi.ID_Nien_khoa = id_nien_khoa
        lich_thi.ID_Khoi = id_khoi
        lich_thi.ID_Mon = id_mon
        lich_thi.ThoiGianThi = NgayThi
        lich_thi.ThoiGianLamBai = ThoiGian

        db_session.flush()
        db_session.commit()
        return redirect(url_for('xem_lich_thi' ,message='Cập nhật thành công'))
    return render_template('lich_thi/sua_lich_thi.html', lich = lich, form = form)