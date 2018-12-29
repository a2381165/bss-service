
# -*- coding: utf-8 -*-
from config import db


class MonthlyWages(db.Model):
    __tablename__ = "boss_monthly_wages"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    admin_id = db.Column(db.Integer)
    rate = db.Column(db.String(255))
    start_fee = db.Column(db.String(255))
    manage_fee = db.Column(db.String(255))
    project_fee = db.Column(db.String(255))
    project_rate = db.Column(db.String(255))
    proejct_check_list = db.Column(db.String(255))
    edit_check_list = db.Column(db.String(255))
    year = db.Column(db.SmallInteger)
    month = db.Column(db.SmallInteger)
    update_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime)

    def __init__(self,admin_id,rate,start_fee,manage_fee,project_fee,project_rate,proejct_check_list,edit_check_list,year,month,update_time,create_time):
        '''Constructor'''
        self.admin_id=admin_id
        self.rate=rate
        self.start_fee=start_fee
        self.manage_fee=manage_fee
        self.project_fee=project_fee
        self.project_rate=project_rate
        self.proejct_check_list=proejct_check_list
        self.edit_check_list=edit_check_list
        self.year=year
        self.month=month
        self.update_time=update_time
        self.create_time=create_time


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id','adminId','rate','startFee','manageFee','projectFee','projectRate','proejctCheckList','editCheckList','year','month','updateTime','createTime']
MonthlyWagesChangeDic = {
    "id":"id",
    "adminId":"admin_id",
    "rate":"rate",
    "startFee":"start_fee",
    "manageFee":"manage_fee",
    "projectFee":"project_fee",
    "projectRate":"project_rate",
    "proejctCheckList":"proejct_check_list",
    "editCheckList":"edit_check_list",
    "year":"year",
    "month":"month",
    "updateTime":"update_time",
    "createTime":"create_time"
}

intList = ['id','adminId','year','month']

# db.create_all()
