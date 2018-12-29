# -*- coding: utf-8 -*-
from config import db


class MemberEnterpriseCertificationCheck(db.Model):
    __tablename__ = "zzh_member_enterprise_certification_check"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    member_id = db.Column(db.Integer)
    member_name = db.Column(db.String(50))
    member_unit_type = db.Column(db.String(20))
    member_credit_code = db.Column(db.String(32))
    member_credit_url = db.Column(db.BLOB)
    member_legal_person = db.Column(db.String(20))
    member_registered_capital = db.Column(db.Numeric(15, 2))
    member_registered_address = db.Column(db.String(100))
    member_found_date = db.Column(db.DateTime)
    member_business_scope = db.Column(db.String(255))
    member_mailing_address = db.Column(db.String(100))
    audit_person = db.Column(db.String(100))
    audit_time = db.Column(db.DateTime)
    audit_status = db.Column(db.SmallInteger)
    audit_remark = db.Column(db.String(255))
    check_member_type = db.Column(db.SmallInteger)
    member_enterprise_id = db.Column(db.Integer)
    manage_id = db.Column(db.Integer)

    def __init__(self, member_id, member_name, member_unit_type, member_credit_code, member_credit_url,
                 member_legal_person, member_registered_capital, member_registered_address, member_found_date,
                 member_business_scope, member_mailing_address, audit_person, audit_time, audit_status, audit_remark,
                 check_member_type, member_enterprise_id, manage_id):
        '''Constructor'''
        self.member_id = member_id
        self.member_name = member_name
        self.member_unit_type = member_unit_type
        self.member_credit_code = member_credit_code
        self.member_credit_url = member_credit_url
        self.member_legal_person = member_legal_person
        self.member_registered_capital = member_registered_capital
        self.member_registered_address = member_registered_address
        self.member_found_date = member_found_date
        self.member_business_scope = member_business_scope
        self.member_mailing_address = member_mailing_address
        self.audit_person = audit_person
        self.audit_time = audit_time
        self.audit_status = audit_status
        self.audit_remark = audit_remark
        self.check_member_type = check_member_type
        self.member_enterprise_id = member_enterprise_id
        self.manage_id = manage_id

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'memberId', 'memberName', 'memberUnitType', 'memberCreditCode', 'memberCreditUrl',
              'memberLegalPerson', 'memberRegisteredCapital', 'memberRegisteredAddress', 'memberFoundDate',
              'memberBusinessScope', 'memberMailingAddress', 'auditPerson', 'auditTime', 'auditStatus', 'auditRemark',
              'checkMemberType', 'memberEnterpriseId', 'manageId']
MemberEnterpriseCertificationCheckChangeDic = {
    "id": "id",
    "memberId": "member_id",
    "memberName": "member_name",
    "memberUnitType": "member_unit_type",
    "memberCreditCode": "member_credit_code",
    "memberCreditUrl": "member_credit_url",
    "memberLegalPerson": "member_legal_person",
    "memberRegisteredCapital": "member_registered_capital",
    "memberRegisteredAddress": "member_registered_address",
    "memberFoundDate": "member_found_date",
    "memberBusinessScope": "member_business_scope",
    "memberMailingAddress": "member_mailing_address",
    "auditPerson": "audit_person",
    "auditTime": "audit_time",
    "auditStatus": "audit_status",
    "auditRemark": "audit_remark",
    "checkMemberType": "check_member_type",
    "memberEnterpriseId": "member_enterprise_id",
    "manageId": "manage_id"
}

intList = ['id', 'memberId', 'auditStatus', 'checkMemberType', 'memberEnterpriseId', 'manageId']

# db.create_all()
