# -*- coding: utf-8 -*-
from config import db
import datetime


class AreaSet(db.Model):
    __tablename__ = "boss_area_set"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer)
    area_code = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())
    create_person = db.Column(db.String(255))
    oz_id = db.Column(db.Integer)

    def __init__(self, user_id, area_code, create_person, oz_id):
        '''Constructor'''
        self.user_id = user_id
        self.area_code = area_code
        self.create_person = create_person
        self.oz_id = oz_id

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'userId', u'areaCode', u'createTime', u'createPerson'}
tableChangeDic = {
    "id": "id",
    "userId": "user_id",
    "areaCode": "area_code",
    "createTime": "create_time",
    "createPerson": "create_person",
    "ozId": "oz_id",
}

intList = {u'id', u'userId', u'areaCode', "ozId"}

# db.create_all()
