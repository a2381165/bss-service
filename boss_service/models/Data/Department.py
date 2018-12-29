
# -*- coding: utf-8 -*-
from config import db


class Department(db.Model):
    __tablename__ = "data_department"

    dept_id = db.Column(db.Integer, primary_key=True, nullable=False)
    dept_code = db.Column(db.String(18))
    dept_pid = db.Column(db.Integer)
    dept_name = db.Column(db.String(50))
    dept_address = db.Column(db.String(50))
    dept_url = db.Column(db.String(255))
    is_lock = db.Column(db.SmallInteger)
    level_code = db.Column(db.String(255))
    area_code = db.Column(db.String(6))
    category_id = db.Column(db.Integer)

    def __init__(self, dept_id,dept_code,dept_pid,dept_name,dept_address,dept_url,is_lock,level_code,area_code,category_id):
        '''Constructor'''
        self.dept_id=dept_id
        self.dept_code=dept_code
        self.dept_pid=dept_pid
        self.dept_name=dept_name
        self.dept_address=dept_address
        self.dept_url=dept_url
        self.is_lock=is_lock
        self.level_code=level_code
        self.area_code=area_code
        self.category_id=category_id


    def __repr__(self):
        return 'dept_id : %s' % self.dept_id


# Client and database attributes dictionary
clinetHead = {u'deptId', u'deptCode', u'deptPid', u'deptName', u'deptAddress', u'deptUrl', u'isLock', u'levelCode', u'areaCode', u'categoryId'}
tableChangeDic = {
    "deptId":"dept_id",
    "deptCode":"dept_code",
    "deptPid":"dept_pid",
    "deptName":"dept_name",
    "deptAddress":"dept_address",
    "deptUrl":"dept_url",
    "isLock":"is_lock",
    "levelCode":"level_code",
    "areaCode":"area_code",
    "categoryId":"category_id"
}

intList = {u'deptId', u'deptPid', u'isLock', u'categoryId'}

# db.create_all()
