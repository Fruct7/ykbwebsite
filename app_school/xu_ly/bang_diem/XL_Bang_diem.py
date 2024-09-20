from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import BangDiem, HocSinh, Mon
from app_school.xu_ly.mon_hoc.XL_Mon_hoc import doc_danh_sach_mon_hoc


def doc_danh_sach_bang_diem_hoc():  # select field tupple choice
    ds_bang_diem = []
    try:
        ds_bangdiem = db_session.query(BangDiem).all()
        for bang_diem in ds_bangdiem:
            bd = (bang_diem.IDbang_diem, bang_diem.Tenbang_diem)
            ds_bang_diem.append(bd)
    except:
        pass
    return ds_bang_diem

def cap_nhat_bang_diem(id_bang_diem, loai_diem, diem_so):
    # try:
    bang_diem = db_session.query(BangDiem).filter(BangDiem.IDBangDiem == id_bang_diem).one()
    print(bang_diem.__dict__)
    if BangDiem._15Phut_1_.name == loai_diem:
        bang_diem._15Phut_1_ = diem_so
    elif BangDiem._15Phut_2_.name == loai_diem:
        bang_diem._15Phut_2_ = diem_so
    elif BangDiem._15Phut_3_.name == loai_diem:
        bang_diem._15Phut_3_ = diem_so
    elif BangDiem._45Phut_1_.name == loai_diem:
        bang_diem._45Phut_1_ = diem_so
    elif BangDiem._45Phut_2_.name == loai_diem:
        bang_diem._45Phut_2_ = diem_so
    elif BangDiem._45Phut_3_.name == loai_diem:
        bang_diem._45Phut_3_ = diem_so
    elif BangDiem.HocKy.name == loai_diem:
        bang_diem.HocKy = diem_so
    db_session.flush()
    db_session.commit()
    # except:
        # db_session.rollback()
    pass

def doc_bang_diem_theo_id_bang_diem(id_bang_diem):
    bd = {}
    try:
        bang_diem = db_session.query(BangDiem).filter(BangDiem.IDBangDiem == id_bang_diem).one()
        mon = db_session.query(Mon).filter(Mon.IDMon == bang_diem.IDMon).one()
        bd['mon'] = mon.TenMon
        list_bang_diem = [bang_diem._15Phut_1_, bang_diem._15Phut_2_, bang_diem._15Phut_3_,
                            bang_diem._45Phut_1_, bang_diem._45Phut_1_, bang_diem._45Phut_2_,
                            bang_diem._45Phut_2_, bang_diem._45Phut_3_, bang_diem._45Phut_3_,
                            bang_diem.HocKy, bang_diem.HocKy, bang_diem.HocKy]
        bang_diem.TrungBinhMon = tinh_trung_binh(list_bang_diem)
        bd['15_phut'] = {1:bang_diem._15Phut_1_,2:bang_diem._15Phut_2_, 3:bang_diem._15Phut_3_}
        bd['45_phut'] = {1:bang_diem._45Phut_1_,2:bang_diem._45Phut_2_, 3:bang_diem._45Phut_3_}
        bd['thi'] = bang_diem.HocKy
        bd['trung_binh'] = bang_diem.TrungBinhMon
        db_session.flush()
        db_session.commit()
    except:
        db_session.rollback()
        return None
    return bd

def diem_trung_binh_theo_hoc_sinh(id_hoc_sinh):
    ds_bang_diem = {}
    try:
        ds_bangdiem = db_session.query(BangDiem).filter(BangDiem.IDHocSinh == id_hoc_sinh).all()
        for bang_diem in ds_bangdiem:
            bd = {}
            mon = db_session.query(Mon).filter(Mon.IDMon == bang_diem.IDMon).one()
            bd['id_bd'] = bang_diem.IDBangDiem
            bd['trung_binh'] = bang_diem.TrungBinhMon
            try:
                db_session.flush()
                db_session.commit()
                ds_bang_diem[mon.TenMon] = bd
            except:
                db_session.rollback()
                pass
    except:
        db_session.rollback()
        pass
    return ds_bang_diem

def doc_bang_diem_theo_hoc_sinh(id_hoc_sinh):  # select field tupple choice
    ds_bang_diem = []
    try:
        ds_bangdiem = db_session.query(BangDiem).filter(BangDiem.IDHocSinh == id_hoc_sinh).all()
        for bang_diem in ds_bangdiem:
            bd = {}
            mon = db_session.query(Mon).filter(Mon.IDMon == bang_diem.IDMon).one()
            bd['mon'] = mon.TenMon
            bd['id_bd'] = bang_diem.IDBangDiem
            list_bang_diem = [bang_diem._15Phut_1_, bang_diem._15Phut_2_, bang_diem._15Phut_3_,
                            bang_diem._45Phut_1_, bang_diem._45Phut_1_, bang_diem._45Phut_2_,
                            bang_diem._45Phut_2_, bang_diem._45Phut_3_, bang_diem._45Phut_3_,
                            bang_diem.HocKy, bang_diem.HocKy, bang_diem.HocKy]
            bang_diem.TrungBinhMon = tinh_trung_binh(list_bang_diem)
            bd['15_phut'] = {1:bang_diem._15Phut_1_,2:bang_diem._15Phut_2_, 3:bang_diem._15Phut_3_}
            bd['45_phut'] = {1:bang_diem._45Phut_1_,2:bang_diem._45Phut_2_, 3:bang_diem._45Phut_3_}
            bd['thi'] = bang_diem.HocKy
            bd['trung_binh'] = bang_diem.TrungBinhMon
            print(bd)
            try:
                db_session.flush()
                db_session.commit()
                ds_bang_diem.append(bd)
            except:
                db_session.rollback()
                pass
    except:
        db_session.rollback()
        pass
    return ds_bang_diem

def tinh_trung_binh(list_bang_diem):
    count = 0; tong = 0
    for diem in list_bang_diem:
        if diem != None:
            count += 1
            tong += diem
    if count == 0:
        return None
    else:
        return float(tong/count)

def tao_bang_diem_cho_hoc_sinh(id_hoc_sinh):
    for mon in doc_danh_sach_mon_hoc():
        IDHocSinh = id_hoc_sinh
        IDMon = mon[0] 
        HocKy = None
        _15Phut_1_ = None
        _15Phut_2_ = None
        _15Phut_3_ = None
        _45Phut_1_ = None
        _45Phut_2_ = None
        _45Phut_3_ = None
        TrungBinhMon = None
        GhiChu = None
        bang_diem = BangDiem(IDHocSinh=IDHocSinh, IDMon=IDMon)
        try:
            db_session.add(bang_diem)
            db_session.commit()
        except:
            db_session.rollback()
            return False
    return True
