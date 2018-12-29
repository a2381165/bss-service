# -*- coding: utf-8 -*-
from config import db


class PotentialCustomers(db.Model):
    __tablename__ = "boss_potential_customers"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    service_id = db.Column(db.Integer)
    customer_name = db.Column(db.String(20))
    address = db.Column(db.String(50))
    contact_person = db.Column(db.String(20))
    contact_phone = db.Column(db.String(11))
    require = db.Column(db.String(255))
    excel_path = db.Column(db.String(255))
    company_scope = db.Column(db.String(200))
    registered_capital = db.Column(db.String(50))
    is_choose = db.Column(db.SmallInteger)
    source_type = db.Column(db.SmallInteger)
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)

    def __init__(self, service_id, customer_name, address, contact_person, contact_phone, require, excel_path,
                 company_scope, registered_capital, is_choose, source_type, create_person, create_time):
        '''Constructor'''
        self.service_id = service_id
        self.customer_name = customer_name
        self.address = address
        self.contact_person = contact_person
        self.contact_phone = contact_phone
        self.require = require
        self.excel_path = excel_path
        self.company_scope = company_scope
        self.registered_capital = registered_capital
        self.is_choose = is_choose
        self.source_type = source_type
        self.create_person = create_person
        self.create_time = create_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'serviceId', 'customerName', 'address', 'contactPerson', 'contactPhone', 'require', 'excelPath',
              'companyScope', 'registeredCapital', 'isChoose', 'sourceType', 'createPerson', 'createTime']
PotentialCustomersChangeDic = {
    "id": "id",
    "serviceId": "service_id",
    "customerName": "customer_name",
    "address": "address",
    "contactPerson": "contact_person",
    "contactPhone": "contact_phone",
    "require": "require",
    "excelPath": "excel_path",
    "companyScope": "company_scope",
    "registeredCapital": "registered_capital",
    "isChoose": "is_choose",
    "sourceType": "source_type",
    "createPerson": "create_person",
    "createTime": "create_time"
}

intList = ['id', 'serviceId', 'isChoose', 'sourceType']

# db.create_all()
