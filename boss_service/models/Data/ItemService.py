# -*- coding: utf-8 -*-
from config import db


class ItemService(db.Model):
    __tablename__ = "data_item_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer)
    dept_id = db.Column(db.Integer)
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    directions = db.Column(db.String(500))
    check_status = db.Column(db.SmallInteger)
    check_person = db.Column(db.String(20))
    check_remark = db.Column(db.String(200))
    check_time = db.Column(db.DateTime)
    is_lock = db.Column(db.SmallInteger)

    def __init__(self, item_id, dept_id, create_person, create_time, directions, check_status, check_person,
                 check_remark, check_time,is_lock):
        '''Constructor'''
        self.item_id = item_id
        self.dept_id = dept_id
        self.create_person = create_person
        self.create_time = create_time
        self.directions = directions
        self.check_status = check_status
        self.check_person = check_person
        self.check_remark = check_remark
        self.check_time = check_time
        self.is_lock = is_lock

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'itemId', u'deptId', u'createPerson', u'createTime', u'directions', u'checkStatus',
              u'checkPerson', u'checkRemark', u'checkTime'}
tableChangeDic = {
    "id": "id",
    "itemId": "item_id",
    "deptId": "dept_id",
    "createPerson": "create_person",
    "createTime": "create_time",
    "directions": "directions",
    "checkStatus": "check_status",
    "checkPerson": "check_person",
    "checkRemark": "check_remark",
    "checkTime": "check_time",
    "isLock": "is_lock",
}

intList = {u'id', u'itemId', u'deptId',"isLock","checkStatus"}

# db.create_all()
