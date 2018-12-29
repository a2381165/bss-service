# -*- coding: utf-8 -*-
from config import db


class TempSingleService(db.Model):
    __tablename__ = "data_temp_single_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    service_id = db.Column(db.Integer)
    aidance_id = db.Column(db.Integer)
    customer_name = db.Column(db.String(20))
    service_agency = db.Column(db.String(50))
    service_person = db.Column(db.String(100))
    service_content = db.Column(db.String(1000))
    declare_direction = db.Column(db.String(100))
    manage_dept = db.Column(db.String(50))
    apply_amount = db.Column(db.String(50))
    subsidy_method = db.Column(db.String(500))
    service_deadline = db.Column(db.DateTime)
    declare_conditions = db.Column(db.String(255))
    declare_data = db.Column(db.String(255))
    remark = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)

    def __init__(self, service_id, aidance_id, customer_name, service_agency, service_person, service_content,
                 declare_direction, manage_dept, apply_amount, subsidy_method, service_deadline, declare_conditions,
                 declare_data, remark, create_time):
        '''Constructor'''
        self.service_id = service_id
        self.aidance_id = aidance_id
        self.customer_name = customer_name
        self.service_agency = service_agency
        self.service_person = service_person
        self.service_content = service_content
        self.declare_direction = declare_direction
        self.manage_dept = manage_dept
        self.apply_amount = apply_amount
        self.subsidy_method = subsidy_method
        self.service_deadline = service_deadline
        self.declare_conditions = declare_conditions
        self.declare_data = declare_data
        self.remark = remark
        self.create_time = create_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'serviceId', u'aidanceId', u'customerName', u'serviceAgency', u'servicePerson', u'serviceContent',
              u'declareDirection', u'manageDept', u'applyAmount', u'subsidyMethod', u'serviceDeadline',
              u'declareConditions', u'declareData', u'remark', u'createTime'}
TempSingleServiceChangeDic = {
    "id": "id",
    "serviceId": "service_id",
    "aidanceId": "aidance_id",
    "customerName": "customer_name",
    "serviceAgency": "service_agency",
    "servicePerson": "service_person",
    "serviceContent": "service_content",
    "declareDirection": "declare_direction",
    "manageDept": "manage_dept",
    "applyAmount": "apply_amount",
    "subsidyMethod": "subsidy_method",
    "serviceDeadline": "service_deadline",
    "declareConditions": "declare_conditions",
    "declareData": "declare_data",
    "remark": "remark",
    "createTime": "create_time"
}

intList = {u'id', u'serviceId', u'aidanceId'}

# db.create_all()
