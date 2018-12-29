
# -*- coding: utf-8 -*-
from config import db

class EditSettlement(db.Model):
    __tablename__ = "boss_edit_settlement"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    counselor_id = db.Column(db.Integer)
    customer_name = db.Column(db.String(20))
    project_name = db.Column(db.String(50))
    declaration_limit = db.Column(db.Numeric(12,2))
    declaration_plan = db.Column(db.String(255))
    edit_fee = db.Column(db.Numeric(10,2))
    accept_fee = db.Column(db.Numeric(10,2))
    royalty_base = db.Column(db.Float(3))
    royalty_ratio = db.Column(db.SmallInteger)
    project_royalty = db.Column(db.Numeric(10,2))
    actual_payment = db.Column(db.Numeric(10,2))
    project_status = db.Column(db.SmallInteger)
    remark = db.Column(db.String(200))
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)
    execute_done = db.Column(db.SmallInteger)

    def __init__(self, task_id,counselor_id,customer_name,project_name,declaration_limit,declaration_plan,edit_fee,accept_fee,royalty_base,royalty_ratio,project_royalty,actual_payment,project_status,remark,create_person,create_time,execute_person,execute_time,is_done,execute_done):
        '''Constructor'''
        self.task_id=task_id
        self.counselor_id=counselor_id
        self.customer_name=customer_name
        self.project_name=project_name
        self.declaration_limit=declaration_limit
        self.declaration_plan=declaration_plan
        self.edit_fee=edit_fee
        self.accept_fee=accept_fee
        self.royalty_base=royalty_base
        self.royalty_ratio=royalty_ratio
        self.project_royalty=project_royalty
        self.actual_payment=actual_payment
        self.project_status=project_status
        self.remark=remark
        self.create_person=create_person
        self.create_time=create_time
        self.execute_person=execute_person
        self.execute_time=execute_time
        self.is_done=is_done
        self.execute_done=execute_done


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id','taskId','counselorId','customerName','projectName','declarationLimit','declarationPlan','editFee','acceptFee','royaltyBase','royaltyRatio','projectRoyalty','actualPayment','projectStatus','remark','createPerson','createTime','executePerson','executeTime','isDone','executeDone']
EditSettlementChangeDic = {
    "id":"id",
    "taskId":"task_id",
    "counselorId":"counselor_id",
    "customerName":"customer_name",
    "projectName":"project_name",
    "declarationLimit":"declaration_limit",
    "declarationPlan":"declaration_plan",
    "editFee":"edit_fee",
    "acceptFee":"accept_fee",
    "royaltyBase":"royalty_base",
    "royaltyRatio":"royalty_ratio",
    "projectRoyalty":"project_royalty",
    "actualPayment":"actual_payment",
    "projectStatus":"project_status",
    "remark":"remark",
    "createPerson":"create_person",
    "createTime":"create_time",
    "executePerson":"execute_person",
    "executeTime":"execute_time",
    "isDone":"is_done",
    "executeDone":"execute_done"
}

intList = ['id','taskId','counselorId','royaltyRatio','projectStatus','isDone','executeDone']

# db.create_all()
