# -*- coding: utf-8 -*-
from config import db


class UserLog(db.Model):
    __tablename__ = "boss_user_log"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer)
    admin_name = db.Column(db.String(50))
    log_group = db.Column(db.SmallInteger)
    log_ip = db.Column(db.String(30))
    log_action = db.Column(db.String(100))
    log_remark = db.Column(db.Text)
    log_add_time = db.Column(db.DateTime)

    def __init__(self, user_id, admin_name, log_group, log_ip, log_action, log_remark, log_add_time):
        '''Constructor'''
        self.user_id = user_id
        self.admin_name = admin_name
        self.log_group = log_group
        self.log_ip = log_ip
        self.log_action = log_action
        self.log_remark = log_remark
        self.log_add_time = log_add_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'userId', u'adminName', u'logGroup', u'logIp', u'logAction', u'logRemark', u'logAddTime'}
tableChangeDic = {
    "id": "id",
    "userId": "user_id",
    "adminName": "admin_name",
    "logGroup": "log_group",
    "logIp": "log_ip",
    "logAction": "log_action",
    "logRemark": "log_remark",
    "logAddTime": "log_add_time"
}

intList = {u'id', u'userId', u'logGroup'}

# db.create_all()
