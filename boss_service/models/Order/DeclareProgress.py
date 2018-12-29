# -*- coding: utf-8 -*-
from config import db


class DeclareProgress(db.Model):
    __tablename__ = "zzh_declare_progress"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    stage_name = db.Column(db.String(20))
    stage_person = db.Column(db.String(20))
    stage_time = db.Column(db.DateTime)
    stage_remark = db.Column(db.String(200))

    def __init__(self, order_no, stage_name, stage_person, stage_time, stage_remark):
        '''Constructor'''
        self.order_no = order_no
        self.stage_name = stage_name
        self.stage_person = stage_person
        self.stage_time = stage_time
        self.stage_remark = stage_remark

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'stageName', u'stagePerson', u'stageTime', u'stageRemark'}
DeclareProgressChangeDic = {
    "id": "id",
    "orderNo": "order_no",
    "stageName": "stage_name",
    "stagePerson": "stage_person",
    "stageTime": "stage_time",
    "stageRemark": "stage_remark"
}

intList = {u'id'}

# db.create_all()
