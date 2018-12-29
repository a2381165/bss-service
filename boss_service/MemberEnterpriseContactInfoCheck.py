# -*- coding: utf-8 -*-
from config import db


class MemberEnterpriseContactInfoCheck(db.Model):
    __tablename__ = "zzh_member_enterprise_contact_info_check"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    enterprise_id = db.Column(db.Integer)
    contract_person = db.Column(db.String(20))
    contract_phone = db.Column(db.String(11))
    contract_duty = db.Column(db.String(50))
    contract_email = db.Column(db.String(30))
    contract_weixin = db.Column(db.String(30))
    audit_person = db.Column(db.String(100))
    audit_time = db.Column(db.DateTime)
    audit_status = db.Column(db.SmallInteger)
    audit_remark = db.Column(db.String(255))
    check_member_type = db.Column(db.SmallInteger)
    manage_id = db.Column(db.Integer)

    def __init__(self, enterprise_id, contract_person, contract_phone, contract_duty, contract_email, contract_weixin,
                 audit_person, audit_time, audit_status, audit_remark, check_member_type, manage_id):
        '''Constructor'''
        self.enterprise_id = enterprise_id
        self.contract_person = contract_person
        self.contract_phone = contract_phone
        self.contract_duty = contract_duty
        self.contract_email = contract_email
        self.contract_weixin = contract_weixin
        self.audit_person = audit_person
        self.audit_time = audit_time
        self.audit_status = audit_status
        self.audit_remark = audit_remark
        self.check_member_type = check_member_type
        self.manage_id = manage_id

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'enterpriseId', 'contractPerson', 'contractPhone', 'contractDuty', 'contractEmail',
              'contractWeixin', 'auditPerson', 'auditTime', 'auditStatus', 'auditRemark', 'checkMemberType', 'manageId']
MemberEnterpriseContactInfoCheckChangeDic = {
    "id": "id",
    "enterpriseId": "enterprise_id",
    "contractPerson": "contract_person",
    "contractPhone": "contract_phone",
    "contractDuty": "contract_duty",
    "contractEmail": "contract_email",
    "contractWeixin": "contract_weixin",
    "auditPerson": "audit_person",
    "auditTime": "audit_time",
    "auditStatus": "audit_status",
    "auditRemark": "audit_remark",
    "checkMemberType": "check_member_type",
    "manageId": "manage_id"
}

intList = ['id', 'enterpriseId', 'auditStatus', 'checkMemberType', 'manageId']

# db.create_all()
