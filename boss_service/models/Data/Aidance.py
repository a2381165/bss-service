# -*- coding: utf-8 -*-
from config import db


class Aidance(db.Model):
    __tablename__ = "data_aidance"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    customer_name = db.Column(db.String(20))
    create_reason = db.Column(db.String(200))
    create_real_name = db.Column(db.String(30))
    create_time = db.Column(db.DateTime)
    flow_id = db.Column(db.SmallInteger)
    remark = db.Column(db.String(200))
    execute_person = db.Column(db.String(255))
    create_person = db.Column(db.String(20))
    complete_time = db.Column(db.DateTime)
    check_id = db.Column(db.Integer)
    from_id = db.Column(db.Integer)
    service_id = db.Column(db.Integer)
    flow_step = db.Column(db.SmallInteger)
    accept_status = db.Column(db.SmallInteger)
    is_done = db.Column(db.SmallInteger)
    task_type = db.Column(db.SmallInteger)

    def __init__(self, customer_name, create_reason, create_real_name, create_time, flow_id, remark, execute_person,
                 create_person, complete_time, check_id, from_id, service_id, flow_step, accept_status, is_done,
                 task_type):
        '''Constructor'''
        self.customer_name = customer_name
        self.create_reason = create_reason
        self.create_real_name = create_real_name
        self.create_time = create_time
        self.flow_id = flow_id
        self.remark = remark
        self.execute_person = execute_person
        self.create_person = create_person
        self.complete_time = complete_time
        self.check_id = check_id
        self.from_id = from_id
        self.service_id = service_id
        self.flow_step = flow_step
        self.accept_status = accept_status
        self.is_done = is_done
        self.task_type = task_type

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'customerName', u'createReason', u'createRealName', u'createTime', u'flowId', u'remark',
              u'executePerson', u'createPerson', u'completeTime', u'checkId', u'fromId', u'serviceId', u'flowStep',
              u'acceptStatus', u'isDone', u'taskType'}
AidanceChangeDic = {
    "id": "id",
    "customerName": "customer_name",
    "createReason": "create_reason",
    "createRealName": "create_real_name",
    "createTime": "create_time",
    "flowId": "flow_id",
    "remark": "remark",
    "executePerson": "execute_person",
    "createPerson": "create_person",
    "completeTime": "complete_time",
    "checkId": "check_id",
    "fromId": "from_id",
    "serviceId": "service_id",
    "flowStep": "flow_step",
    "acceptStatus": "accept_status",
    "isDone": "is_done",
    "taskType": "task_type"
}

intList = {u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep', u'acceptStatus', u'isDone', u'taskType'}

# db.create_all()
