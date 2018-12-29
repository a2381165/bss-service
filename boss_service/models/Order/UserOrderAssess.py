
# -*- coding: utf-8 -*-
from config import db


class UserOrderAssess(db.Model):
    __tablename__ = "zzh_user_order_assess"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    item_title = db.Column(db.String(255))
    item_url = db.Column(db.String(255))
    assess_status = db.Column(db.SmallInteger)
    assess_person = db.Column(db.String(100))
    assess_time = db.Column(db.DateTime)
    assess_remark = db.Column(db.String(255))
    counselor_id = db.Column(db.Integer)
    manage_counselor_id = db.Column(db.Integer)
    require_list = db.Column(db.Text)

    def __init__(self,order_no,service_no,item_title,item_url,assess_status,assess_person,assess_time,assess_remark,counselor_id,manage_counselor_id,require_list):
        '''Constructor'''
        self.order_no=order_no
        self.service_no=service_no
        self.item_title=item_title
        self.item_url=item_url
        self.assess_status=assess_status
        self.assess_person=assess_person
        self.assess_time=assess_time
        self.assess_remark=assess_remark
        self.counselor_id=counselor_id
        self.manage_counselor_id=manage_counselor_id
        self.require_list=require_list


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'serviceNo', u'itemTitle', u'itemUrl', u'assessStatus', u'assessPerson', u'assessTime', u'assessRemark', u'counselorId', u'manageCounselorId', u'requireList'}
UserOrderAssessChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "serviceNo":"service_no",
    "itemTitle":"item_title",
    "itemUrl":"item_url",
    "assessStatus":"assess_status",
    "assessPerson":"assess_person",
    "assessTime":"assess_time",
    "assessRemark":"assess_remark",
    "counselorId":"counselor_id",
    "manageCounselorId":"manage_counselor_id",
    "requireList":"require_list"
}

intList = {u'id', u'assessStatus', u'counselorId', u'manageCounselorId'}

# db.create_all()
