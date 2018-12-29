# -*- coding: utf-8 -*-
from config import db


class UserOrderProject(db.Model):
    __tablename__ = "zzh_user_order_project"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    item_title = db.Column(db.String(255))
    specific_fund = db.Column(db.String(255))
    project_status = db.Column(db.SmallInteger)
    project_code = db.Column(db.String(20))
    project_fund = db.Column(db.Numeric(15, 2))
    project_date = db.Column(db.DateTime)
    project_remark = db.Column(db.String(255))
    audit_person = db.Column(db.String(10))
    audit_time = db.Column(db.DateTime)
    audit_status = db.Column(db.SmallInteger)
    audit_remark = db.Column(db.String(255))
    counselor_id = db.Column(db.Integer)
    manage_counselor_id = db.Column(db.Integer)
    project_start_time = db.Column(db.DateTime)
    project_end_time = db.Column(db.DateTime)
    project_name = db.Column(db.String(255))

    def __init__(self, order_no, service_no, item_title, specific_fund, project_status, project_code, project_fund,
                 project_date, project_remark, audit_person, audit_time, audit_status, audit_remark, counselor_id,
                 manage_counselor_id, project_start_time, project_end_time, project_name):
        '''Constructor'''
        self.order_no = order_no
        self.service_no = service_no
        self.item_title = item_title
        self.specific_fund = specific_fund
        self.project_status = project_status
        self.project_code = project_code
        self.project_fund = project_fund
        self.project_date = project_date
        self.project_remark = project_remark
        self.audit_person = audit_person
        self.audit_time = audit_time
        self.audit_status = audit_status
        self.audit_remark = audit_remark
        self.counselor_id = counselor_id
        self.manage_counselor_id = manage_counselor_id
        self.project_start_time = project_start_time
        self.project_end_time = project_end_time
        self.project_name = project_name

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'serviceNo', u'itemTitle', u'specificFund', u'projectStatus', u'projectCode',
              u'projectFund', u'projectDate', u'projectRemark', u'auditPerson', u'auditTime', u'auditStatus',
              u'auditRemark', u'counselorId', u'manageCounselorId', u'projectStartTime', u'projectEndTime',
              u'projectName'}
UserOrderProjectChangeDic = {
    "id": "id",
    "orderNo": "order_no",
    "serviceNo": "service_no",
    "itemTitle": "item_title",
    "specificFund": "specific_fund",
    "projectStatus": "project_status",
    "projectCode": "project_code",
    "projectFund": "project_fund",
    "projectDate": "project_date",
    "projectRemark": "project_remark",
    "auditPerson": "audit_person",
    "auditTime": "audit_time",
    "auditStatus": "audit_status",
    "auditRemark": "audit_remark",
    "counselorId": "counselor_id",
    "manageCounselorId": "manage_counselor_id",
    "projectStartTime": "project_start_time",
    "projectEndTime": "project_end_time",
    "projectName": "project_name"
}

intList = {u'id', u'projectStatus', u'auditStatus', u'counselorId', u'manageCounselorId'}

# db.create_all()
