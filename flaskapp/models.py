from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()           #SQLAlchemy를 사용해 데이터베이스 저장

class Users(db.Model): 
    __tablename__ = 'users'   #테이블 이름
    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    userid = db.Column(db.String(32))       
    password = db.Column(db.String(64))     
    username = db.Column(db.String(8))
    birthday_year = db.Column(db.String(5))
    birthday_month = db.Column(db.String(5))
    birthday_day = db.Column(db.String(5))
    sex = db.Column(db.String(3))
    phone = db.Column(db.String(15))