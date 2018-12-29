# -*- coding: utf-8 -*-
from config import db


class MemberEnterpriseContactInfo(db.Model):
    __tablename__ = "zzh_member_enterprise_contact_info"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    enterprise_id = db.Column(db.Integer)
    contract_person = db.Column(db.String(20))
    contract_phone = db.Column(db.String(11))
    contract_duty = db.Column(db.String(50))
    contract_email = db.Column(db.String(30))
    contract_weixin = db.Column(db.String(30))

    def __init__(self, enterprise_id, contract_person, contract_phone, contract_duty, contract_email, contract_weixin):
        '''Constructor'''
        self.enterprise_id = enterprise_id
        self.contract_person = contract_person
        self.contract_phone = contract_phone
        self.contract_duty = contract_duty
        self.contract_email = contract_email
        self.contract_weixin = contract_weixin

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'enterpriseId', 'contractPerson', 'contractPhone', 'contractDuty', 'contractEmail',
              'contractWeixin']
MemberEnterpriseContactInfoChangeDic = {
    "id": "id",
    "enterpriseId": "enterprise_id",
    "contractPerson": "contract_person",
    "contractPhone": "contract_phone",
    "contractDuty": "contract_duty",
    "contractEmail": "contract_email",
    "contractWeixin": "contract_weixin"
}

intList = ['id', 'enterpriseId']

# db.create_all()
