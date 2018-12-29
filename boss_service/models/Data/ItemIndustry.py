
# -*- coding: utf-8 -*-
from config import db


class ItemIndustry(db.Model):
    __tablename__ = "data_item_industry"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer)
    industry_id = db.Column(db.Integer)

    def __init__(self,item_id,industry_id):
        '''Constructor'''
        self.item_id=item_id
        self.industry_id=industry_id


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'itemId', u'industryId'}
tableChangeDic = {
    "id":"id",
    "itemId":"item_id",
    "industryId":"industry_id"
}

intList = {u'id', u'itemId', u'industryId'}

# db.create_all()
