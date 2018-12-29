# -*- coding: utf-8 -*-
from config import db
import datetime


class UserDeptArea(db.Model):
    __tablename__ = "boss_user_dept_area"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer)
    area_code = db.Column(db.String(255))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, user_id, area_code):
        '''Constructor'''
        self.user_id = user_id
        self.area_code = area_code

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'userId', u'areaCode', u'createTime'}
tableChangeDic = {
    "id": "id",
    "userId": "user_id",
    "areaCode": "area_code",
    "createTime": "create_time"
}

intList = {u'id', u'userId'}

# db.create_all()
