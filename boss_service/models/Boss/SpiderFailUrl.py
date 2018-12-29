
# -*- coding: utf-8 -*-
from config import db


class SpiderFailUrl(db.Model):
    __tablename__ = "spider_fail_url"

    fail_id = db.Column(db.Integer, primary_key=True, nullable=False)
    queue_url = db.Column(db.String(255))
    spider_url = db.Column(db.String(255))
    status_code = db.Column(db.String(11))
    dept_name_key = db.Column(db.String(50))
    dept_id = db.Column(db.Integer)
    save_time = db.Column(db.DateTime)

    def __init__(self, queue_url,spider_url,status_code,dept_name_key,dept_id,save_time):
        '''Constructor'''
        self.queue_url=queue_url
        self.spider_url=spider_url
        self.status_code=status_code
        self.dept_name_key=dept_name_key
        self.dept_id=dept_id
        self.save_time=save_time


    def __repr__(self):
        return 'fail_id : %s' % self.fail_id


# Client and database attributes dictionary
clinetHead = {u'failId', u'queueUrl', u'spiderUrl', u'statusCode', u'deptNameKey', u'deptId', u'saveTime'}
tableChangeDic = {
    "failId":"fail_id",
    "queueUrl":"queue_url",
    "spiderUrl":"spider_url",
    "statusCode":"status_code",
    "deptNameKey":"dept_name_key",
    "deptId":"dept_id",
    "saveTime":"save_time"
}

intList = {u'failId', u'deptId'}

# db.create_all()
