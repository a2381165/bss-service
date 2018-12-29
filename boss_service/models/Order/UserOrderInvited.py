
# -*- coding: utf-8 -*-
from config import db


class UserOrderInvited(db.Model):
    __tablename__ = "zzh_user_order_invited"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    invited_code = db.Column(db.String(32))

    def __init__(self, id,order_no,invited_code):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.invited_code=invited_code


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'invitedCode'}
UserOrderInvitedChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "invitedCode":"invited_code"
}

intList = {u'id'}

# db.create_all()
