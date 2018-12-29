# -*- coding: utf-8 -*-
from config import db


class SingleService(db.Model):
    __tablename__ = "data_single_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    service_id = db.Column(db.Integer)
    customer_name = db.Column(db.String(20))
    service_agency = db.Column(db.String(50))
    service_person = db.Column(db.String(100))
    service_content = db.Column(db.String(1000))
    declare_direction = db.Column(db.String(100))
    manage_dept = db.Column(db.String(50))
    apply_amount = db.Column(db.String(50))
    subsidy_method = db.Column(db.String(500))
    service_deadline = db.Column(db.DateTime)
    declare_conditions = db.Column(db.String(500))
    declare_data = db.Column(db.String(1000))
    other_remark = db.Column(db.String(500))
    aidance_type = db.Column(db.SmallInteger)
    remark = db.Column(db.String(200))
    pdf_path = db.Column(db.String(255))
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)

    def __init__(self, task_id, service_id, customer_name, service_agency, service_person, service_content,
                 declare_direction, manage_dept, apply_amount, subsidy_method, service_deadline, declare_conditions,
                 declare_data, other_remark, aidance_type, remark, pdf_path, create_person, create_time, execute_person,
                 execute_time, is_done):
        '''Constructor'''
        self.task_id = task_id
        self.service_id = service_id
        self.customer_name = customer_name
        self.service_agency = service_agency
        self.service_person = service_person
        self.service_content = service_content
        self.declare_direction = declare_direction
        self.manage_dept = manage_dept
        self.apply_amount = apply_amount
        self.subsidy_method = subsidy_method
        self.service_deadline = service_deadline
        self.declare_conditions = declare_conditions
        self.declare_data = declare_data
        self.other_remark = other_remark
        self.aidance_type = aidance_type
        self.remark = remark
        self.pdf_path = pdf_path
        self.create_person = create_person
        self.create_time = create_time
        self.execute_person = execute_person
        self.execute_time = execute_time
        self.is_done = is_done

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'taskId', 'serviceId', 'customerName', 'serviceAgency', 'servicePerson', 'serviceContent',
              'declareDirection', 'manageDept', 'applyAmount', 'subsidyMethod', 'serviceDeadline', 'declareConditions',
              'declareData', 'otherRemark', 'aidanceType', 'remark', 'pdfPath', 'createPerson', 'createTime',
              'executePerson', 'executeTime', 'isDone']
SingleServiceChangeDic = {
    "id": "id",
    "taskId": "task_id",
    "serviceId": "service_id",
    "customerName": "customer_name",
    "serviceAgency": "service_agency",
    "servicePerson": "service_person",
    "serviceContent": "service_content",
    "declareDirection": "declare_direction",
    "manageDept": "manage_dept",
    "applyAmount": "apply_amount",
    "subsidyMethod": "subsidy_method",
    "serviceDeadline": "service_deadline",
    "declareConditions": "declare_conditions",
    "declareData": "declare_data",
    "otherRemark": "other_remark",
    "aidanceType": "aidance_type",
    "remark": "remark",
    "pdfPath": "pdf_path",
    "createPerson": "create_person",
    "createTime": "create_time",
    "executePerson": "execute_person",
    "executeTime": "execute_time",
    "isDone": "is_done"
}

intList = ['id', 'taskId', 'serviceId', 'aidanceType', 'isDone']

# db.create_all()
