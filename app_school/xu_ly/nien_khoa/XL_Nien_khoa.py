from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import NienKhoa

def doc_danh_sach_nien_khoa_select(): # select field tupple choice
    ds_nien_khoa = []
    try:
        ds_nk = db_session.query(NienKhoa).all()
        for nien_khoa in ds_nk:
            nk = (nien_khoa.ID,  nien_khoa.NamNienKhoa)
            ds_nien_khoa.append(nk)
    except:
        pass
    return ds_nien_khoa
    
def ten_nien_khoa(ID_NienKhoa):
    nien_khoa = db_session.query(NienKhoa).filter(NienKhoa.ID == ID_NienKhoa).first()
    return nien_khoa.NamNienKhoa