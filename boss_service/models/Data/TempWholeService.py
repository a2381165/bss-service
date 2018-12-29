# -*- coding: utf-8 -*-
from config import db


class TempWholeService(db.Model):
    __tablename__ = "data_temp_whole_service"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    service_id = db.Column(db.Integer)
    aidance_id = db.Column(db.Integer)
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
    create_time = db.Column(db.DateTime)

    def __init__(self, service_id, aidance_id, customer_name, service_start_time, service_agency, service_person,
                 policy_financing_adviser, company_profile, declare_project, policy_service, zzh_service,
                 qualification_back, declare_recommend, declare_proposal, create_time):
        '''Constructor'''
        self.service_id = service_id
        self.aidance_id = aidance_id
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
        self.create_time = create_time

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'serviceId', u'aidanceId', u'customerName', u'serviceStartTime', u'serviceAgency',
              u'servicePerson', u'policyFinancingAdviser', u'companyProfile', u'declareProject', u'policyService',
              u'zzhService', u'qualificationBack', u'declareRecommend', u'declareProposal', u'createTime'}
TempWholeServiceChangeDic = {
    "id": "id",
    "serviceId": "service_id",
    "aidanceId": "aidance_id",
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
    "createTime": "create_time"
}

intList = {u'id', u'serviceId', u'aidanceId'}

# db.create_all()
