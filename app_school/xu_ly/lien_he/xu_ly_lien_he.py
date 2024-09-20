from flask import  url_for
import json
import os
import sqlite3

Thu_muc_du_lieu ="app_school/du_lieu/"

def Them_lien_he(Danh_sach_info) :
    conn = sqlite3.connect(Thu_muc_du_lieu + "ql_truong_hoc.db")
    sql = "INSERT INTO LienHe (Nguoi_Gui,Email,Noi_Dung) \
            VALUES (?,?,?)"
    if conn.execute(sql,(Danh_sach_info[0],Danh_sach_info[1],Danh_sach_info[2])) :
        print("Đã thêm liên hệ thành công !")
    conn.commit()
    conn.close()
