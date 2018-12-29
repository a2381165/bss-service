# -*- coding: utf-8 -*-
from config import db


class Menu(db.Model):
    __tablename__ = "boss_menu"

    menu_id = db.Column(db.Integer, primary_key=True, nullable=False)
    menu_key = db.Column(db.String(500))
    menu_parent_id = db.Column(db.Integer)
    menu_type = db.Column(db.String(50))
    menu_title = db.Column(db.String(150))
    menu_ico_url = db.Column(db.String(255))
    menu_link_url = db.Column(db.String(255))
    menu_sort = db.Column(db.Integer)
    menu_remark = db.Column(db.String(200))
    is_sys = db.Column(db.SmallInteger)
    is_lock = db.Column(db.SmallInteger)

    def __init__(self, menu_key, menu_parent_id, menu_type, menu_title, menu_ico_url, menu_link_url, menu_sort,
                 menu_remark, is_sys, is_lock):
        '''Constructor'''
        self.menu_key = menu_key
        self.menu_parent_id = menu_parent_id
        self.menu_type = menu_type
        self.menu_title = menu_title
        self.menu_ico_url = menu_ico_url
        self.menu_link_url = menu_link_url
        self.menu_sort = menu_sort
        self.menu_remark = menu_remark
        self.is_sys = is_sys
        self.is_lock = is_lock

    def __repr__(self):
        return 'menu_id : %s' % self.menu_id



# Client and database attributes dictionary
clinetHead = {u'menuId', u'menuKey', u'menuParentId', u'menuType', u'menuTitle', u'menuIcoUrl', u'menuLinkUrl',
              u'menuSort', u'menuRemark', u'isSys', u'isLock'}
tableChangeDic = {
    "menuId": "menu_id",
    "menuKey": "menu_key",
    "menuParentId": "menu_parent_id",
    "menuType": "menu_type",
    "menuTitle": "menu_title",
    "menuIcoUrl": "menu_ico_url",
    "menuLinkUrl": "menu_link_url",
    "menuSort": "menu_sort",
    "menuRemark": "menu_remark",
    "isSys": "is_sys",
    "isLock": "is_lock"
}

intList = {u'menuId', u'menuParentId', u'menuSort', u'isSys', u'isLock'}

# db.create_all()
