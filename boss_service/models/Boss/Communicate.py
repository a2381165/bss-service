# -*- coding: utf-8 -*-
from config import db


class Communicate(db.Model):
    __tablename__ = "boss_communicate"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    service_id = db.Column(db.Integer)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    product_name = db.Column(db.String(20))
    require = db.Column(db.String(200))
    project_path = db.Column(db.String(255))
    project_type = db.Column(db.SmallInteger)
    customer_name = db.Column(db.String(50))
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    is_send = db.Column(db.SmallInteger)
    is_done = db.Column(db.SmallInteger)
    remark = db.Column(db.String(100))
    choose_type = db.Column(db.SmallInteger)
    source_type = db.Column(db.SmallInteger)

    def __init__(self, service_id, order_no, service_no, product_name, require, project_path, project_type,
                 customer_name, execute_person, execute_time, create_person, create_time, is_send, is_done, remark,
                 choose_type, source_type):
        '''Constructor'''
        self.service_id = service_id
        self.order_no = order_no
        self.service_no = service_no
        self.product_name = product_name
        self.require = require
        self.project_path = project_path
        self.project_type = project_type
        self.customer_name = customer_name
        self.execute_person = execute_person
        self.execute_time = execute_time
        self.create_person = create_person
        self.create_time = create_time
        self.is_send = is_send
        self.is_done = is_done
        self.remark = remark
        self.choose_type = choose_type
        self.source_type = source_type

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'serviceId', 'orderNo', 'serviceNo', 'productName', 'require', 'projectPath', 'projectType',
              'customerName', 'executePerson', 'executeTime', 'createPerson', 'createTime', 'isSend', 'isDone',
              'remark', 'chooseType', 'sourceType']
CommunicateChangeDic = {
    "id": "id",
    "serviceId": "service_id",
    "orderNo": "order_no",
    "serviceNo": "service_no",
    "productName": "product_name",
    "require": "require",
    "projectPath": "project_path",
    "projectType": "project_type",
    "customerName": "customer_name",
    "executePerson": "execute_person",
    "executeTime": "execute_time",
    "createPerson": "create_person",
    "createTime": "create_time",
    "isSend": "is_send",
    "isDone": "is_done",
    "remark": "remark",
    "chooseType": "choose_type",
    "sourceType": "source_type"
}

intList = ['id', 'serviceId', 'projectType', 'isSend', 'isDone', 'chooseType', 'sourceType']

# db.create_all()
