# -*- coding: utf-8 -*-
from config import db


class Role(db.Model):
    __tablename__ = "boss_role"

    role_id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_pid = db.Column(db.SmallInteger)
    role_name = db.Column(db.String(60))
    role_desc = db.Column(db.String(250))
    is_sys = db.Column(db.SmallInteger)
    is_lock = db.Column(db.SmallInteger)
    oz_id = db.Column(db.Integer)
    manager_name = db.Column(db.String(20))
    manager_real_name = db.Column(db.String(20))

    def __init__(self, role_pid, role_name, role_desc, is_sys, is_lock, oz_id, manager_name, manager_real_name):
        '''Constructor'''
        self.role_pid = role_pid
        self.role_name = role_name
        self.role_desc = role_desc
        self.is_sys = is_sys
        self.is_lock = is_lock
        self.oz_id = oz_id
        self.manager_name = manager_name
        self.manager_real_name = manager_real_name

    def __repr__(self):
        return 'role_id : %s' % self.role_id


# Client and database attributes dictionary
clinetHead = {u'roleId', u'rolePid', u'roleName', u'roleDesc', u'isSys', u'isLock', u'ozId', u'managerName',
              u'managerRealName'}
tableChangeDic = {
    "roleId": "role_id",
    "rolePid": "role_pid",
    "roleName": "role_name",
    "roleDesc": "role_desc",
    "isSys": "is_sys",
    "isLock": "is_lock",
    "ozId": "oz_id",
    "managerName": "manager_name",
    "managerRealName": "manager_real_name"
}

intList = {u'roleId', u'rolePid', u'isSys', u'isLock', u'ozId'}

# db.create_all()
