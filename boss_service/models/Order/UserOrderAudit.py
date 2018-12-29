
# -*- coding: utf-8 -*-
from config import db


class UserOrderAudit(db.Model):
    __tablename__ = "zzh_user_order_audit"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    audit_type = db.Column(db.String(2))
    audit_person = db.Column(db.String(20))
    audit_time = db.Column(db.DateTime)
    audit_status = db.Column(db.SmallInteger)
    audit_remark = db.Column(db.String(255))

    def __init__(self, id,order_no,audit_type,audit_person,audit_time,audit_status,audit_remark):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.audit_type=audit_type
        self.audit_person=audit_person
        self.audit_time=audit_time
        self.audit_status=audit_status
        self.audit_remark=audit_remark


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'auditType', u'auditPerson', u'auditTime', u'auditStatus', u'auditRemark'}
UserOrderAuditChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "auditType":"audit_type",
    "auditPerson":"audit_person",
    "auditTime":"audit_time",
    "auditStatus":"audit_status",
    "auditRemark":"audit_remark"
}

intList = {u'id', u'auditStatus'}

# db.create_all()
