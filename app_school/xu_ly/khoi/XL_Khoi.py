from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import Khoi

def doc_danh_sach_khoi_select(): # select field tupple choice
    ds_khoi = []
    try:
        ds_k = db_session.query(Khoi).all()
        for khoi in ds_k:
            k = (khoi.IDKhoi,  khoi.TenKhoi)
            ds_khoi.append(k)
    except:
        pass
    return ds_khoi