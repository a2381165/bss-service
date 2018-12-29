
# -*- coding: utf-8 -*-
from config import db


class UserOrderContract(db.Model):
    __tablename__ = "zzh_user_order_contract"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    item_title = db.Column(db.String(255))
    contract_no = db.Column(db.String(30))
    contract_status = db.Column(db.SmallInteger)
    contract_annex = db.Column(db.String(255))
    contract_remark = db.Column(db.String(255))
    audit_person = db.Column(db.String(100))
    audit_time = db.Column(db.DateTime)
    audit_status = db.Column(db.SmallInteger)
    audit_remark = db.Column(db.String(255))
    counselor_id = db.Column(db.Integer)
    manage_counselor_id = db.Column(db.Integer)
    contract_type = db.Column(db.SmallInteger)
    contract_price = db.Column(db.Numeric(10,2))
    start_fee = db.Column(db.Numeric(10,2))
    project_fee = db.Column(db.Numeric(10,2))
    project_rate = db.Column(db.Integer)
    counselor_start_fee = db.Column(db.Numeric(10,2))
    counselor_accept_fee = db.Column(db.Numeric(10,2))
    counselor_project_fee = db.Column(db.Numeric(10,2))
    counselor_project_rate = db.Column(db.Integer)
    is_generate = db.Column(db.SmallInteger)

    def __init__(self, id,order_no,service_no,item_title,contract_no,contract_status,contract_annex,contract_remark,audit_person,audit_time,audit_status,audit_remark,counselor_id,manage_counselor_id,contract_type,contract_price,start_fee,project_fee,project_rate,counselor_start_fee,counselor_accept_fee,counselor_project_fee,counselor_project_rate,is_generate):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.service_no=service_no
        self.item_title=item_title
        self.contract_no=contract_no
        self.contract_status=contract_status
        self.contract_annex=contract_annex
        self.contract_remark=contract_remark
        self.audit_person=audit_person
        self.audit_time=audit_time
        self.audit_status=audit_status
        self.audit_remark=audit_remark
        self.counselor_id=counselor_id
        self.manage_counselor_id=manage_counselor_id
        self.contract_type=contract_type
        self.contract_price=contract_price
        self.start_fee=start_fee
        self.project_fee=project_fee
        self.project_rate=project_rate
        self.counselor_start_fee=counselor_start_fee
        self.counselor_accept_fee=counselor_accept_fee
        self.counselor_project_fee=counselor_project_fee
        self.counselor_project_rate=counselor_project_rate
        self.is_generate=is_generate


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'serviceNo', u'itemTitle', u'contractNo', u'contractStatus', u'contractAnnex', u'contractRemark', u'auditPerson', u'auditTime', u'auditStatus', u'auditRemark', u'counselorId', u'manageCounselorId', u'contractType', u'contractPrice', u'startFee', u'projectFee', u'projectRate', u'counselorStartFee', u'counselorAcceptFee', u'counselorProjectFee', u'counselorProjectRate', u'isGenerate'}
UserOrderContractChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "serviceNo":"service_no",
    "itemTitle":"item_title",
    "contractNo":"contract_no",
    "contractStatus":"contract_status",
    "contractAnnex":"contract_annex",
    "contractRemark":"contract_remark",
    "auditPerson":"audit_person",
    "auditTime":"audit_time",
    "auditStatus":"audit_status",
    "auditRemark":"audit_remark",
    "counselorId":"counselor_id",
    "manageCounselorId":"manage_counselor_id",
    "contractType":"contract_type",
    "contractPrice":"contract_price",
    "startFee":"start_fee",
    "projectFee":"project_fee",
    "projectRate":"project_rate",
    "counselorStartFee":"counselor_start_fee",
    "counselorAcceptFee":"counselor_accept_fee",
    "counselorProjectFee":"counselor_project_fee",
    "counselorProjectRate":"counselor_project_rate",
    "isGenerate":"is_generate"
}

intList = {u'id', u'contractStatus', u'auditStatus', u'counselorId', u'manageCounselorId', u'contractType', u'projectRate', u'counselorProjectRate', u'isGenerate'}

# db.create_all()
