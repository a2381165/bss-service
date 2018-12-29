
# -*- coding: utf-8 -*-
from config import db


class CounselorRobbing(db.Model):
    __tablename__ = "counselor_robbing"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    counselor_id = db.Column(db.Integer)
    order_no = db.Column(db.String(30))
    robbing_time = db.Column(db.DateTime)

    def __init__(self, id,counselor_id,order_no,robbing_time):
        '''Constructor'''
        self.id=id
        self.counselor_id=counselor_id
        self.order_no=order_no
        self.robbing_time=robbing_time


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'counselorId', u'orderNo', u'robbingTime'}
CounselorRobbingChangeDic = {
    "id":"id",
    "counselorId":"counselor_id",
    "orderNo":"order_no",
    "robbingTime":"robbing_time"
}

intList = {u'id', u'counselorId'}

# db.create_all()
