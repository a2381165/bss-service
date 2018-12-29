
# -*- coding: utf-8 -*-
from config import db


class Label(db.Model):
    __tablename__ = "data_label"

    label_id = db.Column(db.Integer, primary_key=True, nullable=False)
    label_pid = db.Column(db.Integer)
    label_name = db.Column(db.String(50))
    is_lock = db.Column(db.SmallInteger)
    sort = db.Column(db.Integer)
    label_remark = db.Column(db.String(150))

    def __init__(self, label_id,label_pid,label_name,is_lock,sort,label_remark):
        '''Constructor'''
        self.label_id=label_id
        self.label_pid=label_pid
        self.label_name=label_name
        self.is_lock=is_lock
        self.sort=sort
        self.label_remark=label_remark


    def __repr__(self):
        return 'label_id : %s' % self.label_id


# Client and database attributes dictionary
clinetHead = {u'labelId', u'labelPid', u'labelName', u'isLock', u'sort', u'labelRemark'}
tableChangeDic = {
    "labelId":"label_id",
    "labelPid":"label_pid",
    "labelName":"label_name",
    "isLock":"is_lock",
    "sort":"sort",
    "labelRemark":"label_remark"
}

intList = {u'labelId', u'labelPid', u'isLock', u'sort'}

# db.create_all()
