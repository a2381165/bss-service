
# -*- coding: utf-8 -*-
from config import db


class Organization(db.Model):
    __tablename__ = "boss_organization"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    oz_name = db.Column(db.String(255))
    oz_pid = db.Column(db.Integer)
    oz_sort = db.Column(db.SmallInteger)
    oz_code = db.Column(db.String(255))
    is_lock = db.Column(db.SmallInteger)
    remark = db.Column(db.String(255))

    def __init__(self,oz_name,oz_pid,oz_sort,oz_code,is_lock,remark):
        '''Constructor'''
        self.oz_name=oz_name
        self.oz_pid=oz_pid
        self.oz_sort=oz_sort
        self.oz_code=oz_code
        self.is_lock=is_lock
        self.remark=remark


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'ozName', u'ozPid', u'ozSort', u'ozCode', u'isLock', u'remark'}
tableChangeDic = {
    "id":"id",
    "ozName":"oz_name",
    "ozPid":"oz_pid",
    "ozSort":"oz_sort",
    "ozCode":"oz_code",
    "isLock":"is_lock",
    "remark":"remark"
}

intList = {u'id', u'ozPid', u'ozSort', u'isLock'}

# db.create_all()
