
# -*- coding: utf-8 -*-
from config import db


class BankProduct(db.Model):
    __tablename__ = "zzh_bank_product"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    bank_partner_id = db.Column(db.Integer)
    product_name = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    is_secular = db.Column(db.SmallInteger)
    status = db.Column(db.SmallInteger)
    intro = db.Column(db.Text)
    sort = db.Column(db.Integer)

    def __init__(self, id,bank_partner_id,product_name,start_time,end_time,is_secular,status,intro,sort):
        '''Constructor'''
        self.bank_partner_id=bank_partner_id
        self.product_name=product_name
        self.start_time=start_time
        self.end_time=end_time
        self.is_secular=is_secular
        self.status=status
        self.intro=intro
        self.sort=sort


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id','bankPartnerId','productName','startTime','endTime','isSecular','status','intro','sort']
BankProductChangeDic = {
    "id":"id",
    "bankPartnerId":"bank_partner_id",
    "productName":"product_name",
    "startTime":"start_time",
    "endTime":"end_time",
    "isSecular":"is_secular",
    "status":"status",
    "intro":"intro",
    "sort":"sort"
}

intList = ['id','bankPartnerId','isSecular','status','sort']

# db.create_all()
