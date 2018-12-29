
# -*- coding: utf-8 -*-
from config import db


class UserOrderItem(db.Model):
    __tablename__ = "zzh_user_order_item"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    item_url = db.Column(db.String(255))
    item_title = db.Column(db.String(255))
    item_imgurl = db.Column(db.String(255))
    item_pricerange = db.Column(db.String(255))
    item_pulishdate = db.Column(db.DateTime)
    item_deadline = db.Column(db.DateTime)
    item_contact = db.Column(db.String(255))
    item_submit_address = db.Column(db.String(255))
    item_type = db.Column(db.SmallInteger)
    item_content = db.Column(db.Text)
    dept_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)

    def __init__(self, id,order_no,item_url,item_title,item_imgurl,item_pricerange,item_pulishdate,item_deadline,item_contact,item_submit_address,item_type,item_content,dept_id,item_id):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.item_url=item_url
        self.item_title=item_title
        self.item_imgurl=item_imgurl
        self.item_pricerange=item_pricerange
        self.item_pulishdate=item_pulishdate
        self.item_deadline=item_deadline
        self.item_contact=item_contact
        self.item_submit_address=item_submit_address
        self.item_type=item_type
        self.item_content=item_content
        self.dept_id=dept_id
        self.item_id=item_id


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'itemUrl', u'itemTitle', u'itemImgurl', u'itemPricerange', u'itemPulishdate', u'itemDeadline', u'itemContact', u'itemSubmitAddress', u'itemType', u'itemContent', u'deptId', u'itemId'}
UserOrderItemChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "itemUrl":"item_url",
    "itemTitle":"item_title",
    "itemImgurl":"item_imgurl",
    "itemPricerange":"item_pricerange",
    "itemPulishdate":"item_pulishdate",
    "itemDeadline":"item_deadline",
    "itemContact":"item_contact",
    "itemSubmitAddress":"item_submit_address",
    "itemType":"item_type",
    "itemContent":"item_content",
    "deptId":"dept_id",
    "itemId":"item_id"
}

intList = {u'id', u'itemType', u'deptId', u'itemId'}

# db.create_all()
