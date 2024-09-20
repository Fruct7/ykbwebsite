from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import Lop, GiaoVien, Khoi, NienKhoa

def doc_danh_sach_lop_hoc_select(): # select field tupple choice
    ds_lop = []
    try:
        ds_l = db_session.query(Lop).all()
        for lop in ds_l:
            l = (lop.IDLop,  lop.TenLop)
            ds_lop.append(l)
    except:
        pass
    return ds_lop

def doc_danh_sach_lop_hoc_nien_khoa_select(): # select field tupple choice
    ds_lop = []
    try:
        ds_l = db_session.query(Lop).all()
        for lop in ds_l:
            l = (lop.IDLop, lop.TenLop, lop.NamNienKhoa)
            ds_lop.append(l)
    except:
        pass
    return ds_lop

def doc_danh_sach_lop_hoc():
    ds_lop = []
    try:
        ds_l = db_session.query(Lop).all()
        for lop in ds_l:
            l = lop.__dict__
            del l['_sa_instance_state']
            chu_nhiem = db_session.query(GiaoVien).filter(GiaoVien.IDGiaoVien == l['GV_CN']).one()
            khoi = db_session.query(Khoi).filter(Khoi.IDKhoi == l['IDKhoi']).one()
            nien_khoa = db_session.query(NienKhoa).filter(NienKhoa.ID == l['NamNienKhoa']).one()
            l['Ten_Chu_nhiem'] = chu_nhiem.HoVaTen
            l['Ten_Khoi'] = khoi.TenKhoi
            l['Ten_Nien_khoa'] = nien_khoa.NamNienKhoa
            l['ID_nien_khoa'] = nien_khoa.ID
            ds_lop.append(l)
    except:
        pass
    return ds_lop

def doc_danh_sach_lop_hoc_theo_giao_vien(id_giao_vien): # select field tupple choice
    ds_lop = []
    try:
        ds_l = db_session.query(Lop).filter(Lop.GV_CN == id_giao_vien).all()
        for lop in ds_l:
            l = lop.__dict__
            del l['_sa_instance_state']
            chu_nhiem = db_session.query(GiaoVien).filter(GiaoVien.IDGiaoVien == l['GV_CN']).one()
            khoi = db_session.query(Khoi).filter(Khoi.IDKhoi == l['IDKhoi']).one()
            nien_khoa = db_session.query(NienKhoa).filter(NienKhoa.ID == l['NamNienKhoa']).one()
            l['Ten_Chu_nhiem'] = chu_nhiem.HoVaTen
            l['Ten_Khoi'] = khoi.TenKhoi
            l['Ten_Nien_khoa'] = nien_khoa.NamNienKhoa
            l['ID_nien_khoa'] = nien_khoa.ID
            ds_lop.append(l)
    except:
        pass
    return ds_lop

def lay_nien_khoa_theo_lop(lop):
    try:
        lop = db_session.query(Lop).filter(Lop.IDLop == lop).one()
        nien_khoa = db_session.query(NienKhoa).filter(NienKhoa.ID == lop.NamNienKhoa).one()
    except:
        pass
    return nien_khoa

def cap_nhat_si_so(lop, sl_them_giam=1):
    try:
        lop = db_session.query(Lop).filter(Lop.IDLop == lop).one()
        lop.TongSoHS += sl_them_giam
        db_session.flush()
        db_session.commit()
    except:
        db_session.rollback()
        return False
    return True

def ten_lop(lop):
    lop = db_session.query(Lop).filter(Lop.IDLop == lop).first()
    return lop.TenLop