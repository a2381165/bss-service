# -*- coding: utf-8 -*-
from config import db


class WorkFlow(db.Model):
    __tablename__ = "data_work_flow"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255))
    desc = db.Column(db.String(255))
    num = db.Column(db.Integer)
    create_time = db.Column(db.DateTime)

    def __init__(self, name, desc, num,create_time):
        '''Constructor'''
        self.name = name
        self.desc = desc
        self.num = num
        self.create_time = create_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'name', u'desc', u'num',"createTime"}
WorkFlowChangeDic = {
    "id": "id",
    "name": "name",
    "desc": "desc",
    "num": "num",
    "createTime": "create_time",
}

intList = {u'id', u'num'}

# db.create_all()
