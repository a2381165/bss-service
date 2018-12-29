# -*- coding: utf-8 -*-
from config import db
import datetime


class Post(db.Model):
    __tablename__ = "boss_post"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(20))
    code = db.Column(db.String(10))
    p_code = db.Column(db.String(10))
    oz_id = db.Column(db.Integer)
    is_lock = db.Column(db.SmallInteger)
    remark = db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name, code, p_code, oz_id, is_lock, remark):
        '''Constructor'''
        self.name = name
        self.code = code
        self.p_code = p_code
        self.oz_id = oz_id
        self.is_lock = is_lock
        self.remark = remark

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'name', u'code', u'pCode', u'ozId', u'isLock', u'remark', u'createTime'}
tableChangeDic = {
    "id": "id",
    "name": "name",
    "code": "code",
    "pCode": "p_code",
    "ozId": "oz_id",
    "isLock": "is_lock",
    "remark": "remark",
    "createTime": "create_time"
}

intList = {u'id', u'ozId', u'isLock'}

# db.create_all()
