# -*- coding: utf-8 -*-
from config import db


class EnterpriseInformation(db.Model):
    __tablename__ = "zzh_enterprise_information"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    member_name = db.Column(db.String(100))
    member_credit_code = db.Column(db.String(100))
    member_registered_account = db.Column(db.String(100))
    member_organization_code = db.Column(db.String(100))
    member_province = db.Column(db.String(64))
    member_unit_type = db.Column(db.String(100))
    member_industry = db.Column(db.String(64))
    member_legal_person = db.Column(db.String(64))
    member_registered_capital = db.Column(db.String(64))
    member_registered_time = db.Column(db.DateTime)
    member_business_start = db.Column(db.DateTime)
    member_business_end = db.Column(db.DateTime)
    approval_authority = db.Column(db.String(100))
    approval_date = db.Column(db.DateTime)
    member_business_scope = db.Column(db.Text)
    member_mailing_address = db.Column(db.String(100))
    member_phone = db.Column(db.String(255))
    member_email = db.Column(db.String(255))
    member_website = db.Column(db.Text)
    member_status = db.Column(db.String(64))

    def __init__(self, member_name, member_credit_code, member_registered_account, member_organization_code,
                 member_province, member_unit_type, member_industry, member_legal_person, member_registered_capital,
                 member_registered_time, member_business_start, member_business_end, approval_authority, approval_date,
                 member_business_scope, member_mailing_address, member_phone, member_email, member_website,
                 member_status):
        '''Constructor'''
        self.member_name = member_name
        self.member_credit_code = member_credit_code
        self.member_registered_account = member_registered_account
        self.member_organization_code = member_organization_code
        self.member_province = member_province
        self.member_unit_type = member_unit_type
        self.member_industry = member_industry
        self.member_legal_person = member_legal_person
        self.member_registered_capital = member_registered_capital
        self.member_registered_time = member_registered_time
        self.member_business_start = member_business_start
        self.member_business_end = member_business_end
        self.approval_authority = approval_authority
        self.approval_date = approval_date
        self.member_business_scope = member_business_scope
        self.member_mailing_address = member_mailing_address
        self.member_phone = member_phone
        self.member_email = member_email
        self.member_website = member_website
        self.member_status = member_status

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'memberName', 'memberCreditCode', 'memberRegisteredAccount', 'memberOrganizationCode',
              'memberProvince', 'memberUnitType', 'memberIndustry', 'memberLegalPerson', 'memberRegisteredCapital',
              'memberRegisteredTime', 'memberBusinessStart', 'memberBusinessEnd', 'approvalAuthority', 'approvalDate',
              'memberBusinessScope', 'memberMailingAddress', 'memberPhone', 'memberEmail', 'memberWebsite',
              'memberStatus']
EnterpriseInformationChangeDic = {
    "id": "id",
    "memberName": "member_name",
    "memberCreditCode": "member_credit_code",
    "memberRegisteredAccount": "member_registered_account",
    "memberOrganizationCode": "member_organization_code",
    "memberProvince": "member_province",
    "memberUnitType": "member_unit_type",
    "memberIndustry": "member_industry",
    "memberLegalPerson": "member_legal_person",
    "memberRegisteredCapital": "member_registered_capital",
    "memberRegisteredTime": "member_registered_time",
    "memberBusinessStart": "member_business_start",
    "memberBusinessEnd": "member_business_end",
    "approvalAuthority": "approval_authority",
    "approvalDate": "approval_date",
    "memberBusinessScope": "member_business_scope",
    "memberMailingAddress": "member_mailing_address",
    "memberPhone": "member_phone",
    "memberEmail": "member_email",
    "memberWebsite": "member_website",
    "memberStatus": "member_status"
}

intList = ['id']

# db.create_all()
