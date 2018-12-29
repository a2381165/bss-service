# -*- coding: utf-8 -*-
from config import db


class DeptItem(db.Model):
    __tablename__ = "boss_dept_item"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    dept_id = db.Column(db.Integer)
    type = db.Column(db.String(255))
    name = db.Column(db.String(255))
    code = db.Column(db.String(6))
    pcode = db.Column(db.String(6))
    remark = db.Column(db.String(255))
    is_lock = db.Column(db.SmallInteger)
    create_time = db.Column(db.DateTime)

    def __init__(self, dept_id, type, name, code, pcode, remark, is_lock, create_time):
        '''Constructor'''
        self.dept_id = dept_id
        self.type = type
        self.name = name
        self.code = code
        self.pcode = pcode
        self.remark = remark
        self.is_lock = is_lock
        self.create_time = create_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'deptId', u'type', u'name', u'code', u'pcode', u'remark', u'isLock', u'createTime'}
tableChangeDic = {
    "id": "id",
    "deptId": "dept_id",
    "type": "type",
    "name": "name",
    "code": "code",
    "pcode": "pcode",
    "remark": "remark",
    "isLock": "is_lock",
    "createTime": "create_time"
}

intList = {u'id', u'deptId', u'isLock'}

# db.create_all()
