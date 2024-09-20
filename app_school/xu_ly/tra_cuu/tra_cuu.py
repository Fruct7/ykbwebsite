from flask import url_for
import json
import os
import sqlite3

Thu_muc_du_lieu ="app_school/du_lieu/"
# Đọc danh sách - tra cứu học sinh
def Doc_danh_sach_hs_CSDL():
    conn = sqlite3.connect(Thu_muc_du_lieu + "ql_truong_hoc.db")
    list_dshs = []
    cursor = conn.execute("SELECT * FROM HocSinh")
    for row in cursor:        
        list_dshs.append(row)          
    conn.commit()
    conn.close()
    return list_dshs

def Doc_danh_sach_hs():
    Danh_sach = []    
    danh_sach_hs = Doc_danh_sach_hs_CSDL()
    for HocSinh in danh_sach_hs:    
        info_hs = {}
        info_hs["IDHocSinh"] = HocSinh[0]
        info_hs["HoVaTen"] = HocSinh[1]
        info_hs["GioiTinh"] = HocSinh[2]
        info_hs["DiaChi"] = HocSinh[3]
        info_hs["Email"] = HocSinh[4]
        info_hs["NgaySinh"] = HocSinh[5]
        info_hs["SoDienThoai"] = HocSinh[6]
        info_hs["SoDienThoaiPhuHuynh"] = HocSinh[7]
        info_hs["IDLop"] = HocSinh[8]
        info_hs["NienKhoa"] = HocSinh[9]
        Danh_sach.append(info_hs)
    return Danh_sach

def Doc_danh_sach_hs_id():
    Danh_sach = []    
    danh_sach_hs = Doc_danh_sach_hs_CSDL()
    for HocSinh in danh_sach_hs:    
        info_hs = {}
        info_hs["IDHocSinh"] = HocSinh[0]
        Danh_sach.append(info_hs)
    return Danh_sach

def Lay_info_theo_ID(ID, Danh_sach_HS):
    Danh_sach=list(filter(
        lambda HocSinh: str(ID).strip() == str(HocSinh["IDHocSinh"]).strip() ,Danh_sach_HS))
    return Danh_sach[0]

# Đọc danh sách - tra cứu điểm số

def Doc_diem_CSDL():
    conn = sqlite3.connect(Thu_muc_du_lieu + "ql_truong_hoc.db")
    list_diem = []
    cursor = conn.execute("SELECT * FROM BangDiem")
    for row in cursor:        
        list_diem.append(row)          
    conn.commit()
    conn.close()
    return list_diem

def Doc_diem():
    Danh_sach = []    
    danh_sach_diem = Doc_diem_CSDL()
    for BangDiem in danh_sach_diem:    
        info_hs = {}
        info_hs["IDBangDiem"] = BangDiem[0]
        info_hs["IDHocSinh"] = BangDiem[1]
        info_hs["IDMon"] = BangDiem[2]
        info_hs["HocKy"] = BangDiem[3]
        info_hs["_15phut_1_"] = BangDiem[4]
        info_hs["_15phut_2_"] = BangDiem[5]
        info_hs["_15phut_3_"] = BangDiem[6]
        info_hs["_45phut_1_"] = BangDiem[7]
        info_hs["_45phut_2_"] = BangDiem[8]
        info_hs["_45phut_3_"] = BangDiem[9]
        info_hs["TrungBinhMon"] = BangDiem[10]
        info_hs["GhiChu"] = BangDiem[11]
        Danh_sach.append(info_hs)
    return Danh_sach


def Lay_diem_theo_ID(ID, Danh_sach_diem):
    Danh_sach=list(filter(
        lambda BangDiem: str(ID).strip() == str(BangDiem["IDHocSinh"]).strip() ,Danh_sach_diem))
    return Danh_sach[0]

def Lay_diem_theo_ID_mon(ID,Danh_sach_ktra) :
    Danh_sach = []
    i = 0 
    while i < len(Danh_sach_ktra) :
        if Danh_sach_ktra[i]['IDMon'] == int(ID) :  
            info_diem = {}
            info_diem['IDBangDiem'] = Danh_sach_ktra[i]['IDBangDiem']
            info_diem['IDHocSinh'] = Danh_sach_ktra[i]['IDHocSinh']
            info_diem['IDMon'] = Danh_sach_ktra[i]['IDMon']
            info_diem['HocKy'] = Danh_sach_ktra[i]['HocKy']
            info_diem['_15phut_1_'] = Danh_sach_ktra[i]['_15phut_1_']
            info_diem['_15phut_2_'] = Danh_sach_ktra[i]['_15phut_2_']
            info_diem['_15phut_3_'] = Danh_sach_ktra[i]['_15phut_3_']
            info_diem['_45phut_1_'] = Danh_sach_ktra[i]['_45phut_1_']
            info_diem['_45phut_2_'] = Danh_sach_ktra[i]['_45phut_2_']
            info_diem['_45phut_3_'] = Danh_sach_ktra[i]['_45phut_3_']
            info_diem['TrungBinhMon'] = Danh_sach_ktra[i]['TrungBinhMon']
            info_diem['GhiChu'] = Danh_sach_ktra[i]['GhiChu']
            Danh_sach.append(info_diem)
        i += 1
    return Danh_sach

def Lay_diem_theo_nam(Nam ,Danh_sach_ktra) :
    Danh_sach = []
    i = 0 
    while i < len(Danh_sach_ktra) :
        if Danh_sach_ktra[i]['HocKy'] == Nam :  
            info_diem = {}
            info_diem['IDBangDiem'] = Danh_sach_ktra[i]['IDBangDiem']
            info_diem['IDHocSinh'] = Danh_sach_ktra[i]['IDHocSinh']
            info_diem['IDMon'] = Danh_sach_ktra[i]['IDMon']
            info_diem['HocKy'] = Danh_sach_ktra[i]['HocKy']
            info_diem['_15phut_1_'] = Danh_sach_ktra[i]['_15phut_1_']
            info_diem['_15phut_2_'] = Danh_sach_ktra[i]['_15phut_2_']
            info_diem['_15phut_3_'] = Danh_sach_ktra[i]['_15phut_3_']
            info_diem['_45phut_1_'] = Danh_sach_ktra[i]['_45phut_1_']
            info_diem['_45phut_2_'] = Danh_sach_ktra[i]['_45phut_2_']
            info_diem['_45phut_3_'] = Danh_sach_ktra[i]['_45phut_3_']
            info_diem['TrungBinhMon'] = Danh_sach_ktra[i]['TrungBinhMon']
            info_diem['GhiChu'] = Danh_sach_ktra[i]['GhiChu']
            Danh_sach.append(info_diem)
        i += 1
    return Danh_sach

def tra_cuu_diem_theo_mon(Chuoi_Tra_cuu,Danh_sach_ktra) :
    Chuoi_Tra_cuu = Chuoi_Tra_cuu.split("-")
    # Nam = Chuoi_Tra_cuu[2] + "-" + Chuoi_Tra_cuu[3]
    Danh_sach_chon_mon = Lay_diem_theo_ID_mon( Chuoi_Tra_cuu[1] , Danh_sach_ktra )
    # Danh_sach_chon_mon = Lay_diem_theo_nam( Nam , Danh_sach_chon_mon )
    Danh_sach_xem = Lay_diem_theo_ID( Chuoi_Tra_cuu[0] , Danh_sach_chon_mon )

    return Danh_sach_xem


# Danh_sach_ktra = Doc_diem()
# print(Danh_sach_ktra)
# Chuoi_Tra_cuu = "2-1-2018-2019"
# Danh_sach_hien_thi = tra_cuu_diem_theo_mon(Chuoi_Tra_cuu , Danh_sach_ktra)   
# print(Danh_sach_hien_thi) 

# Chuoi_Tra_cuu=Chuoi_Tra_cuu.split("-")
# Nam = Chuoi_Tra_cuu[2] + "-" + Chuoi_Tra_cuu[3]
# Danh_sach_chon_mon = Lay_diem_theo_ID_mon( Chuoi_Tra_cuu[1] , Danh_sach_ktra )
# print(Danh_sach_chon_mon)
# Danh_sach_chon_mon_theo_nam = Lay_diem_theo_nam( Nam , Danh_sach_chon_mon )
# print(Danh_sach_chon_mon_theo_nam)
# Danh_sach_xem = Lay_diem_theo_ID( Chuoi_Tra_cuu[0] , Danh_sach_chon_mon_theo_nam )
# print(Danh_sach_xem)


