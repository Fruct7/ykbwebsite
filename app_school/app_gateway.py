from flask import request, render_template, url_for, session, redirect
from app_school import app
from app_school.xu_ly.Xu_ly_Model import db_session, GiaoVien, HocSinh, QuanLi
from app_school.xu_ly.Xu_ly_Form import Form_Register, Form_Login
from app_school.xu_ly.tra_cuu.tra_cuu import *

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('error_page/pages-404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('error_page/pages-500.html'), 500

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index/index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get("giaovien") != None:
        return redirect('giao-vien')
    elif session.get("hocsinh") != None:
            return redirect('hoc-sinh')
    if session.get("quanli") != None :
        return redirect('quan-li')
    form = Form_Login()
    Th_Taikhoan = ''
    Th_Matkhau = ''
    error = ''
    if form.validate_on_submit():
        Th_Taikhoan = request.form['Th_Taikhoan']
        Th_Matkhau = request.form['Th_Matkhau']
        Th_Quyen = request.form['Th_Vaitro']
        try:
            if Th_Quyen == 'gv': 
                giaovien = db_session.query(GiaoVien).filter(GiaoVien.TenDangNhap == Th_Taikhoan).one()
                if giaovien.MatKhau == Th_Matkhau:
                    session['giaovien'] = Th_Taikhoan
                    return redirect(url_for('giao_vien'))
                else:
                    error = 'Tài khoản hoặc mật khẩu không đúng'
            elif Th_Quyen == 'ql': 
                quanli = db_session.query(QuanLi).filter(QuanLi.TenDangNhap == Th_Taikhoan).one()
                if quanli.MatKhau == Th_Matkhau:
                    session['quanli'] = Th_Taikhoan
                    return redirect(url_for('trang_quan_li'))
                else:
                    error = 'Tài khoản hoặc mật khẩu không đúng'   
            else:
                hocsinh = db_session.query(HocSinh).filter(HocSinh.IDHocSinh == Th_Taikhoan).one()
                if hocsinh.MatKhau == Th_Matkhau:
                    session['hocsinh'] = Th_Taikhoan
                    return redirect(url_for('hoc_sinh'))
                else:
                    error = 'Tài khoản hoặc mật khẩu không đúng'
        except Exception as e:
            print(str(e))
            pass
    return render_template("account/login.html", form=form, error=error)

@app.route('/register', methods=['GET','POST'])
def register():
    form = Form_Register()
    Th_Email = ''
    Th_Taikhoan = ''
    Th_Matkhau = ''
    error = ''
    if form.validate_on_submit():
        Th_Email = request.form['Th_Email']
        Th_Taikhoan = request.form['Th_Taikhoan']
        Th_Matkhau = request.form['Th_Matkhau']
        giaovien = GiaoVien(TenDangNhap=Th_Taikhoan, MatKhau=Th_Matkhau, Email=Th_Email)
        try:
            db_session.add(giaovien)
            db_session.commit()
            session['giaovien'] = Th_Taikhoan
            return redirect(url_for('giao_vien'))
        except Exception as e:
            db_session.rollback()
            error = 'Tài khoản đã tồn tại'
            pass
    return render_template("account/register.html", form=form, error=error)

@app.route('/lockscreen', methods=['GET','POST'])
def lockscreen():
    return render_template("account/lockscreen.html")

@app.route('/recoverpw', methods=['GET','POST'])
def recoverpw():
    if session.get("giaovien") != None:
        return redirect('giao-vien')
    return render_template("account/recoverpw.html")
