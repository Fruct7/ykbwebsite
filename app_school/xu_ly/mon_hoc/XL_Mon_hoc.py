from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import  Mon

def doc_danh_sach_mon_hoc(): # select field tupple choice
    ds_mon = []
    try:
        ds_m = db_session.query(Mon).all()
        for mon in ds_m:
            m = (mon.IDMon, mon.TenMon)
            ds_mon.append(m)
    except:
        pass
    return ds_mon

def lay_ten_mon(id_mon):
    ten_mon = None
    try:
        mon = db_session.query(Mon).filter(Mon.IDMon == id_mon).one()
    except:
        pass
    return mon.TenMon