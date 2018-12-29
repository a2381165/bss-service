# -*- coding: utf-8 -*-
from config import db
from UserRole import UserRole


class User(db.Model):
    __tablename__ = "boss_user"

    admin_id = db.Column(db.Integer, primary_key=True, nullable=False)
    admin_name = db.Column(db.String(50))
    admin_token = db.Column(db.Text)
    admin_refresh_token = db.Column(db.Text)
    admin_salt = db.Column(db.String(20))
    admin_password = db.Column(db.String(35))
    admin_desc = db.Column(db.Text)
    admin_real_name = db.Column(db.String(50))
    admin_telephone = db.Column(db.String(20))
    admin_email = db.Column(db.String(30))
    admin_add_time = db.Column(db.DateTime)
    is_lock = db.Column(db.SmallInteger)
    oz_id = db.Column(db.Integer)
    # adminRole = db.relationship(UserRole, backref='admin', lazy='dynamic')

    def __init__(self, admin_name, admin_token, admin_refresh_token, admin_salt, admin_password, admin_desc,
                 admin_real_name, admin_telephone, admin_email, admin_add_time, is_lock, oz_id):
        '''Constructor'''
        self.admin_name = admin_name
        self.admin_token = admin_token
        self.admin_refresh_token = admin_refresh_token
        self.admin_salt = admin_salt
        self.admin_password = admin_password
        self.admin_desc = admin_desc
        self.admin_real_name = admin_real_name
        self.admin_telephone = admin_telephone
        self.admin_email = admin_email
        self.admin_add_time = admin_add_time
        self.is_lock = is_lock
        self.oz_id = oz_id

    def __repr__(self):
        return 'admin_id : %s' % self.admin_id


# Client and database attributes dictionary
clinetHead = {u'adminId', u'adminName', u'adminToken', u'adminRefreshToken', u'adminSalt', u'adminPassword',
              u'adminDesc', u'adminRealName', u'adminTelephone', u'adminEmail', u'adminAddTime', u'isLock', u'ozId'}
tableChangeDic = {
    "adminId": "admin_id",
    "adminName": "admin_name",
    "adminToken": "admin_token",
    "adminRefreshToken": "admin_refresh_token",
    "adminSalt": "admin_salt",
    "adminPassword": "admin_password",
    "adminDesc": "admin_desc",
    "adminRealName": "admin_real_name",
    "adminTelephone": "admin_telephone",
    "adminEmail": "admin_email",
    "adminAddTime": "admin_add_time",
    "isLock": "is_lock",
    "ozId": "oz_id"
}

intList = {u'adminId', u'isLock', u'ozId'}

# db.create_all()
