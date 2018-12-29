
# -*- coding: utf-8 -*-
from config import db


class ItemLabel(db.Model):
    __tablename__ = "data_item_label"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer)
    label_id = db.Column(db.Integer)
    key_words = db.Column(db.String(32))

    def __init__(self,item_id,label_id,key_words):
        '''Constructor'''
        self.item_id=item_id
        self.label_id=label_id
        self.key_words=key_words


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'itemId', u'labelId', u'keyWords'}
tableChangeDic = {
    "id":"id",
    "itemId":"item_id",
    "labelId":"label_id",
    "keyWords":"key_words"
}

intList = {u'id', u'itemId', u'labelId'}

# db.create_all()
