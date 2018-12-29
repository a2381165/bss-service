# -*- coding: utf-8 -*-
from config import db


class ProductService(db.Model):
    __tablename__ = "data_product_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_name = db.Column(db.String(20))
    product_desc = db.Column(db.String(200))
    product_origin = db.Column(db.String(50))
    create_time = db.Column(db.DateTime)
    create_person = db.Column(db.String(20))
    is_lock = db.Column(db.SmallInteger)
    service_process = db.Column(db.String(500))
    service_content = db.Column(db.String(255))
    service_price = db.Column(db.Numeric(10, 2))

    def __init__(self, product_name, product_desc, product_origin, create_time, create_person, is_lock, service_process,
                 service_content, service_price):
        '''Constructor'''
        self.product_name = product_name
        self.product_desc = product_desc
        self.product_origin = product_origin
        self.create_time = create_time
        self.create_person = create_person
        self.is_lock = is_lock
        self.service_process = service_process
        self.service_content = service_content
        self.service_price = service_price

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'productName', 'productDesc', 'productOrigin', 'createTime', 'createPerson', 'isLock',
              'serviceProcess', 'serviceContent', 'servicePrice']
ProductServiceChangeDic = {
    "id": "id",
    "productName": "product_name",
    "productDesc": "product_desc",
    "productOrigin": "product_origin",
    "createTime": "create_time",
    "createPerson": "create_person",
    "isLock": "is_lock",
    "serviceProcess": "service_process",
    "serviceContent": "service_content",
    "servicePrice": "service_price"
}

intList = ['id', 'isLock']

# db.create_all()
