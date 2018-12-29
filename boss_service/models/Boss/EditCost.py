
# -*- coding: utf-8 -*-
from config import db


class EditCost(db.Model):
    __tablename__ = "boss_edit_cost"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    internal_order_no = db.Column(db.Integer)
    contract_no = db.Column(db.Integer)
    order_no = db.Column(db.String(64))
    internal_order_type = db.Column(db.SmallInteger)
    edit_check_id = db.Column(db.Integer)
    accept_check_id = db.Column(db.Integer)
    project_check_id = db.Column(db.Integer)
    development_check_id = db.Column(db.Integer)
    sign_check_id = db.Column(db.Integer)
    commission_check_id = db.Column(db.Integer)
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)

    def __init__(self, internal_order_no,contract_no,order_no,internal_order_type,edit_check_id,accept_check_id,project_check_id,development_check_id,sign_check_id,commission_check_id,create_person,create_time,is_done):
        '''Constructor'''
        self.internal_order_no=internal_order_no
        self.contract_no=contract_no
        self.order_no=order_no
        self.internal_order_type=internal_order_type
        self.edit_check_id=edit_check_id
        self.accept_check_id=accept_check_id
        self.project_check_id=project_check_id
        self.development_check_id=development_check_id
        self.sign_check_id=sign_check_id
        self.commission_check_id=commission_check_id
        self.create_person=create_person
        self.create_time=create_time
        self.is_done=is_done


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id','internalOrderNo','contractNo','orderNo','internalOrderType','editCheckId','acceptCheckId','projectCheckId','developmentCheckId','signCheckId','commissionCheckId','createPerson','createTime','isDone']
EditCostChangeDic = {
    "id":"id",
    "internalOrderNo":"internal_order_no",
    "contractNo":"contract_no",
    "orderNo":"order_no",
    "internalOrderType":"internal_order_type",
    "editCheckId":"edit_check_id",
    "acceptCheckId":"accept_check_id",
    "projectCheckId":"project_check_id",
    "developmentCheckId":"development_check_id",
    "signCheckId":"sign_check_id",
    "commissionCheckId":"commission_check_id",
    "createPerson":"create_person",
    "createTime":"create_time",
    "isDone":"is_done"
}

intList = ['id','internalOrderNo','contractNo','internalOrderType','editCheckId','acceptCheckId','projectCheckId','developmentCheckId','signCheckId','commissionCheckId','isDone']

# db.create_all()
