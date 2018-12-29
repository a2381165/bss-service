# -*- coding: utf-8 -*-
from config import db


class BankPartner(db.Model):
    __tablename__ = "zzh_bank_partner"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(50))
    image_url = db.Column(db.String(255))
    intro = db.Column(db.String(1000))
    status = db.Column(db.SmallInteger)
    area_name = db.Column(db.String(50))
    remark = db.Column(db.String(100))
    logo_url = db.Column(db.String(255))
    sort = db.Column(db.Integer)

    def __init__(self, name, image_url, intro, status, area_name, remark, logo_url, sort):
        '''Constructor'''
        self.name = name
        self.image_url = image_url
        self.intro = intro
        self.status = status
        self.area_name = area_name
        self.remark = remark
        self.logo_url = logo_url
        self.sort = sort

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'name', 'imageUrl', 'intro', 'status', 'areaName', 'remark', 'logoUrl', 'sort']
BankPartnerChangeDic = {
    "id": "id",
    "name": "name",
    "imageUrl": "image_url",
    "intro": "intro",
    "status": "status",
    "areaName": "area_name",
    "remark": "remark",
    "logoUrl": "logo_url",
    "sort": "sort"
}

intList = ['id', 'status', 'sort']

# db.create_all()
