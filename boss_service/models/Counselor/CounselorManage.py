
# -*- coding: utf-8 -*-
from config import db


class CounselorManage(db.Model):
    __tablename__ = "counselor_manage"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_id = db.Column(db.Integer)
    counselor_id = db.Column(db.Integer)

    def __init__(self, id,group_id,counselor_id):
        '''Constructor'''
        self.id=id
        self.group_id=group_id
        self.counselor_id=counselor_id


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'groupId', u'counselorId'}
CounselorManageChangeDic = {
    "id":"id",
    "groupId":"group_id",
    "counselorId":"counselor_id"
}

intList = {u'id', u'groupId', u'counselorId'}

# db.create_all()
