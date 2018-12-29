# -*- coding: utf-8 -*-
from config import db


class Service(db.Model):
    __tablename__ = "data_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer)
    service_name = db.Column(db.String(20))
    policy_source = db.Column(db.String(200))
    service_price = db.Column(db.Numeric(15, 2))
    service_starttime = db.Column(db.DateTime)
    service_deadline = db.Column(db.DateTime)
    direction_name = db.Column(db.String(100))
    service_content = db.Column(db.String(500))
    sheet_content = db.Column(db.Text)
    material_list = db.Column(db.String(1000))
    forecast_path = db.Column(db.String(255))
    service_contact_person = db.Column(db.String(20))
    service_contact_phone = db.Column(db.String(20))
    is_secular = db.Column(db.SmallInteger)
    is_evaluate = db.Column(db.SmallInteger)
    declare_list = db.Column(db.String(1000))
    create_time = db.Column(db.DateTime)
    category_type = db.Column(db.SmallInteger)
    servcice_process = db.Column(db.String(500))

    def __init__(self, item_id, service_name, policy_source, service_price, service_starttime, service_deadline,
                 direction_name, service_content, sheet_content, material_list, forecast_path, service_contact_person,
                 service_contact_phone, is_secular, is_evaluate, declare_list, create_time, category_type,
                 servcice_process):
        '''Constructor'''
        self.item_id = item_id
        self.service_name = service_name
        self.policy_source = policy_source
        self.service_price = service_price
        self.service_starttime = service_starttime
        self.service_deadline = service_deadline
        self.direction_name = direction_name
        self.service_content = service_content
        self.sheet_content = sheet_content
        self.material_list = material_list
        self.forecast_path = forecast_path
        self.service_contact_person = service_contact_person
        self.service_contact_phone = service_contact_phone
        self.is_secular = is_secular
        self.is_evaluate = is_evaluate
        self.declare_list = declare_list
        self.create_time = create_time
        self.category_type = category_type
        self.servcice_process = servcice_process

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'itemId', 'serviceName', 'policySource', 'servicePrice', 'serviceStarttime', 'serviceDeadline',
              'directionName', 'serviceContent', 'sheetContent', 'materialList', 'forecastPath', 'serviceContactPerson',
              'serviceContactPhone', 'isSecular', 'isEvaluate', 'declareList', 'createTime', 'categoryType',
              'servciceProcess']
ServiceChangeDic = {
    "id": "id",
    "itemId": "item_id",
    "serviceName": "service_name",
    "policySource": "policy_source",
    "servicePrice": "service_price",
    "serviceStarttime": "service_starttime",
    "serviceDeadline": "service_deadline",
    "directionName": "direction_name",
    "serviceContent": "service_content",
    "sheetContent": "sheet_content",
    "materialList": "material_list",
    "forecastPath": "forecast_path",
    "serviceContactPerson": "service_contact_person",
    "serviceContactPhone": "service_contact_phone",
    "isSecular": "is_secular",
    "isEvaluate": "is_evaluate",
    "declareList": "declare_list",
    "createTime": "create_time",
    "categoryType": "category_type",
    "servciceProcess": "servcice_process"
}

intList = ['id', 'itemId', 'isSecular', 'isEvaluate', 'categoryType']

# db.create_all()
