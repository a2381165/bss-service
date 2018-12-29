
# -*- coding: utf-8 -*-
from config import db


class UserOrderService(db.Model):
    __tablename__ = "zzh_user_order_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_startup_fee = db.Column(db.String(255))
    service_price = db.Column(db.Numeric(10,2))
    service_rate = db.Column(db.String(255))
    service_process = db.Column(db.String(255))
    service_content = db.Column(db.Text)
    required_list = db.Column(db.String(255))
    service_contact_person = db.Column(db.String(255))
    service_contact_phone = db.Column(db.String(255))
    service_beforehand_day = db.Column(db.DateTime)

    def __init__(self, id,order_no,service_startup_fee,service_price,service_rate,service_process,service_content,required_list,service_contact_person,service_contact_phone,service_beforehand_day):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.service_startup_fee=service_startup_fee
        self.service_price=service_price
        self.service_rate=service_rate
        self.service_process=service_process
        self.service_content=service_content
        self.required_list=required_list
        self.service_contact_person=service_contact_person
        self.service_contact_phone=service_contact_phone
        self.service_beforehand_day=service_beforehand_day


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'serviceStartupFee', u'servicePrice', u'serviceRate', u'serviceProcess', u'serviceContent', u'requiredList', u'serviceContactPerson', u'serviceContactPhone', u'serviceBeforehandDay'}
UserOrderServiceChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "serviceStartupFee":"service_startup_fee",
    "servicePrice":"service_price",
    "serviceRate":"service_rate",
    "serviceProcess":"service_process",
    "serviceContent":"service_content",
    "requiredList":"required_list",
    "serviceContactPerson":"service_contact_person",
    "serviceContactPhone":"service_contact_phone",
    "serviceBeforehandDay":"service_beforehand_day"
}

intList = {u'id'}

# db.create_all()
