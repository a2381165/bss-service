
# -*- coding: utf-8 -*-
from config import db


class Area(db.Model):
    __tablename__ = "data_area"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    area_code = db.Column(db.String(6))
    area_status = db.Column(db.SmallInteger)

    def __init__(self,area_code,area_status):
        '''Constructor'''
        self.area_code=area_code
        self.area_status=area_status


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'areaCode', u'areaStatus'}
tableChangeDic = {
    "id":"id",
    "areaCode":"area_code",
    "areaStatus":"area_status"
}

intList = {u'id', u'areaStatus'}

# db.create_all()
