# -*- coding: utf-8 -*-
from config import db


class MemberEnterpriseCertification(db.Model):
    __tablename__ = "zzh_member_enterprise_certification"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
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
    manage_id = db.Column(db.Integer)

    def __init__(self, member_name, member_unit_type, member_credit_code, member_credit_url, member_legal_person,
                 member_registered_capital, member_registered_address, member_found_date, member_business_scope,
                 member_mailing_address, manage_id):
        '''Constructor'''
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
        self.manage_id = manage_id

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'memberName', 'memberUnitType', 'memberCreditCode', 'memberCreditUrl', 'memberLegalPerson',
              'memberRegisteredCapital', 'memberRegisteredAddress', 'memberFoundDate', 'memberBusinessScope',
              'memberMailingAddress', 'manageId']
MemberEnterpriseCertificationChangeDic = {
    "id": "id",
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
    "manageId": "manage_id"
}

intList = ['id', 'manageId']

# db.create_all()
