
# -*- coding: utf-8 -*-
from config import db


class Transfer(db.Model):
    __tablename__ = "data_transfer"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    owner = db.Column(db.String(20))
    transfer = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    reason = db.Column(db.String(100))

    def __init__(self,task_id,owner,transfer,create_time,reason):
        '''Constructor'''
        self.task_id=task_id
        self.owner=owner
        self.transfer=transfer
        self.create_time=create_time
        self.reason=reason


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'taskId', u'owner', u'transfer', u'createTime', u'reason'}
TransferChangeDic = {
    "id":"id",
    "taskId":"task_id",
    "owner":"owner",
    "transfer":"transfer",
    "createTime":"create_time",
    "reason":"reason"
}

intList = {u'id', u'taskId'}

# db.create_all()
