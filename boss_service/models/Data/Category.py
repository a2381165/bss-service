
# -*- coding: utf-8 -*-
from config import db


class Category(db.Model):
    __tablename__ = "data_category"

    category_id = db.Column(db.Integer, primary_key=True, nullable=False)
    category_name = db.Column(db.String(20))
    category_pid = db.Column(db.Integer)
    category_sort = db.Column(db.Integer)
    is_lock = db.Column(db.SmallInteger)
    category_code = db.Column(db.String(3))

    def __init__(self, category_id,category_name,category_pid,category_sort,is_lock,category_code):
        '''Constructor'''
        self.category_id=category_id
        self.category_name=category_name
        self.category_pid=category_pid
        self.category_sort=category_sort
        self.is_lock=is_lock
        self.category_code=category_code


    def __repr__(self):
        return 'category_id : %s' % self.category_id


# Client and database attributes dictionary
clinetHead = {u'categoryId', u'categoryName', u'categoryPid', u'categorySort', u'isLock', u'categoryCode'}
tableChangeDic = {
    "categoryId":"category_id",
    "categoryName":"category_name",
    "categoryPid":"category_pid",
    "categorySort":"category_sort",
    "isLock":"is_lock",
    "categoryCode":"category_code"
}

intList = {u'categoryId', u'categoryPid', u'categorySort', u'isLock'}

# db.create_all()
