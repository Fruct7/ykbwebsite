from flask import request, render_template, url_for, session, redirect
from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import GiaoVien
from datetime import datetime
def doc_danh_sach_gv_select(): # select field tupple choice
    ds_giao_vien = []
    try:
        ds_gv = db_session.query(GiaoVien).all()
        for giao_vien in ds_gv:
            gv = (giao_vien.IDGiaoVien,  giao_vien.HoVaTen + ' - ' + giao_vien.TenDangNhap)
            ds_giao_vien.append(gv)
    except:
        pass
    return ds_giao_vien

def doc_danh_sach_gv_loai_tru_select(GV_ID): # select field tupple choice
    ds_giao_vien = []
    try:
        ds_gv = db_session.query(GiaoVien).filter(GiaoVien.IDGiaoVien != GV_ID).all()
        for giao_vien in ds_gv:
            gv = (giao_vien.IDGiaoVien,  giao_vien.HoVaTen + ' - ' + giao_vien.TenDangNhap)
            ds_giao_vien.append(gv)
    except:
        pass
    return ds_giao_vien

def Profile_Giao_Vien(TaiKhoan):
    gv1 = db_session.query(GiaoVien).filter(GiaoVien.TenDangNhap == TaiKhoan).first()
    gv = {"HoVaTen": gv1.HoVaTen, "GioiTinh": gv1.GioiTinh, "NgaySinh": datetime.strptime(gv1.NgaySinh,'%Y-%m-%d' ).date(), "Email": gv1.Email, "DiaChi" : gv1.DiaChi,
         "SoDienThoai": gv1.SoDienThoai, "TrinhDo":gv1.TrinhDo,"ChuyenMon": gv1.ChuyenMon, "ID_GV": gv1.IDGiaoVien, 'Quyen': gv1.Quyen}
    return gv

def gv_doi_mat_khau(TaiKhoan,matkhau_cu,matkhau_moi):
        ThongBao = ""
        gv1 = db_session.query(GiaoVien).filter(GiaoVien.TenDangNhap == TaiKhoan).first()
        if matkhau_cu != gv1.MatKhau:
            ThongBao = "Mật khẩu không khớp"
        else:
            gv1.MatKhau = matkhau_moi
            db_session.flush()
            db_session.commit()
            ThongBao = "Đổi Mật Khẩu Thành Công"
        return ThongBao

def ten_giao_vien(taikhoan_gv):
    gv1 = db_session.query(GiaoVien).filter(GiaoVien.TenDangNhap == taikhoan_gv).first()
    return gv1.HoVaTen
