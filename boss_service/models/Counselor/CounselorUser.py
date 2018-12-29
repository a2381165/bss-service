
# -*- coding: utf-8 -*-
from config import db


class CounselorUser(db.Model):
    __tablename__ = "counselor_user"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(50))
    user_salt = db.Column(db.String(20))
    user_password = db.Column(db.String(32))
    user_phone = db.Column(db.String(11))
    user_email = db.Column(db.String(60))
    avatar = db.Column(db.BLOB)
    nick_name = db.Column(db.String(50))
    reg_time = db.Column(db.DateTime)
    reg_ip = db.Column(db.String(30))
    is_check_phone = db.Column(db.SmallInteger)
    is_check_email = db.Column(db.SmallInteger)
    access_token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)
    reg_type = db.Column(db.SmallInteger)
    is_lock = db.Column(db.SmallInteger)

    def __init__(self, id,user_name,user_salt,user_password,user_phone,user_email,avatar,nick_name,reg_time,reg_ip,is_check_phone,is_check_email,access_token,refresh_token,reg_type,is_lock):
        '''Constructor'''
        self.id=id
        self.user_name=user_name
        self.user_salt=user_salt
        self.user_password=user_password
        self.user_phone=user_phone
        self.user_email=user_email
        self.avatar=avatar
        self.nick_name=nick_name
        self.reg_time=reg_time
        self.reg_ip=reg_ip
        self.is_check_phone=is_check_phone
        self.is_check_email=is_check_email
        self.access_token=access_token
        self.refresh_token=refresh_token
        self.reg_type=reg_type
        self.is_lock=is_lock


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'userName', u'userSalt', u'userPassword', u'userPhone', u'userEmail', u'avatar', u'nickName', u'regTime', u'regIp', u'isCheckPhone', u'isCheckEmail', u'accessToken', u'refreshToken', u'regType', u'isLock'}
CounselorUserChangeDic = {
    "id":"id",
    "userName":"user_name",
    "userSalt":"user_salt",
    "userPassword":"user_password",
    "userPhone":"user_phone",
    "userEmail":"user_email",
    "avatar":"avatar",
    "nickName":"nick_name",
    "regTime":"reg_time",
    "regIp":"reg_ip",
    "isCheckPhone":"is_check_phone",
    "isCheckEmail":"is_check_email",
    "accessToken":"access_token",
    "refreshToken":"refresh_token",
    "regType":"reg_type",
    "isLock":"is_lock"
}

intList = {u'id', u'isCheckPhone', u'isCheckEmail', u'regType', u'isLock'}

# db.create_all()
