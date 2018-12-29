# -*- coding: utf-8 -*-
from config import db


class CounselorOrderAmountCheck(db.Model):
    __tablename__ = "counselor_order_amount_check"

    amount_id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(30))
    payment_stage = db.Column(db.SmallInteger)
    payment_id = db.Column(db.SmallInteger)
    payment_name = db.Column(db.String(20))
    payment_bank = db.Column(db.String(40))
    payment_account = db.Column(db.String(20))
    payment_trade_no = db.Column(db.String(100))
    payment_money = db.Column(db.Numeric(15, 2))
    payment_confirm_time = db.Column(db.DateTime)
    payment_time = db.Column(db.DateTime)
    payment_status = db.Column(db.SmallInteger)
    payment_create_time = db.Column(db.DateTime)
    check_status = db.Column(db.SmallInteger)
    check_person = db.Column(db.String(20))
    check_time = db.Column(db.DateTime)
    check_remark = db.Column(db.String(100))
    service_no = db.Column(db.String(64))

    def __init__(self, order_no, payment_stage, payment_id, payment_name, payment_bank, payment_account,
                 payment_trade_no, payment_money, payment_confirm_time, payment_time, payment_status,
                 payment_create_time, check_status, check_person, check_time, check_remark, service_no):
        '''Constructor'''
        self.order_no = order_no
        self.payment_stage = payment_stage
        self.payment_id = payment_id
        self.payment_name = payment_name
        self.payment_bank = payment_bank
        self.payment_account = payment_account
        self.payment_trade_no = payment_trade_no
        self.payment_money = payment_money
        self.payment_confirm_time = payment_confirm_time
        self.payment_time = payment_time
        self.payment_status = payment_status
        self.payment_create_time = payment_create_time
        self.check_status = check_status
        self.check_person = check_person
        self.check_time = check_time
        self.check_remark = check_remark
        self.service_no = service_no

    def __repr__(self):
        return 'amount_id : %s' % self.amount_id


# Client and database attributes dictionary
clinetHead = {u'amountId', u'orderNo', u'paymentStage', u'paymentId', u'paymentName', u'paymentBank', u'paymentAccount',
              u'paymentTradeNo', u'paymentMoney', u'paymentConfirmTime', u'paymentTime', u'paymentStatus',
              u'paymentCreateTime', u'checkStatus', u'checkPerson', u'checkTime', u'checkRemark', u'serviceNo'}
CounselorOrderAmountCheckChangeDic = {
    "amountId": "amount_id",
    "orderNo": "order_no",
    "paymentStage": "payment_stage",
    "paymentId": "payment_id",
    "paymentName": "payment_name",
    "paymentBank": "payment_bank",
    "paymentAccount": "payment_account",
    "paymentTradeNo": "payment_trade_no",
    "paymentMoney": "payment_money",
    "paymentConfirmTime": "payment_confirm_time",
    "paymentTime": "payment_time",
    "paymentStatus": "payment_status",
    "paymentCreateTime": "payment_create_time",
    "checkStatus": "check_status",
    "checkPerson": "check_person",
    "checkTime": "check_time",
    "checkRemark": "check_remark",
    "serviceNo": "service_no"
}

intList = {u'amountId', u'paymentStage', u'paymentId', u'paymentStatus', u'checkStatus'}

# db.create_all()
