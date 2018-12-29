
# -*- coding: utf-8 -*-
from config import db


class RoleMenu(db.Model):
    __tablename__ = "boss_role_menu"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    role_id = db.Column(db.Integer)
    menu_id = db.Column(db.Integer)

    def __init__(self,role_id,menu_id):
        '''Constructor'''
        self.role_id=role_id
        self.menu_id=menu_id


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'roleId', u'menuId'}
tableChangeDic = {
    "id":"id",
    "roleId":"role_id",
    "menuId":"menu_id"
}

intList = {u'id', u'roleId', u'menuId'}

# db.create_all()
