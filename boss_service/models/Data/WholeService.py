# -*- coding: utf-8 -*-
from config import db


class WholeService(db.Model):
    __tablename__ = "data_whole_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    service_id = db.Column(db.Integer)
    customer_name = db.Column(db.String(20))
    service_start_time = db.Column(db.DateTime)
    service_agency = db.Column(db.String(50))
    service_person = db.Column(db.String(100))
    policy_financing_adviser = db.Column(db.String(100))
    company_profile = db.Column(db.Text)
    declare_project = db.Column(db.Text)
    policy_service = db.Column(db.Text)
    zzh_service = db.Column(db.Text)
    qualification_back = db.Column(db.Text)
    declare_recommend = db.Column(db.Text)
    declare_proposal = db.Column(db.Text)
    aidance_type = db.Column(db.SmallInteger)
    remark = db.Column(db.String(200))
    pdf_path = db.Column(db.String(255))
    create_person = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)

    def __init__(self, task_id, service_id, customer_name, service_start_time, service_agency, service_person,
                 policy_financing_adviser, company_profile, declare_project, policy_service, zzh_service,
                 qualification_back, declare_recommend, declare_proposal, aidance_type, remark, pdf_path, create_person,
                 create_time, execute_person, execute_time, is_done):
        '''Constructor'''
        self.task_id = task_id
        self.service_id = service_id
        self.customer_name = customer_name
        self.service_start_time = service_start_time
        self.service_agency = service_agency
        self.service_person = service_person
        self.policy_financing_adviser = policy_financing_adviser
        self.company_profile = company_profile
        self.declare_project = declare_project
        self.policy_service = policy_service
        self.zzh_service = zzh_service
        self.qualification_back = qualification_back
        self.declare_recommend = declare_recommend
        self.declare_proposal = declare_proposal
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
clinetHead = ['id', 'taskId', 'serviceId', 'customerName', 'serviceStartTime', 'serviceAgency', 'servicePerson',
              'policyFinancingAdviser', 'companyProfile', 'declareProject', 'policyService', 'zzhService',
              'qualificationBack', 'declareRecommend', 'declareProposal', 'aidanceType', 'remark', 'pdfPath',
              'createPerson', 'createTime', 'executePerson', 'executeTime', 'isDone']
WholeServiceChangeDic = {
    "id": "id",
    "taskId": "task_id",
    "serviceId": "service_id",
    "customerName": "customer_name",
    "serviceStartTime": "service_start_time",
    "serviceAgency": "service_agency",
    "servicePerson": "service_person",
    "policyFinancingAdviser": "policy_financing_adviser",
    "companyProfile": "company_profile",
    "declareProject": "declare_project",
    "policyService": "policy_service",
    "zzhService": "zzh_service",
    "qualificationBack": "qualification_back",
    "declareRecommend": "declare_recommend",
    "declareProposal": "declare_proposal",
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
