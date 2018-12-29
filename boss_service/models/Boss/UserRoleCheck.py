# -*- coding: utf-8 -*-
from config import db


class UserRoleCheck(db.Model):
    __tablename__ = "boss_user_role_check"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    check_status = db.Column(db.SmallInteger)
    check_person = db.Column(db.String(20))
    check_remark = db.Column(db.String(200))
    check_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime)
    role_type = db.Column(db.SmallInteger)

    def __init__(self, user_id, role_id, check_status, check_person, check_remark, check_time, create_time,role_type):
        '''Constructor'''
        self.user_id = user_id
        self.role_id = role_id
        self.check_status = check_status
        self.check_person = check_person
        self.check_remark = check_remark
        self.check_time = check_time
        self.create_time = create_time
        self.role_type = role_type

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'userId', u'roleId', u'checkStatus', u'checkPerson', u'checkRemark', u'checkTime', u'createTime'}
tableChangeDic = {
    "id": "id",
    "userId": "user_id",
    "roleId": "role_id",
    "checkStatus": "check_status",
    "checkPerson": "check_person",
    "checkRemark": "check_remark",
    "checkTime": "check_time",
    "createTime": "create_time",
    "roleType": "role_type"
}

intList = {u'id', u'userId', u'roleId', u'checkStatus',"roleType"}

# db.create_all()
