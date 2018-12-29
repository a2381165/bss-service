# -*- coding: utf-8 -*-
from config import db


class UserOrderCancel(db.Model):
    __tablename__ = "zzh_user_order_cancel"

    cancel_id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    cancel_type = db.Column(db.SmallInteger)
    cancel_reason = db.Column(db.String(255))
    cancel_time = db.Column(db.DateTime)
    cancel_ip = db.Column(db.String(255))
    check_status = db.Column(db.SmallInteger)
    check_person = db.Column(db.String(255))
    check_time = db.Column(db.DateTime)
    check_remark = db.Column(db.String(255))

    def __init__(self, order_no, cancel_type, cancel_reason, cancel_time, cancel_ip, check_status, check_person,
                 check_time, check_remark):
        '''Constructor'''
        self.order_no = order_no
        self.cancel_type = cancel_type
        self.cancel_reason = cancel_reason
        self.cancel_time = cancel_time
        self.cancel_ip = cancel_ip
        self.check_status = check_status
        self.check_person = check_person
        self.check_time = check_time
        self.check_remark = check_remark

    def __repr__(self):
        return 'cancel_id : %s' % self.cancel_id


# Client and database attributes dictionary
clinetHead = {u'cancelId', u'orderNo', u'cancelType', u'cancelReason', u'cancelTime', u'cancelIp', u'checkStatus',
              u'checkPerson', u'checkTime', u'checkRemark'}
UserOrderCancelChangeDic = {
    "cancelId": "cancel_id",
    "orderNo": "order_no",
    "cancelType": "cancel_type",
    "cancelReason": "cancel_reason",
    "cancelTime": "cancel_time",
    "cancelIp": "cancel_ip",
    "checkStatus": "check_status",
    "checkPerson": "check_person",
    "checkTime": "check_time",
    "checkRemark": "check_remark"
}

intList = {u'cancelId', u'cancelType', u'checkStatus'}

# db.create_all()
