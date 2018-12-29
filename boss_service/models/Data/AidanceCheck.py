# -*- coding: utf-8 -*-
from config import db


class AidanceCheck(db.Model):
    __tablename__ = "data_aidance_check"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    aidance_id = db.Column(db.Integer)
    submit_time = db.Column(db.DateTime)
    submit_person = db.Column(db.String(20))
    check_status = db.Column(db.SmallInteger)
    check_time = db.Column(db.DateTime)
    check_person = db.Column(db.String(20))
    check_remark = db.Column(db.String(200))
    sort = db.Column(db.SmallInteger)

    def __init__(self, aidance_id, submit_time, submit_person, check_status, check_time, check_person, check_remark,sort):
        '''Constructor'''
        self.aidance_id = aidance_id
        self.submit_time = submit_time
        self.submit_person = submit_person
        self.check_status = check_status
        self.check_time = check_time
        self.check_person = check_person
        self.check_remark = check_remark
        self.sort = sort

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'aidanceId', u'submitTime', u'submitPerson', u'checkStatus', u'checkTime', u'checkPerson',
              u'checkRemark'}
AidanceCheckChangeDic = {
    "id": "id",
    "aidanceId": "aidance_id",
    "submitTime": "submit_time",
    "submitPerson": "submit_person",
    "checkStatus": "check_status",
    "checkTime": "check_time",
    "checkPerson": "check_person",
    "checkRemark": "check_remark",
    "sort": "sort",
}

intList = [u'id', u'aidanceId', u'checkStatus',"sort"]

# db.create_all()
