# -*- coding: utf-8 -*-
from config import db


class Area(db.Model):
    __tablename__ = "base_area"

    area_id = db.Column(db.Integer, primary_key=True, nullable=False)
    area_name = db.Column(db.String(50))
    area_code = db.Column(db.String(6))
    area_zip = db.Column(db.String(6))
    p_code = db.Column(db.String(6))

    def __init__(self, area_name, area_code, area_zip, p_code):
        '''Constructor'''
        self.area_name = area_name
        self.area_code = area_code
        self.area_zip = area_zip
        self.p_code = p_code

    def __repr__(self):
        return 'area_id : %s' % self.area_id


# Client and database attributes dictionary
clinetHead = {u'areaId', u'areaName', u'areaCode', u'areaZip', u'pCode'}
tableChangeDic = {
    "areaId": "area_id",
    "areaName": "area_name",
    "areaCode": "area_code",
    "areaZip": "area_zip",
    "pCode": "p_code"
}

intList = {u'areaId'}

# db.create_all()
