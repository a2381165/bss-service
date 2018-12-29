
# -*- coding: utf-8 -*-
from config import db


class UserOrderAmountCheck(db.Model):
    __tablename__ = "zzh_user_order_amount_check"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    payment_id = db.Column(db.Integer)
    payment_name = db.Column(db.String(20))
    trade_no = db.Column(db.String(100))
    payment_fee = db.Column(db.Numeric(5,2))
    payment_status = db.Column(db.SmallInteger)
    payment_time = db.Column(db.DateTime)
    check_status = db.Column(db.SmallInteger)
    check_person = db.Column(db.String(20))
    check_time = db.Column(db.DateTime)
    check_remark = db.Column(db.String(100))

    def __init__(self, id,order_no,payment_id,payment_name,trade_no,payment_fee,payment_status,payment_time,check_status,check_person,check_time,check_remark):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.payment_id=payment_id
        self.payment_name=payment_name
        self.trade_no=trade_no
        self.payment_fee=payment_fee
        self.payment_status=payment_status
        self.payment_time=payment_time
        self.check_status=check_status
        self.check_person=check_person
        self.check_time=check_time
        self.check_remark=check_remark


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'paymentId', u'paymentName', u'tradeNo', u'paymentFee', u'paymentStatus', u'paymentTime', u'checkStatus', u'checkPerson', u'checkTime', u'checkRemark'}
UserOrderAmountCheckChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "paymentId":"payment_id",
    "paymentName":"payment_name",
    "tradeNo":"trade_no",
    "paymentFee":"payment_fee",
    "paymentStatus":"payment_status",
    "paymentTime":"payment_time",
    "checkStatus":"check_status",
    "checkPerson":"check_person",
    "checkTime":"check_time",
    "checkRemark":"check_remark"
}

intList = {u'id', u'paymentId', u'paymentStatus', u'checkStatus'}

# db.create_all()
