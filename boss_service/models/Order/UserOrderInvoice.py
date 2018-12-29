
# -*- coding: utf-8 -*-
from config import db


class UserOrderInvoice(db.Model):
    __tablename__ = "zzh_user_order_invoice"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    invoice_header = db.Column(db.String(20))
    invoice_type = db.Column(db.SmallInteger)
    invoice_content = db.Column(db.String(200))
    invoice_tax_code = db.Column(db.String(20))
    invoice_bank = db.Column(db.String(20))
    invoice_bank_account = db.Column(db.String(20))
    invoice_registered_address = db.Column(db.String(50))
    invoice_telephone = db.Column(db.String(20))
    invoice_status = db.Column(db.Integer)

    def __init__(self, id,order_no,invoice_header,invoice_type,invoice_content,invoice_tax_code,invoice_bank,invoice_bank_account,invoice_registered_address,invoice_telephone,invoice_status):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.invoice_header=invoice_header
        self.invoice_type=invoice_type
        self.invoice_content=invoice_content
        self.invoice_tax_code=invoice_tax_code
        self.invoice_bank=invoice_bank
        self.invoice_bank_account=invoice_bank_account
        self.invoice_registered_address=invoice_registered_address
        self.invoice_telephone=invoice_telephone
        self.invoice_status=invoice_status


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'invoiceHeader', u'invoiceType', u'invoiceContent', u'invoiceTaxCode', u'invoiceBank', u'invoiceBankAccount', u'invoiceRegisteredAddress', u'invoiceTelephone', u'invoiceStatus'}
UserOrderInvoiceChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "invoiceHeader":"invoice_header",
    "invoiceType":"invoice_type",
    "invoiceContent":"invoice_content",
    "invoiceTaxCode":"invoice_tax_code",
    "invoiceBank":"invoice_bank",
    "invoiceBankAccount":"invoice_bank_account",
    "invoiceRegisteredAddress":"invoice_registered_address",
    "invoiceTelephone":"invoice_telephone",
    "invoiceStatus":"invoice_status"
}

intList = {u'id', u'invoiceType', u'invoiceStatus'}

# db.create_all()
