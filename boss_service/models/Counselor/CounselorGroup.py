
# -*- coding: utf-8 -*-
from config import db


class CounselorGroup(db.Model):
    __tablename__ = "counselor_group"

    group_id = db.Column(db.Integer, primary_key=True, nullable=False)
    group_name = db.Column(db.String(100))
    admin_id = db.Column(db.Integer)
    group_remark = db.Column(db.String(200))
    is_lock = db.Column(db.SmallInteger)

    def __init__(self, group_id,group_name,admin_id,group_remark,is_lock):
        '''Constructor'''
        self.group_id=group_id
        self.group_name=group_name
        self.admin_id=admin_id
        self.group_remark=group_remark
        self.is_lock=is_lock


    def __repr__(self):
        return 'group_id : %s' % self.group_id


# Client and database attributes dictionary
clinetHead = {u'groupId', u'groupName', u'adminId', u'groupRemark', u'isLock'}
CounselorGroupChangeDic = {
    "groupId":"group_id",
    "groupName":"group_name",
    "adminId":"admin_id",
    "groupRemark":"group_remark",
    "isLock":"is_lock"
}

intList = {u'groupId', u'adminId', u'isLock'}

# db.create_all()
