
# -*- coding: utf-8 -*-
from config import db


class CounselorAccountCertification(db.Model):
    __tablename__ = "counselor_account_certification"

    counselor_id = db.Column(db.Integer, primary_key=True, nullable=False)
    counselor_payee = db.Column(db.String(20))
    counselor_receipt_method = db.Column(db.SmallInteger)
    counselor_receipt_bank = db.Column(db.String(40))
    counselor_receipt_account = db.Column(db.String(20))
    check_id = db.Column(db.Integer)
    counselor_receipt_code = db.Column(db.String(18))

    def __init__(self, counselor_id,counselor_payee,counselor_receipt_method,counselor_receipt_bank,counselor_receipt_account,check_id,counselor_receipt_code):
        '''Constructor'''
        self.counselor_id=counselor_id
        self.counselor_payee=counselor_payee
        self.counselor_receipt_method=counselor_receipt_method
        self.counselor_receipt_bank=counselor_receipt_bank
        self.counselor_receipt_account=counselor_receipt_account
        self.check_id=check_id
        self.counselor_receipt_code=counselor_receipt_code


    def __repr__(self):
        return 'counselor_id : %s' % self.counselor_id


# Client and database attributes dictionary
clinetHead = {u'counselorId', u'counselorPayee', u'counselorReceiptMethod', u'counselorReceiptBank', u'counselorReceiptAccount', u'checkId', u'counselorReceiptCode'}
CounselorAccountCertificationChangeDic = {
    "counselorId":"counselor_id",
    "counselorPayee":"counselor_payee",
    "counselorReceiptMethod":"counselor_receipt_method",
    "counselorReceiptBank":"counselor_receipt_bank",
    "counselorReceiptAccount":"counselor_receipt_account",
    "checkId":"check_id",
    "counselorReceiptCode":"counselor_receipt_code"
}

intList = {u'counselorId', u'counselorReceiptMethod', u'checkId'}

# db.create_all()
