# -*- coding: utf-8 -*-
from config import db


class ContractSettlement(db.Model):
    __tablename__ = "boss_contract_settlement"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    enterprise_id = db.Column(db.Integer)
    customer_name = db.Column(db.String(100))
    contract_name = db.Column(db.String(255))
    contract_no = db.Column(db.String(64))
    contract_price = db.Column(db.Numeric(10, 2))
    suggest_person = db.Column(db.String(20))
    suggest_price = db.Column(db.String(255))
    manage_person = db.Column(db.String(20))
    manage_price = db.Column(db.Numeric(10, 2))
    business_person = db.Column(db.String(20))
    business_price = db.Column(db.Numeric(10, 2))
    edit_person = db.Column(db.String(20))
    edit_price = db.Column(db.Numeric(10, 2))
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)

    def __init__(self, task_id, enterprise_id, customer_name, contract_name, contract_no, contract_price,
                 suggest_person, suggest_price, manage_person, manage_price, business_person, business_price,
                 edit_person, edit_price, create_person, create_time, execute_person, execute_time, is_done):
        '''Constructor'''
        self.task_id = task_id
        self.enterprise_id = enterprise_id
        self.customer_name = customer_name
        self.contract_name = contract_name
        self.contract_no = contract_no
        self.contract_price = contract_price
        self.suggest_person = suggest_person
        self.suggest_price = suggest_price
        self.manage_person = manage_person
        self.manage_price = manage_price
        self.business_person = business_person
        self.business_price = business_price
        self.edit_person = edit_person
        self.edit_price = edit_price
        self.create_person = create_person
        self.create_time = create_time
        self.execute_person = execute_person
        self.execute_time = execute_time
        self.is_done = is_done

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'taskId', 'enterpriseId', 'customerName', 'contractName', 'contractNo', 'contractPrice',
              'suggestPerson', 'suggestPrice', 'managePerson', 'managePrice', 'businessPerson', 'businessPrice',
              'editPerson', 'editPrice', 'createPerson', 'createTime', 'executePerson', 'executeTime', 'isDone']
ContractSettlementChangeDic = {
    "id": "id",
    "taskId": "task_id",
    "enterpriseId": "enterprise_id",
    "customerName": "customer_name",
    "contractName": "contract_name",
    "contractNo": "contract_no",
    "contractPrice": "contract_price",
    "suggestPerson": "suggest_person",
    "suggestPrice": "suggest_price",
    "managePerson": "manage_person",
    "managePrice": "manage_price",
    "businessPerson": "business_person",
    "businessPrice": "business_price",
    "editPerson": "edit_person",
    "editPrice": "edit_price",
    "createPerson": "create_person",
    "createTime": "create_time",
    "executePerson": "execute_person",
    "executeTime": "execute_time",
    "isDone": "is_done"
}

intList = ['id', 'taskId', 'enterpriseId', 'isDone']

# db.create_all()
