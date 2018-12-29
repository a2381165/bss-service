
# -*- coding: utf-8 -*-
from config import db


class Source(db.Model):
    __tablename__ = "data_source"

    source_id = db.Column(db.Integer, primary_key=True, nullable=False)
    level_code = db.Column(db.SmallInteger)
    area_code = db.Column(db.String(6))
    dept_category = db.Column(db.Integer)
    dept_name = db.Column(db.String(50))
    dept_address = db.Column(db.String(100))
    dept_url = db.Column(db.String(255))
    des_url = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    create_person = db.Column(db.String(50))
    check_status = db.Column(db.SmallInteger)
    check_time = db.Column(db.DateTime)
    check_person = db.Column(db.String(50))
    check_remark = db.Column(db.String(255))
    is_lock = db.Column(db.SmallInteger)

    def __init__(self,level_code,area_code,dept_category,dept_name,dept_address,dept_url,des_url,create_time,create_person,check_status,check_time,check_person,check_remark,is_lock):
        '''Constructor'''
        self.level_code=level_code
        self.area_code=area_code
        self.dept_category=dept_category
        self.dept_name=dept_name
        self.dept_address=dept_address
        self.dept_url=dept_url
        self.des_url=des_url
        self.create_time=create_time
        self.create_person=create_person
        self.check_status=check_status
        self.check_time=check_time
        self.check_person=check_person
        self.check_remark=check_remark
        self.is_lock=is_lock


    def __repr__(self):
        return 'source_id : %s' % self.source_id


# Client and database attributes dictionary
clinetHead = {u'sourceId', u'levelCode', u'areaCode', u'deptCategory', u'deptName', u'deptAddress', u'deptUrl', u'desUrl', u'createTime', u'createPerson', u'checkStatus', u'checkTime', u'checkPerson', u'checkRemark', u'isLock'}
tableChangeDic = {
    "sourceId":"source_id",
    "levelCode":"level_code",
    "areaCode":"area_code",
    "deptCategory":"dept_category",
    "deptName":"dept_name",
    "deptAddress":"dept_address",
    "deptUrl":"dept_url",
    "desUrl":"des_url",
    "createTime":"create_time",
    "createPerson":"create_person",
    "checkStatus":"check_status",
    "checkTime":"check_time",
    "checkPerson":"check_person",
    "checkRemark":"check_remark",
    "isLock":"is_lock"
}

intList = {u'sourceId', u'levelCode', u'deptCategory', u'checkStatus', u'isLock'}

# db.create_all()
