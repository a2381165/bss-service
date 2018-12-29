
# -*- coding: utf-8 -*-
from config import db


class ServiceFee(db.Model):
    __tablename__ = "boss_service_fee"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    admin_id = db.Column(db.Integer)
    service_fee = db.Column(db.Numeric(15,2))
    service_rate = db.Column(db.SmallInteger)
    fee_status = db.Column(db.SmallInteger)
    fee_type = db.Column(db.SmallInteger)
    update_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime)

    def __init__(self, admin_id,service_fee,service_rate,fee_status,fee_type,update_time,create_time):
        '''Constructor'''
        self.admin_id=admin_id
        self.service_fee=service_fee
        self.service_rate=service_rate
        self.fee_status=fee_status
        self.fee_type=fee_type
        self.update_time=update_time
        self.create_time=create_time


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id','adminId','serviceFee','serviceRate','feeStatus','feeType','updateTime','createTime']
ServiceFeeChangeDic = {
    "id":"id",
    "adminId":"admin_id",
    "serviceFee":"service_fee",
    "serviceRate":"service_rate",
    "feeStatus":"fee_status",
    "feeType":"fee_type",
    "updateTime":"update_time",
    "createTime":"create_time"
}

intList = ['id','adminId',"serviceFee",'serviceRate','feeStatus','feeType']

# db.create_all()
