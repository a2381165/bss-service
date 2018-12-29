
# -*- coding: utf-8 -*-
from config import db


class UserInternalOrder(db.Model):
    __tablename__ = "zzh_user_internal_order"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    internal_order_no = db.Column(db.Integer)
    order_no = db.Column(db.String(64))
    internal_declare_status = db.Column(db.String(10))
    internal_order_type = db.Column(db.SmallInteger)
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)
    close_time = db.Column(db.DateTime)
    close_person = db.Column(db.String(20))
    close_reason = db.Column(db.String(200))
    close_type = db.Column(db.String(20))

    def __init__(self,task_id,internal_order_no,order_no,internal_declare_status,internal_order_type,create_person,create_time,execute_person,execute_time,is_done,close_time,close_person,close_reason,close_type):
        '''Constructor'''
        self.task_id=task_id
        self.internal_order_no=internal_order_no
        self.order_no=order_no
        self.internal_declare_status=internal_declare_status
        self.internal_order_type=internal_order_type
        self.create_person=create_person
        self.create_time=create_time
        self.execute_person=execute_person
        self.execute_time=execute_time
        self.is_done=is_done
        self.close_time=close_time
        self.close_person=close_person
        self.close_reason=close_reason
        self.close_type=close_type


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id','taskId','internalOrderNo','orderNo','internalDeclareStatus','internalOrderType','createPerson','createTime','executePerson','executeTime','isDone','closeTime','closePerson','closeReason','closeType']
UserInternalOrderChangeDic = {
    "id":"id",
    "taskId":"task_id",
    "internalOrderNo":"internal_order_no",
    "orderNo":"order_no",
    "internalDeclareStatus":"internal_declare_status",
    "internalOrderType":"internal_order_type",
    "createPerson":"create_person",
    "createTime":"create_time",
    "executePerson":"execute_person",
    "executeTime":"execute_time",
    "isDone":"is_done",
    "closeTime":"close_time",
    "closePerson":"close_person",
    "closeReason":"close_reason",
    "closeType":"close_type"
}














intList = ['id','taskId','internalOrderNo','internalOrderType','isDone']

# db.create_all()
