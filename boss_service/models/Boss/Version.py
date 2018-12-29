
# -*- coding: utf-8 -*-
from config import db


class Version(db.Model):
    __tablename__ = "boss_version"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    app_id = db.Column(db.String(30))
    app_type = db.Column(db.SmallInteger)
    update_type = db.Column(db.SmallInteger)
    version = db.Column(db.String(15))
    url_one = db.Column(db.String(255))
    url_two = db.Column(db.String(255))
    url_three = db.Column(db.String(255))
    is_lock = db.Column(db.SmallInteger)
    create_time = db.Column(db.DateTime)
    create_person = db.Column(db.String(50))
    verison_remark = db.Column(db.String(255))

    def __init__(self,app_id,app_type,update_type,version,url_one,url_two,url_three,is_lock,create_time,create_person,verison_remark):
        '''Constructor'''
        self.app_id=app_id
        self.app_type=app_type
        self.update_type=update_type
        self.version=version
        self.url_one=url_one
        self.url_two=url_two
        self.url_three=url_three
        self.is_lock=is_lock
        self.create_time=create_time
        self.create_person=create_person
        self.verison_remark=verison_remark


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'appId', u'appType', u'updateType', u'version', u'urlOne', u'urlTwo', u'urlThree', u'isLock', u'createTime', u'createPerson', u'verisonRemark'}
tableChangeDic = {
    "id":"id",
    "appId":"app_id",
    "appType":"app_type",
    "updateType":"update_type",
    "version":"version",
    "urlOne":"url_one",
    "urlTwo":"url_two",
    "urlThree":"url_three",
    "isLock":"is_lock",
    "createTime":"create_time",
    "createPerson":"create_person",
    "verisonRemark":"verison_remark"
}

intList = {u'id', u'appType', u'updateType', u'isLock'}

# db.create_all()
