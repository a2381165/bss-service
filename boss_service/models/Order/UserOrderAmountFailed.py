
# -*- coding: utf-8 -*-
from config import db


class UserOrderAmountFailed(db.Model):
    __tablename__ = "zzh_user_order_amount_failed"

    amount_id = db.Column(db.Integer, primary_key=True, nullable=False)
    payment_id = db.Column(db.Integer)
    payment_info_remark = db.Column(db.Text)
    payment_time = db.Column(db.DateTime)

    def __init__(self, amount_id,payment_id,payment_info_remark,payment_time):
        '''Constructor'''
        self.amount_id=amount_id
        self.payment_id=payment_id
        self.payment_info_remark=payment_info_remark
        self.payment_time=payment_time


    def __repr__(self):
        return 'amount_id : %s' % self.amount_id


# Client and database attributes dictionary
clinetHead = {u'amountId', u'paymentId', u'paymentInfoRemark', u'paymentTime'}
UserOrderAmountFailedChangeDic = {
    "amountId":"amount_id",
    "paymentId":"payment_id",
    "paymentInfoRemark":"payment_info_remark",
    "paymentTime":"payment_time"
}

intList = {u'amountId', u'paymentId'}

# db.create_all()
