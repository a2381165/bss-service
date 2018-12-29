# -*- coding: utf-8 -*-
from config import db


class UserOrderAccept(db.Model):
    __tablename__ = "zzh_user_order_accept"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    item_title = db.Column(db.String(255))
    specific_fund = db.Column(db.Integer)
    is_system = db.Column(db.SmallInteger)
    is_paper = db.Column(db.SmallInteger)
    declare_name = db.Column(db.String(50))
    pre_project_time = db.Column(db.DateTime)
    accept_status = db.Column(db.SmallInteger)
    accept_remark = db.Column(db.String(255))
    audit_person = db.Column(db.String(10))
    audit_time = db.Column(db.DateTime)
    audit_status = db.Column(db.SmallInteger)
    audit_remark = db.Column(db.String(255))
    counselor_id = db.Column(db.Integer)
    manage_counselor_id = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    require_list = db.Column(db.Text)
    accept_time = db.Column(db.DateTime)

    def __init__(self, order_no, service_no, item_title, specific_fund, is_system, is_paper, declare_name,
                 pre_project_time, accept_status, accept_remark, audit_person, audit_time, audit_status, audit_remark,
                 counselor_id, manage_counselor_id, image_url, require_list, accept_time):
        '''Constructor'''
        self.order_no = order_no
        self.service_no = service_no
        self.item_title = item_title
        self.specific_fund = specific_fund
        self.is_system = is_system
        self.is_paper = is_paper
        self.declare_name = declare_name
        self.pre_project_time = pre_project_time
        self.accept_status = accept_status
        self.accept_remark = accept_remark
        self.audit_person = audit_person
        self.audit_time = audit_time
        self.audit_status = audit_status
        self.audit_remark = audit_remark
        self.counselor_id = counselor_id
        self.manage_counselor_id = manage_counselor_id
        self.image_url = image_url
        self.require_list = require_list
        self.accept_time = accept_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'serviceNo', u'itemTitle', u'specificFund', u'isSystem', u'isPaper', u'declareName',
              u'preProjectTime', u'acceptStatus', u'acceptRemark', u'auditPerson', u'auditTime', u'auditStatus',
              u'auditRemark', u'counselorId', u'manageCounselorId', u'imageUrl', u'requireList', u'acceptTime'}
UserOrderAcceptChangeDic = {
    "id": "id",
    "orderNo": "order_no",
    "serviceNo": "service_no",
    "itemTitle": "item_title",
    "specificFund": "specific_fund",
    "isSystem": "is_system",
    "isPaper": "is_paper",
    "declareName": "declare_name",
    "preProjectTime": "pre_project_time",
    "acceptStatus": "accept_status",
    "acceptRemark": "accept_remark",
    "auditPerson": "audit_person",
    "auditTime": "audit_time",
    "auditStatus": "audit_status",
    "auditRemark": "audit_remark",
    "counselorId": "counselor_id",
    "manageCounselorId": "manage_counselor_id",
    "imageUrl": "image_url",
    "requireList": "require_list",
    "acceptTime": "accept_time"
}

intList = {u'id', u'specificFund', u'isSystem', u'isPaper', u'acceptStatus', u'auditStatus', u'counselorId',
           u'manageCounselorId'}

# db.create_all()
