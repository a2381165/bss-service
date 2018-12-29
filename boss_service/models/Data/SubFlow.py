# -*- coding: utf-8 -*-
from config import db


class SubFlow(db.Model):
    __tablename__ = "data_sub_flow"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    flow_id = db.Column(db.Integer)
    role_id = db.Column(db.Integer)
    sort = db.Column(db.SmallInteger)
    persons = db.Column(db.String(255))
    remark = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)

    def __init__(self, flow_id, role_id, sort, persons, remark, create_time):
        '''Constructor'''
        self.flow_id = flow_id
        self.role_id = role_id
        self.sort = sort
        self.persons = persons
        self.remark = remark
        self.create_time = create_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'flowId', u'roleId', u'sort', u'persons', u'remark', u'createTime'}
SubFlowChangeDic = {
    "id": "id",
    "flowId": "flow_id",
    "roleId": "role_id",
    "sort": "sort",
    "persons": "persons",
    "remark": "remark",
    "createTime": "create_time"
}

intList = {u'id', u'flowId', u'roleId', u'sort'}

# db.create_all()
