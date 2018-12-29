# -*- coding: utf-8 -*-
from config import db


class MemberContract(db.Model):
    __tablename__ = "zzh_member_contract"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    service_no = db.Column(db.String(64))
    item_title = db.Column(db.String(255))
    contract_no = db.Column(db.String(70))
    contract_annex = db.Column(db.String(255))
    contract_remark = db.Column(db.String(255))
    contract_type = db.Column(db.SmallInteger)
    contract_price = db.Column(db.Numeric(10, 2))
    start_fee = db.Column(db.Numeric(10, 2))
    project_fee = db.Column(db.Numeric(10, 2))
    project_rate = db.Column(db.Integer)
    is_generate = db.Column(db.SmallInteger)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    signing_person = db.Column(db.String(20))
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)

    def __init__(self, order_no, service_no, item_title, contract_no, contract_annex, contract_remark, contract_type,
                 contract_price, start_fee, project_fee, project_rate, is_generate, start_time, end_time,
                 signing_person, create_person, create_time):
        '''Constructor'''
        self.order_no = order_no
        self.service_no = service_no
        self.item_title = item_title
        self.contract_no = contract_no
        self.contract_annex = contract_annex
        self.contract_remark = contract_remark
        self.contract_type = contract_type
        self.contract_price = contract_price
        self.start_fee = start_fee
        self.project_fee = project_fee
        self.project_rate = project_rate
        self.is_generate = is_generate
        self.start_time = start_time
        self.end_time = end_time
        self.signing_person = signing_person
        self.create_person = create_person
        self.create_time = create_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'orderNo', 'serviceNo', 'itemTitle', 'contractNo', 'contractAnnex', 'contractRemark',
              'contractType', 'contractPrice', 'startFee', 'projectFee', 'projectRate', 'isGenerate', 'startTime',
              'endTime', 'signingPerson', 'createPerson', 'createTime']
MemberContractChangeDic = {
    "id": "id",
    "orderNo": "order_no",
    "serviceNo": "service_no",
    "itemTitle": "item_title",
    "contractNo": "contract_no",
    "contractAnnex": "contract_annex",
    "contractRemark": "contract_remark",
    "contractType": "contract_type",
    "contractPrice": "contract_price",
    "startFee": "start_fee",
    "projectFee": "project_fee",
    "projectRate": "project_rate",
    "isGenerate": "is_generate",
    "startTime": "start_time",
    "endTime": "end_time",
    "signingPerson": "signing_person",
    "createPerson": "create_person",
    "createTime": "create_time"
}

intList = ['id', 'contractType', 'projectRate', 'isGenerate']

# db.create_all()
