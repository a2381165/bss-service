# -*- coding: utf-8 -*-
from config import db


class UserRole(db.Model):
    __tablename__ = "boss_user_role"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, role_id, user_id):
        '''Constructor'''
        self.role_id = role_id
        self.user_id = user_id

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'roleId', u'userId'}
tableChangeDic = {
    "id": "id",
    "roleId": "role_id",
    "userId": "user_id"
}

intList = {u'id', u'roleId', u'userId'}

# db.create_all()
