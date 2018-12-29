
# -*- coding: utf-8 -*-
from config import db


class UserOrderEdit(db.Model):
    __tablename__ = "zzh_user_order_edit"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    item_title = db.Column(db.String(255))
    specific_fund = db.Column(db.Numeric(8,2))
    edit_status = db.Column(db.SmallInteger)
    edit_remark = db.Column(db.String(255))
    audit_person = db.Column(db.String(10))
    audit_time = db.Column(db.DateTime)
    audit_status = db.Column(db.SmallInteger)
    audit_remark = db.Column(db.String(255))
    counselor_id = db.Column(db.Integer)
    manage_counselor_id = db.Column(db.Integer)
    require_list = db.Column(db.Text)
    manuscript_time = db.Column(db.DateTime)
    declare_name = db.Column(db.String(255))
    edit_time = db.Column(db.DateTime)
    edit_annex = db.Column(db.String(255))

    def __init__(self, id,order_no,service_no,item_title,specific_fund,edit_status,edit_remark,audit_person,audit_time,audit_status,audit_remark,counselor_id,manage_counselor_id,require_list,manuscript_time,declare_name,edit_time,edit_annex):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.service_no=service_no
        self.item_title=item_title
        self.specific_fund=specific_fund
        self.edit_status=edit_status
        self.edit_remark=edit_remark
        self.audit_person=audit_person
        self.audit_time=audit_time
        self.audit_status=audit_status
        self.audit_remark=audit_remark
        self.counselor_id=counselor_id
        self.manage_counselor_id=manage_counselor_id
        self.require_list=require_list
        self.manuscript_time=manuscript_time
        self.declare_name=declare_name
        self.edit_time=edit_time
        self.edit_annex=edit_annex


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'serviceNo', u'itemTitle', u'specificFund', u'editStatus', u'editRemark', u'auditPerson', u'auditTime', u'auditStatus', u'auditRemark', u'counselorId', u'manageCounselorId', u'requireList', u'manuscriptTime', u'declareName', u'editTime', u'editAnnex'}
UserOrderEditChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "serviceNo":"service_no",
    "itemTitle":"item_title",
    "specificFund":"specific_fund",
    "editStatus":"edit_status",
    "editRemark":"edit_remark",
    "auditPerson":"audit_person",
    "auditTime":"audit_time",
    "auditStatus":"audit_status",
    "auditRemark":"audit_remark",
    "counselorId":"counselor_id",
    "manageCounselorId":"manage_counselor_id",
    "requireList":"require_list",
    "manuscriptTime":"manuscript_time",
    "declareName":"declare_name",
    "editTime":"edit_time",
    "editAnnex":"edit_annex"
}

intList = {u'id', u'editStatus', u'auditStatus', u'counselorId', u'manageCounselorId'}

# db.create_all()
