
# -*- coding: utf-8 -*-
from config import db


class CounselorBases(db.Model):
    __tablename__ = "counselor_bases"

    counselor_id = db.Column(db.Integer, primary_key=True, nullable=False)
    counselor_type = db.Column(db.SmallInteger)
    invited_code = db.Column(db.String(20))
    counselor_code = db.Column(db.String(20))
    counselor_points = db.Column(db.Integer)
    counselor_balance = db.Column(db.Numeric(11,2))
    is_payment_account = db.Column(db.SmallInteger)
    is_check = db.Column(db.SmallInteger)
    counselor_contact_email = db.Column(db.String(50))
    counselor_contact_person = db.Column(db.String(20))
    counselor_contact_phone = db.Column(db.String(20))
    area_code = db.Column(db.String(6))
    counselor_person_id = db.Column(db.Integer)
    counselor_enterprise_id = db.Column(db.Integer)
    counselor_name = db.Column(db.String(20))
    counselor_rank = db.Column(db.Integer)

    def __init__(self, counselor_id,counselor_type,invited_code,counselor_code,counselor_points,counselor_balance,is_payment_account,is_check,counselor_contact_email,counselor_contact_person,counselor_contact_phone,area_code,counselor_person_id,counselor_enterprise_id,counselor_name,counselor_rank):
        '''Constructor'''
        self.counselor_id=counselor_id
        self.counselor_type=counselor_type
        self.invited_code=invited_code
        self.counselor_code=counselor_code
        self.counselor_points=counselor_points
        self.counselor_balance=counselor_balance
        self.is_payment_account=is_payment_account
        self.is_check=is_check
        self.counselor_contact_email=counselor_contact_email
        self.counselor_contact_person=counselor_contact_person
        self.counselor_contact_phone=counselor_contact_phone
        self.area_code=area_code
        self.counselor_person_id=counselor_person_id
        self.counselor_enterprise_id=counselor_enterprise_id
        self.counselor_name=counselor_name
        self.counselor_rank=counselor_rank


    def __repr__(self):
        return 'counselor_id : %s' % self.counselor_id


# Client and database attributes dictionary
clinetHead = {u'counselorId', u'counselorType', u'invitedCode', u'counselorCode', u'counselorPoints', u'counselorBalance', u'isPaymentAccount', u'isCheck', u'counselorContactEmail', u'counselorContactPerson', u'counselorContactPhone', u'areaCode', u'counselorPersonId', u'counselorEnterpriseId', u'counselorName', u'counselorRank'}
CounselorBasesChangeDic = {
    "counselorId":"counselor_id",
    "counselorType":"counselor_type",
    "invitedCode":"invited_code",
    "counselorCode":"counselor_code",
    "counselorPoints":"counselor_points",
    "counselorBalance":"counselor_balance",
    "isPaymentAccount":"is_payment_account",
    "isCheck":"is_check",
    "counselorContactEmail":"counselor_contact_email",
    "counselorContactPerson":"counselor_contact_person",
    "counselorContactPhone":"counselor_contact_phone",
    "areaCode":"area_code",
    "counselorPersonId":"counselor_person_id",
    "counselorEnterpriseId":"counselor_enterprise_id",
    "counselorName":"counselor_name",
    "counselorRank":"counselor_rank"
}

intList = {u'counselorId', u'counselorType', u'counselorPoints', u'isPaymentAccount', u'isCheck', u'counselorPersonId', u'counselorEnterpriseId', u'counselorRank'}

# db.create_all()
