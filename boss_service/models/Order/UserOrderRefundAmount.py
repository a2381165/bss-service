
# -*- coding: utf-8 -*-
from config import db


class UserOrderRefundAmount(db.Model):
    __tablename__ = "zzh_user_order_refund_amount"

    amount_id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    payment_id = db.Column(db.Integer)
    refund_status = db.Column(db.SmallInteger)
    refund_time = db.Column(db.DateTime)
    out_refund_no = db.Column(db.String(64))
    total_fee = db.Column(db.Numeric(10,2))
    refund_fee = db.Column(db.Numeric(10,2))

    def __init__(self, amount_id,order_no,payment_id,refund_status,refund_time,out_refund_no,total_fee,refund_fee):
        '''Constructor'''
        self.amount_id=amount_id
        self.order_no=order_no
        self.payment_id=payment_id
        self.refund_status=refund_status
        self.refund_time=refund_time
        self.out_refund_no=out_refund_no
        self.total_fee=total_fee
        self.refund_fee=refund_fee


    def __repr__(self):
        return 'amount_id : %s' % self.amount_id


# Client and database attributes dictionary
clinetHead = {u'amountId', u'orderNo', u'paymentId', u'refundStatus', u'refundTime', u'outRefundNo', u'totalFee', u'refundFee'}
UserOrderRefundAmountChangeDic = {
    "amountId":"amount_id",
    "orderNo":"order_no",
    "paymentId":"payment_id",
    "refundStatus":"refund_status",
    "refundTime":"refund_time",
    "outRefundNo":"out_refund_no",
    "totalFee":"total_fee",
    "refundFee":"refund_fee"
}

intList = {u'amountId', u'paymentId', u'refundStatus'}

# db.create_all()
