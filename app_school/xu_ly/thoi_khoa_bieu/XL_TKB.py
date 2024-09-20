from app_school import app, db_session
from app_school.xu_ly.Xu_ly_Model import *
import json


def ten_giao_vien(id_giao_vien):
    gv = db_session.query(GiaoVien).filter(
        GiaoVien.IDGiaoVien == id_giao_vien).first()
    return gv.HoVaTen


def ten_mon(id_mon):
    mon = db_session.query(Mon).filter(Mon.IDMon == id_mon).first()
    return mon.TenMon


def ten_nien_khoa(id_nien_khoa):
    nien_khoa = db_session.query(NienKhoa).filter(
        NienKhoa.ID == id_nien_khoa).first()
    return nien_khoa.NamNienKhoa

def ten_lop(id_lop):
    lop = db_session.query(Lop).filter(
    Lop.IDLop == id_lop).first()
    return lop.TenLop


def doc_thong_tin_chi_tiet_tkb(id_nien_khoa, id_lop, id_thu, id_buoi, id_tiet):
    chi_tiet_tkb = db_session.query(ThoiKhoaBieu).filter(ThoiKhoaBieu.ID_Nien_khoa == id_nien_khoa,
                                                         ThoiKhoaBieu.Thu == id_thu,
                                                         ThoiKhoaBieu.Buoi == id_buoi,
                                                         ThoiKhoaBieu.Tiet == id_tiet).all()
    return chi_tiet_tkb

def doc_thong_tin_chi_tiet_tkb_theo_lop(id_nien_khoa, id_lop, id_thu, id_buoi, id_tiet):
    chi_tiet_tkb = db_session.query(ThoiKhoaBieu).filter(ThoiKhoaBieu.ID_Nien_khoa == id_nien_khoa,
                                                        ThoiKhoaBieu.ID_Lop == id_lop,
                                                        ThoiKhoaBieu.Thu == id_thu,
                                                        ThoiKhoaBieu.Buoi == id_buoi,
                                                        ThoiKhoaBieu.Tiet == id_tiet).first()
    return chi_tiet_tkb

def doc_thong_tin_chi_tiet_tkb_theo_gv(id_nien_khoa, id_gv, id_thu, id_buoi, id_tiet):
    chi_tiet_tkb = db_session.query(ThoiKhoaBieu).filter(ThoiKhoaBieu.ID_Nien_khoa == id_nien_khoa,
                                                        ThoiKhoaBieu.ID_Giao_vien == id_gv,
                                                        ThoiKhoaBieu.Thu == id_thu,
                                                        ThoiKhoaBieu.Buoi == id_buoi,
                                                        ThoiKhoaBieu.Tiet == id_tiet).first()
    return chi_tiet_tkb

def them_thoi_khoa_bieu(thoi_khoa_bieu):
    try:
        db_session.add(thoi_khoa_bieu)
        db_session.commit()
    except:
        db_session.rollback()
        return False
    return True

def tao_thoi_khoa_bieu_rong():
    tkb = [
            [ #   2   3   4   5   6   7
                ['-','-','-','-','-','-'], # 1
                ['-','-','-','-','-','-'], # 2
                ['-','-','-','-','-','-'], # 3
                ['-','-','-','-','-','-']  # 4
            ],
            [
                ['-','-','-','-','-','-'],
                ['-','-','-','-','-','-'],
                ['-','-','-','-','-','-'],
                ['-','-','-','-','-','-']
            ]
        ]
    return tkb

def doc_thoi_khoa_bieu(id_nien_khoa, id_lop):
    tkb = tao_thoi_khoa_bieu_rong()
    for i in range(0,2):
        for j in range(0,4):
            for g in range(0,6):
                tkb_chi_tiet = doc_thong_tin_chi_tiet_tkb_theo_lop(id_nien_khoa,id_lop,g+2,i+1,j+1)
                if tkb_chi_tiet != None:
                    tkb[i][j][g] = ten_lop(tkb_chi_tiet.ID_Lop) + ' - ' + ten_giao_vien(tkb_chi_tiet.ID_Giao_vien) + ' - ' + ten_mon(tkb_chi_tiet.ID_Mon)
    return tkb

def doc_thoi_khoa_bieu_gv(id_nien_khoa, id_giao_vien):
    tkb = tao_thoi_khoa_bieu_rong()
    for i in range(0,2):
        for j in range(0,4):
            for g in range(0,6):
                tkb_chi_tiet = doc_thong_tin_chi_tiet_tkb_theo_gv(id_nien_khoa,id_giao_vien,g+2,i+1,j+1)
                if tkb_chi_tiet != None:
                    tkb[i][j][g] = ten_lop(tkb_chi_tiet.ID_Lop) + ' - '  + ten_mon(tkb_chi_tiet.ID_Mon)
    return tkb

def doc_thoi_khoa_bieu_hs(id_nien_khoa, id_lop):
    tkb = tao_thoi_khoa_bieu_rong()
    for i in range(0,2):
        for j in range(0,4):
            for g in range(0,6):
                tkb_chi_tiet = doc_thong_tin_chi_tiet_tkb_theo_lop(id_nien_khoa,id_lop,g+2,i+1,j+1)
                if tkb_chi_tiet != None:
                    tkb[i][j][g] = ten_giao_vien(tkb_chi_tiet.ID_Giao_vien) + ' - ' + ten_mon(tkb_chi_tiet.ID_Mon)
    return tkb