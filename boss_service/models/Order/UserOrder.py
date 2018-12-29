# -*- coding: utf-8 -*-
from config import db


class UserOrder(db.Model):
    __tablename__ = "zzh_user_order"

    order_id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    order_type = db.Column(db.SmallInteger)
    order_from = db.Column(db.String(20))
    order_status = db.Column(db.SmallInteger)
    declare_status = db.Column(db.String(10))
    order_add_ip = db.Column(db.String(26))
    order_add_time = db.Column(db.DateTime)
    service_id = db.Column(db.Integer)
    contact_person = db.Column(db.String(100))
    contact_phone = db.Column(db.String(11))
    contact_email = db.Column(db.String(255))
    order_message = db.Column(db.String(255))
    order_amount = db.Column(db.Numeric(8, 2))
    payable_amount = db.Column(db.Numeric(8, 2))
    real_amount = db.Column(db.Numeric(8, 2))
    order_point = db.Column(db.Integer)
    is_coupon = db.Column(db.SmallInteger)
    is_invoice = db.Column(db.SmallInteger)
    is_comment = db.Column(db.SmallInteger)
    user_id = db.Column(db.Integer)

    def __init__(self, order_no, order_type, order_from, order_status, declare_status, order_add_ip, order_add_time,
                 service_id, contact_person, contact_phone, contact_email, order_message, order_amount, payable_amount,
                 real_amount, order_point, is_coupon, is_invoice, is_comment, user_id):
        '''Constructor'''
        self.order_no = order_no
        self.order_type = order_type
        self.order_from = order_from
        self.order_status = order_status
        self.declare_status = declare_status
        self.order_add_ip = order_add_ip
        self.order_add_time = order_add_time
        self.service_id = service_id
        self.contact_person = contact_person
        self.contact_phone = contact_phone
        self.contact_email = contact_email
        self.order_message = order_message
        self.order_amount = order_amount
        self.payable_amount = payable_amount
        self.real_amount = real_amount
        self.order_point = order_point
        self.is_coupon = is_coupon
        self.is_invoice = is_invoice
        self.is_comment = is_comment
        self.user_id = user_id

    def __repr__(self):
        return 'order_id : %s' % self.order_id


# Client and database attributes dictionary
clinetHead = ['orderId', 'orderNo', 'orderType', 'orderFrom', 'orderStatus', 'declareStatus', 'orderAddIp',
              'orderAddTime', 'serviceId', 'contactPerson', 'contactPhone', 'contactEmail', 'orderMessage',
              'orderAmount', 'payableAmount', 'realAmount', 'orderPoint', 'isCoupon', 'isInvoice', 'isComment',
              'userId']
UserOrderChangeDic = {
    "orderId": "order_id",
    "orderNo": "order_no",
    "orderType": "order_type",
    "orderFrom": "order_from",
    "orderStatus": "order_status",
    "declareStatus": "declare_status",
    "orderAddIp": "order_add_ip",
    "orderAddTime": "order_add_time",
    "serviceId": "service_id",
    "contactPerson": "contact_person",
    "contactPhone": "contact_phone",
    "contactEmail": "contact_email",
    "orderMessage": "order_message",
    "orderAmount": "order_amount",
    "payableAmount": "payable_amount",
    "realAmount": "real_amount",
    "orderPoint": "order_point",
    "isCoupon": "is_coupon",
    "isInvoice": "is_invoice",
    "isComment": "is_comment",
    "userId": "user_id"
}

intList = ['orderId', 'orderType', 'orderStatus', 'serviceId', 'orderPoint', 'isCoupon', 'isInvoice', 'isComment',
           'userId']

# db.create_all()
