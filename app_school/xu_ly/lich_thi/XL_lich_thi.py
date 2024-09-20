from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import *

def Ten_Mon(ID_Mon):
    Mon_Hoc = db_session.query(Mon).filter(Mon.IDMon == ID_Mon).first()
    return  Mon_Hoc.TenMon    


def load_lich_thi(id_nien_khoa,id_khoi):
    lich_thi = db_session.query(LichThi).filter(LichThi.ID_Nien_khoa == id_nien_khoa, LichThi.ID_Khoi == id_khoi).all()
    lst = []
    for i in lich_thi:
        t = {}
        t['ID_Mon']  = Ten_Mon(i.ID_Mon)
        t['Mon'] = i.ID_Mon
        t['NienKhoa'] = id_nien_khoa
        t['Khoi'] = id_khoi
        t['ThoiGianThi'] = i.ThoiGianThi
        t['ThoiGianLamBai'] = i.ThoiGianLamBai
        
        lst.append(t)
    return lst
    

def Them_Lich_Thi(lich_thi):
    _lich_ = db_session.query(LichThi).filter(LichThi.ID_Khoi == lich_thi.ID_Khoi, LichThi.ID_Nien_khoa == lich_thi.ID_Nien_khoa ,LichThi.ID_Mon == lich_thi.ID_Mon).first()
    if _lich_ != None:
        return "Đã Tồn Môn Này Lịch Thi "
    else:
        db_session.add(lich_thi)
        db_session.commit()
    return  "Đã Thêm Thành Công"

def load_lich_thi_hs(id_hs):
    hs = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == id_hs).one()
    lp = db_session.query(Lop).filter(hs.IDLop == Lop.IDLop).one()
    Kh = db_session.query(Khoi).filter(Khoi.IDKhoi == lp.IDKhoi).one()
    return load_lich_thi(hs.IDNienKhoa,Kh.IDKhoi)
