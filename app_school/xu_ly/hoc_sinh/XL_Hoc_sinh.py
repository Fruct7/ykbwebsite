from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import HocSinh, Lop, NienKhoa, BangDiem
from app_school.xu_ly.bang_diem.XL_Bang_diem import diem_trung_binh_theo_hoc_sinh
from datetime import datetime

def doc_danh_sach_hoc_sinh_theo_lop(lop): # select field tupple choice
    ds_hoc_sinh = []
    try:
        ds_hs = db_session.query(HocSinh).filter(HocSinh.IDLop == lop).all()
        for hoc_sinh in ds_hs:
            hs = hoc_sinh.__dict__
            del hs['_sa_instance_state']
            lop_hoc = db_session.query(Lop).filter(Lop.IDLop == lop).one()
            nien_khoa = db_session.query(NienKhoa).filter(NienKhoa.ID == hs['IDNienKhoa']).one()
            hs['Ten_Lop'] = lop_hoc.TenLop
            hs['Ten_Nien_khoa'] = nien_khoa.NamNienKhoa
            ds_hoc_sinh.append(hs)
    except:
        pass
    return ds_hoc_sinh

def doc_danh_sach_bang_diem_hoc_sinh_theo_lop(lop): # select field tupple choice
    ds_hoc_sinh = []
    try:
        ds_hs = db_session.query(HocSinh).filter(HocSinh.IDLop == lop).all()
        for hoc_sinh in ds_hs:
            hs = {}
            lop_hoc = db_session.query(Lop).filter(Lop.IDLop == lop).one()
            nien_khoa = db_session.query(NienKhoa).filter(NienKhoa.ID == hoc_sinh.IDNienKhoa).one()
            hs['IDNienKhoa'] = hoc_sinh.IDNienKhoa
            hs['IDLop'] = hoc_sinh.IDLop
            hs['IDHocSinh'] = hoc_sinh.IDHocSinh
            hs['HoVaTen'] = hoc_sinh.HoVaTen
            hs['Ten_Lop'] = lop_hoc.TenLop
            hs['Ten_Nien_khoa'] = nien_khoa.NamNienKhoa
            hs['bang_diem'] = dict(diem_trung_binh_theo_hoc_sinh(hoc_sinh.IDHocSinh))
            count = 0
            sum = 0
            for diem in hs['bang_diem'].values():
                if diem['trung_binh']:
                    count += 1
                    sum += diem['trung_binh']
            if count != 0:
                hs['trung_binh'] = sum/count
            else:
                hs['trung_binh'] = None
            if count != len(hs['bang_diem'].values()):
                hs['xep_loai'] = 'Chưa thể xếp loại học lực'
            elif hs['trung_binh'] < 5:
                hs['xep_loai'] = 'Kém'
            elif hs['trung_binh'] < 6.5:
                hs['xep_loai'] = 'Trung Bình'
            elif hs['trung_binh'] < 8:
                hs['xep_loai'] = 'Khá'
            elif hs['trung_binh'] < 10:
                hs['xep_loai'] = 'Giỏi'
            ds_hoc_sinh.append(hs)
            print(hs)
    except:
        pass
    return ds_hoc_sinh

def Profile_hoc_sinh(id_hs):
    hoc_sinh = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == id_hs).first()
    lop_hoc = db_session.query(Lop).filter(Lop.IDLop == hoc_sinh.IDLop).first()
    nien_khoa = db_session.query(NienKhoa).filter(NienKhoa.ID == hoc_sinh.IDNienKhoa).first()
    hs = {"IDHocSinh": hoc_sinh.IDHocSinh,"HoVaTen": hoc_sinh.HoVaTen, "GioiTinh": hoc_sinh.GioiTinh, "NgaySinh": datetime.strptime(hoc_sinh.NgaySinh,'%Y-%m-%d' ).date(), "Email": hoc_sinh.Email, "DiaChi" : hoc_sinh.DiaChi,
         "SoDienThoai": hoc_sinh.SoDienThoai, "SoDienThoaiPH":hoc_sinh.SoDienThoaiPhuHuynh,"Lop": lop_hoc.TenLop,"NienKhoa": nien_khoa.NamNienKhoa }
    return hs

def hs_doi_mat_khau(TaiKhoan, MatkhauCu, MatkhauMoi):
    ThongBao = ""
    hs = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == TaiKhoan).first()
    if MatkhauCu != hs.MatKhau:
        ThongBao = "Mật khẩu không khớp"
    else:
        hs.MatKhau = MatkhauMoi
        db_session.flush()
        db_session.commit()
        ThongBao = "Đổi Mật Khẩu Thành Công"
    return ThongBao
