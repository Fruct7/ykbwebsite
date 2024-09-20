from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table,Column,ForeignKey,Integer,String,Float,Text,Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

#create memory database
DuongDan ='sqlite:///app_school/du_lieu/ql_truong_hoc.db?check_same_thread =False' 
engine = create_engine(DuongDan)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()

class Khoi(Base):
    __tablename__ = 'Khoi'
    IDKhoi = Column(Integer, primary_key = True)
    TenKhoi = Column(String(100),  unique=True)
    def __str__(self):
        return self.TenKhoi

class Mon(Base):
    __tablename__ = 'Mon'
    IDMon = Column(Integer, primary_key = True)
    TenMon = Column(String(100),  unique=True )
    def __str__(self):
        return self.TenMon

class NienKhoa(Base):
    __tablename__ = 'NienKhoa'
    ID = Column(Integer, primary_key = True)
    NamNienKhoa = Column(String(100),  unique=True)
    def __str__(self):
        return self.NamNienKhoa

class GiaoVien(Base):
    __tablename__ = 'GiaoVien'
    IDGiaoVien = Column(Integer, primary_key = True)
    TenDangNhap = Column(String(100),  unique=True)
    MatKhau = Column(String(100) )
    HoVaTen = Column(String(100) )
    GioiTinh = Column(String(10) )
    DiaChi =  Column(String(100) )
    Email = Column(String(100) )
    NgaySinh = Column(String(30) )
    SoDienThoai = Column(String(11) )
    TrinhDo =  Column(String(100) )
    ChuyenMon = Column(String(100) )
    Quyen = Column(String(2) )
    def __init__(self, TenDangNhap=None, MatKhau=None, Email=None):
        self.TenDangNhap = TenDangNhap
        self.MatKhau = MatKhau
        self.Email = Email

    def __str__(self):
        return self.HoVaTen

class Lop(Base):
    __tablename__ = 'Lop'
    IDLop = Column(Integer, primary_key = True)
    TenLop = Column(String(100),  unique=True)
    DiaDiem = Column(String(100) )
    child = relationship("GiaoVien", backref="Lop")
    TongSoHS = Column(Float )
    NamNienKhoa = Column(String(20))

    GV_CN = Column(Integer, ForeignKey(GiaoVien.IDGiaoVien))
    FK_GiaoVien = relationship('GiaoVien', foreign_keys='Lop.GV_CN')

    IDKhoi  = Column(Integer, ForeignKey(Khoi.IDKhoi))
    FK_Khoi = relationship('Khoi', foreign_keys='Lop.IDKhoi')
    def __str__(self):
        return self.TenLop

class HocSinh(Base):
    __tablename__ = 'HocSinh'
    MatKhau = Column(String(100))
    IDHocSinh = Column(Integer, primary_key = True)
    HoVaTen = Column(String(100) )
    GioiTinh = Column(String(10) )
    DiaChi =  Column(String(100) )
    Email = Column(String(100) )
    NgaySinh = Column(String(100) )
    SoDienThoai = Column(String(11) )
    SoDienThoaiPhuHuynh = Column(String(11) )

    IDLop = Column(Integer, ForeignKey(Lop.IDLop))
    FK_Lop = relationship(Integer, foreign_keys='HocSinh.IDLop')

    IDNienKhoa = Column(Integer, ForeignKey(NienKhoa.ID))
    FK_Lop = relationship('NienKhoa', foreign_keys='HocSinh.IDNienKhoa')

    def __str__(self):
        return self.HoVaTen

class BangDiem(Base):
    __tablename__ = 'BangDiem'
    IDBangDiem = Column(Integer, primary_key = True)

    IDHocSinh = Column(Integer, ForeignKey(HocSinh.IDHocSinh))
    FK_HocSinh = relationship('HocSinh', foreign_keys='BangDiem.IDHocSinh')

    IDMon = Column(Integer, ForeignKey(Mon.IDMon))
    FK_Mon = relationship('Mon', foreign_keys='BangDiem.IDMon')
 
    HocKy = Column(Float )
    _15Phut_1_ = Column(Float )
    _15Phut_2_ = Column(Float )
    _15Phut_3_ = Column(Float )
    _45Phut_1_ = Column(Float )
    _45Phut_2_ = Column(Float )
    _45Phut_3_ = Column(Float )
    TrungBinhMon = Column(Float )
    GhiChu = Column(String(100) )
    def __str__(self):
        return self.HoVaTen


class ThoiKhoaBieu(Base):
    __tablename__ = 'ThoiKhoaBieu'
    ID_Nien_khoa = Column(Integer, ForeignKey('NienKhoa.ID'), primary_key = True)
    ID_Giao_vien = Column(Integer, ForeignKey('GiaoVien.IDGiaoVien'), primary_key = True)
    Thu = Column(Integer, primary_key = True, autoincrement=False)
    Buoi = Column(Integer, primary_key = True, autoincrement=False)
    Tiet = Column(Integer, primary_key = True, autoincrement=False)
    ID_Lop = Column(Integer, ForeignKey('Lop.IDLop'))
    ID_Mon = Column(Integer, ForeignKey('Mon.IDMon'))

class LichThi(Base):
    __tablename__ = 'LichThi'
    ID_Nien_khoa = Column(Integer, ForeignKey('NienKhoa.ID'), primary_key = True)
    ID_Khoi =  Column(Integer,ForeignKey('Khoi.IDKhoi') ,primary_key = True)
    ID_Mon = Column(Integer, ForeignKey('Mon.IDMon'),primary_key = True)
    ThoiGianThi = Column(String(100) )
    ThoiGianLamBai = Column(String(100) )

class LienHe(Base):
    __tablename__ = 'LienHe'
    Nguoi_Gui = Column(String(100))
    Email = Column( String(100)  ,primary_key = True)
    Noi_Dung = Column(String(200))


class QuanLi(Base):
    __tablename__ = 'QuanLi'
    IDQuanLi = Column(Integer, primary_key = True)
    TenDangNhap = Column(String(100),  unique=True)
    MatKhau = Column(String(100) )
    HoVaTen = Column(String(100) )
    GioiTinh = Column(String(10) )
    DiaChi =  Column(String(100) )
    Email = Column(String(100) )
    NgaySinh = Column(String(30) )
    SoDienThoai = Column(String(11) )
    def __init__(self, TenDangNhap=None, MatKhau=None, Email=None):
        self.TenDangNhap = TenDangNhap
        self.MatKhau = MatKhau
        self.Email = Email

    def __str__(self):
        return self.HoVaTen
class Hoat_Dong(Base):
    __tablename__ = 'Hoat_Dong'
    IDHoatDong = Column(Integer, primary_key = True)
    TieuDe = Column(String(200))
    GiaoVienTao =  Column(String(100),ForeignKey('GiaoVien.TenDangNhap'))
    NoiDung = Column(Text)
    ThoiHanDangKy = Column(String(20))
    Khoi_10 = Column(Boolean)
    Khoi_11 = Column(Boolean)
    Khoi_12 = Column(Boolean)
    NienKhoa = Column(Integer, ForeignKey('NienKhoa.ID'))
    SoNguoiDaThamGia  = Column(Integer)

class Tham_Gia_Hoat_Dong(Base):
    __tablename__ = 'Tham_Gia_Hoat_Dong'
    IDHoatDong = Column(Integer, primary_key = True)
    IDHocSinh = Column(Integer, ForeignKey(HocSinh.IDHocSinh),primary_key = True)
    NgayDangKy = Column(String(20))

Base.metadata.create_all(engine)
##############################################