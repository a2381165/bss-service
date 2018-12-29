# -*- coding: utf-8 -*-
from config import db


class OrderAidance(db.Model):
    __tablename__ = "boss_order_aidance"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    service_no = db.Column(db.String(64))
    pre_order_no = db.Column(db.String(64))
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)

    def __init__(self, task_id, service_no, pre_order_no, create_person, create_time, execute_person, execute_time,
                 is_done):
        '''Constructor'''
        self.task_id = task_id
        self.service_no = service_no
        self.pre_order_no = pre_order_no
        self.create_person = create_person
        self.create_time = create_time
        self.execute_person = execute_person
        self.execute_time = execute_time
        self.is_done = is_done

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'taskId', 'serviceNo', 'preOrderNo', 'createPerson', 'createTime', 'executePerson', 'executeTime',
              'isDone']
OrderAidanceChangeDic = {
    "id": "id",
    "taskId": "task_id",
    "serviceNo": "service_no",
    "preOrderNo": "pre_order_no",
    "createPerson": "create_person",
    "createTime": "create_time",
    "executePerson": "execute_person",
    "executeTime": "execute_time",
    "isDone": "is_done"
}

intList = ['id', 'taskId', 'isDone']

# db.create_all()
