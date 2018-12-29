# -*- coding: utf-8 -*-
from config import db


class TempService(db.Model):
    __tablename__ = "data_temp_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer)
    service_price = db.Column(db.Numeric(15, 2))
    service_starttime = db.Column(db.DateTime)
    is_secular = db.Column(db.SmallInteger)
    service_deadline = db.Column(db.DateTime)
    direction_name = db.Column(db.String(100))
    policy_source = db.Column(db.String(200))
    sheet_content = db.Column(db.Text)
    material_list = db.Column(db.String(1000))
    forecast_path = db.Column(db.String(255))
    is_evaluate = db.Column(db.SmallInteger)
    service_person = db.Column(db.String(255))
    service_contact_person = db.Column(db.String(20))
    service_contact_phone = db.Column(db.String(20))
    service_content = db.Column(db.String(500))
    declare_list = db.Column(db.String(1000))
    check_status = db.Column(db.SmallInteger)
    check_person = db.Column(db.String(20))
    check_time = db.Column(db.DateTime)
    check_remark = db.Column(db.String(100))
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    category_type = db.Column(db.SmallInteger)
    service_name = db.Column(db.String(20))
    servcice_process = db.Column(db.String(500))

    def __init__(self, item_id, service_price, service_starttime, is_secular, service_deadline, direction_name,
                 policy_source, sheet_content, material_list, forecast_path, is_evaluate, service_person,
                 service_contact_person, service_contact_phone, service_content, declare_list, check_status,
                 check_person, check_time, check_remark, create_person, create_time, category_type, service_name,
                 servcice_process):
        '''Constructor'''
        self.item_id = item_id
        self.service_price = service_price
        self.service_starttime = service_starttime
        self.is_secular = is_secular
        self.service_deadline = service_deadline
        self.direction_name = direction_name
        self.policy_source = policy_source
        self.sheet_content = sheet_content
        self.material_list = material_list
        self.forecast_path = forecast_path
        self.is_evaluate = is_evaluate
        self.service_person = service_person
        self.service_contact_person = service_contact_person
        self.service_contact_phone = service_contact_phone
        self.service_content = service_content
        self.declare_list = declare_list
        self.check_status = check_status
        self.check_person = check_person
        self.check_time = check_time
        self.check_remark = check_remark
        self.create_person = create_person
        self.create_time = create_time
        self.category_type = category_type
        self.service_name = service_name
        self.servcice_process = servcice_process

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = [u'id', u'itemId', u'servicePrice', u'serviceStarttime', u'isSecular', u'serviceDeadline',
              u'directionName', u'policySource', u'sheetContent', u'materialList', u'forecastPath', u'isEvaluate',
              u'servicePerson', u'serviceContactPerson', u'serviceContactPhone', u'serviceContent', u'declareList',
              u'checkStatus', u'checkPerson', u'checkTime', u'checkRemark', u'createPerson', u'createTime',
              u'categoryType', u'serviceName', u'servciceProcess']
TempServiceChangeDic = {
    "id": "id",
    "itemId": "item_id",
    "servicePrice": "service_price",
    "serviceStarttime": "service_starttime",
    "isSecular": "is_secular",
    "serviceDeadline": "service_deadline",
    "directionName": "direction_name",
    "policySource": "policy_source",
    "sheetContent": "sheet_content",
    "materialList": "material_list",
    "forecastPath": "forecast_path",
    "isEvaluate": "is_evaluate",
    "servicePerson": "service_person",
    "serviceContactPerson": "service_contact_person",
    "serviceContactPhone": "service_contact_phone",
    "serviceContent": "service_content",
    "declareList": "declare_list",
    "checkStatus": "check_status",
    "checkPerson": "check_person",
    "checkTime": "check_time",
    "checkRemark": "check_remark",
    "createPerson": "create_person",
    "createTime": "create_time",
    "categoryType": "category_type",
    "serviceName": "service_name",
    "servciceProcess": "servcice_process"
}

intList = [u'id', u'itemId', u'isSecular', u'isEvaluate', u'checkStatus', u'categoryType']

# db.create_all()
