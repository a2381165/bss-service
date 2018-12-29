
# -*- coding: utf-8 -*-
from config import db


class MemberTempContract(db.Model):
    __tablename__ = "data_member_temp_contract"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    contract_no = db.Column(db.String(70))
    contract_name = db.Column(db.String(255))
    contract_remark = db.Column(db.String(255))
    product_name = db.Column(db.String(20))
    contract_price = db.Column(db.Numeric(10,2))
    start_fee = db.Column(db.Numeric(10,2))
    project_fee = db.Column(db.Numeric(10,2))
    project_rate = db.Column(db.Integer)
    contract_type = db.Column(db.SmallInteger)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    create_person = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)

    def __init__(self,task_id,order_no,service_no,contract_no,contract_name,contract_remark,product_name,contract_price,start_fee,project_fee,project_rate,contract_type,start_time,end_time,create_person,create_time,execute_person,execute_time,is_done):
        '''Constructor'''
        self.task_id=task_id
        self.order_no=order_no
        self.service_no=service_no
        self.contract_no=contract_no
        self.contract_name=contract_name
        self.contract_remark=contract_remark
        self.product_name=product_name
        self.contract_price=contract_price
        self.start_fee=start_fee
        self.project_fee=project_fee
        self.project_rate=project_rate
        self.contract_type=contract_type
        self.start_time=start_time
        self.end_time=end_time
        self.create_person=create_person
        self.create_time=create_time
        self.execute_person=execute_person
        self.execute_time=execute_time
        self.is_done=is_done


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id','taskId','orderNo','serviceNo','contractNo','contractName','contractRemark','productName','contractPrice','startFee','projectFee','projectRate','contractType','startTime','endTime','createPerson','createTime','executePerson','executeTime','isDone']
MemberTempContractChangeDic = {
    "id":"id",
    "taskId":"task_id",
    "orderNo":"order_no",
    "serviceNo":"service_no",
    "contractNo":"contract_no",
    "contractName":"contract_name",
    "contractRemark":"contract_remark",
    "productName":"product_name",
    "contractPrice":"contract_price",
    "startFee":"start_fee",
    "projectFee":"project_fee",
    "projectRate":"project_rate",
    "contractType":"contract_type",
    "startTime":"start_time",
    "endTime":"end_time",
    "createPerson":"create_person",
    "createTime":"create_time",
    "executePerson":"execute_person",
    "executeTime":"execute_time",
    "isDone":"is_done"
}

intList = ['id','taskId','projectRate','contractType','isDone']

# db.create_all()
