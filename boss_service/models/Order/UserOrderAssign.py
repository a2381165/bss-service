# -*- coding: utf-8 -*-
from config import db


class UserOrderAssign(db.Model):
    __tablename__ = "zzh_user_order_assign"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    counselor_id = db.Column(db.Integer)
    manage_counselor_id = db.Column(db.Integer)
    assign_status = db.Column(db.SmallInteger)
    assign_person = db.Column(db.String(20))
    assign_time = db.Column(db.DateTime)
    remark = db.Column(db.String(255))
    is_send = db.Column(db.SmallInteger)
    accept_status = db.Column(db.SmallInteger)
    return_remark = db.Column(db.String(255))

    def __init__(self, order_no, service_no, counselor_id, manage_counselor_id, assign_status, assign_person,
                 assign_time, remark, is_send, accept_status, return_remark):
        '''Constructor'''
        self.order_no = order_no
        self.service_no = service_no
        self.counselor_id = counselor_id
        self.manage_counselor_id = manage_counselor_id
        self.assign_status = assign_status
        self.assign_person = assign_person
        self.assign_time = assign_time
        self.remark = remark
        self.is_send = is_send
        self.accept_status = accept_status
        self.return_remark = return_remark

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'serviceNo', u'counselorId', u'manageCounselorId', u'assignStatus', u'assignPerson',
              u'assignTime', u'remark', u'isSend', u'acceptStatus', u'returnRemark'}
UserOrderAssignChangeDic = {
    "id": "id",
    "orderNo": "order_no",
    "serviceNo": "service_no",
    "counselorId": "counselor_id",
    "manageCounselorId": "manage_counselor_id",
    "assignStatus": "assign_status",
    "assignPerson": "assign_person",
    "assignTime": "assign_time",
    "remark": "remark",
    "isSend": "is_send",
    "acceptStatus": "accept_status",
    "returnRemark": "return_remark"
}

intList = {u'id', u'counselorId', u'manageCounselorId', u'assignStatus', u'isSend', u'acceptStatus'}

# db.create_all()
