# -*- coding: utf-8 -*-
from config import db


class ChannelUserTask(db.Model):
    __tablename__ = "channel_user_task"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.Integer)
    contract_no = db.Column(db.String(64))
    user_name = db.Column(db.String(50))
    member_contact_phone = db.Column(db.String(11))
    member_type = db.Column(db.String(255))
    reg_type = db.Column(db.SmallInteger)
    member_name = db.Column(db.String(20))
    member_contact_person = db.Column(db.String(10))
    member_contact_address = db.Column(db.String(255))
    member_contact_email = db.Column(db.String(60))
    app_key = db.Column(db.String(255))
    app_secret = db.Column(db.String(255))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    socpe_area = db.Column(db.String(255))
    socpe_category = db.Column(db.String(255))
    scope_industry = db.Column(db.String(255))
    scope_keyword = db.Column(db.String(255))
    create_person = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    execute_person = db.Column(db.String(20))
    execute_time = db.Column(db.DateTime)
    is_done = db.Column(db.SmallInteger)

    def __init__(self, task_id, contract_no, user_name, member_contact_phone, member_type, reg_type, member_name,
                 member_contact_person, member_contact_address, member_contact_email, app_key, app_secret, start_date,
                 end_date, socpe_area, socpe_category, scope_industry, scope_keyword, create_person, create_time,
                 execute_person, execute_time, is_done):
        '''Constructor'''
        self.task_id = task_id
        self.contract_no = contract_no
        self.user_name = user_name
        self.member_contact_phone = member_contact_phone
        self.member_type = member_type
        self.reg_type = reg_type
        self.member_name = member_name
        self.member_contact_person = member_contact_person
        self.member_contact_address = member_contact_address
        self.member_contact_email = member_contact_email
        self.app_key = app_key
        self.app_secret = app_secret
        self.start_date = start_date
        self.end_date = end_date
        self.socpe_area = socpe_area
        self.socpe_category = socpe_category
        self.scope_industry = scope_industry
        self.scope_keyword = scope_keyword
        self.create_person = create_person
        self.create_time = create_time
        self.execute_person = execute_person
        self.execute_time = execute_time
        self.is_done = is_done

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'taskId', 'contractNo', 'userName', 'memberContactPhone', 'memberType', 'regType', 'memberName',
              'memberContactPerson', 'memberContactAddress', 'memberContactEmail', 'appKey', 'appSecret', 'startDate',
              'endDate', 'socpeArea', 'socpeCategory', 'scopeIndustry', 'scopeKeyword', 'createPerson', 'createTime',
              'executePerson', 'executeTime', 'isDone']
UserTaskChangeDic = {
    "id": "id",
    "taskId": "task_id",
    "contractNo": "contract_no",
    "userName": "user_name",
    "memberContactPhone": "member_contact_phone",
    "memberType": "member_type",
    "regType": "reg_type",
    "memberName": "member_name",
    "memberContactPerson": "member_contact_person",
    "memberContactAddress": "member_contact_address",
    "memberContactEmail": "member_contact_email",
    "appKey": "app_key",
    "appSecret": "app_secret",
    "startDate": "start_date",
    "endDate": "end_date",
    "socpeArea": "socpe_area",
    "socpeCategory": "socpe_category",
    "scopeIndustry": "scope_industry",
    "scopeKeyword": "scope_keyword",
    "createPerson": "create_person",
    "createTime": "create_time",
    "executePerson": "execute_person",
    "executeTime": "execute_time",
    "isDone": "is_done"
}

intList = ['id', 'taskId', 'regType', 'isDone']

# db.create_all()
