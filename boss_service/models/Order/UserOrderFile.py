# -*- coding: utf-8 -*-
from config import db


class UserOrderFile(db.Model):
    __tablename__ = "zzh_user_order_file"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    item_title = db.Column(db.String(255))
    specific_fund = db.Column(db.String(255))
    file_status = db.Column(db.SmallInteger)
    file_date = db.Column(db.DateTime)
    project_status = db.Column(db.SmallInteger)
    project_code = db.Column(db.String(20))
    project_fund = db.Column(db.String(255))
    project_date = db.Column(db.DateTime)
    file_annex = db.Column(db.String(65535))
    file_remark = db.Column(db.String(65535))
    counselor_id = db.Column(db.Integer)
    manage_counselor_id = db.Column(db.Integer)
    require_list = db.Column(db.Text)

    def __init__(self, order_no, service_no, item_title, specific_fund, file_status, file_date, project_status,
                 project_code, project_fund, project_date, file_annex, file_remark, counselor_id, manage_counselor_id,
                 require_list):
        '''Constructor'''
        self.order_no = order_no
        self.service_no = service_no
        self.item_title = item_title
        self.specific_fund = specific_fund
        self.file_status = file_status
        self.file_date = file_date
        self.project_status = project_status
        self.project_code = project_code
        self.project_fund = project_fund
        self.project_date = project_date
        self.file_annex = file_annex
        self.file_remark = file_remark
        self.counselor_id = counselor_id
        self.manage_counselor_id = manage_counselor_id
        self.require_list = require_list

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'serviceNo', u'itemTitle', u'specificFund', u'fileStatus', u'fileDate',
              u'projectStatus', u'projectCode', u'projectFund', u'projectDate', u'fileAnnex', u'fileRemark',
              u'counselorId', u'manageCounselorId', u'requireList'}
UserOrderFileChangeDic = {
    "id": "id",
    "orderNo": "order_no",
    "serviceNo": "service_no",
    "itemTitle": "item_title",
    "specificFund": "specific_fund",
    "fileStatus": "file_status",
    "fileDate": "file_date",
    "projectStatus": "project_status",
    "projectCode": "project_code",
    "projectFund": "project_fund",
    "projectDate": "project_date",
    "fileAnnex": "file_annex",
    "fileRemark": "file_remark",
    "counselorId": "counselor_id",
    "manageCounselorId": "manage_counselor_id",
    "requireList": "require_list"
}

intList = {u'id', u'fileStatus', u'projectStatus', u'counselorId', u'manageCounselorId'}

# db.create_all()
