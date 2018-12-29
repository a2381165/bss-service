# -*- coding: utf-8 -*-
from config import db


class SpiderScript(db.Model):
    __tablename__ = "spider_script"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    dept_name_key = db.Column(db.String(50))
    dept_id = db.Column(db.Integer)
    url = db.Column(db.String(1024))
    script_text = db.Column(db.Text)
    priority = db.Column(db.SmallInteger)
    next_filter = db.Column(db.SmallInteger)
    is_lock = db.Column(db.SmallInteger)
    remark = db.Column(db.String(50))
    project_name = db.Column(db.String(20))
    spider_name = db.Column(db.String(20))
    content_xpath = db.Column(db.String(255))
    script_type = db.Column(db.SmallInteger)

    def __init__(self, dept_name_key, dept_id, url, script_text, priority, next_filter, is_lock, remark, project_name,
                 spider_name, content_xpath, script_type):
        '''Constructor'''
        self.dept_name_key = dept_name_key
        self.dept_id = dept_id
        self.url = url
        self.script_text = script_text
        self.priority = priority
        self.next_filter = next_filter
        self.is_lock = is_lock
        self.remark = remark
        self.project_name = project_name
        self.spider_name = spider_name
        self.content_xpath = content_xpath
        self.script_type = script_type

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'deptNameKey', u'deptId', u'url', u'scriptText', u'priority', u'nextFilter', u'isLock', u'remark',
              u'projectName', u'spiderName', u'contentXpath'}
tableChangeDic = {
    "id": "id",
    "deptNameKey": "dept_name_key",
    "deptId": "dept_id",
    "url": "url",
    "scriptText": "script_text",
    "priority": "priority",
    "nextFilter": "next_filter",
    "isLock": "is_lock",
    "remark": "remark",
    "projectName": "project_name",
    "spiderName": "spider_name",
    "contentXpath": "content_xpath",
    "scriptType": "script_type",
}

intList = {u'id', u'deptId', u'priority', u'nextFilter', u'isLock', 'scriptType'}

# db.create_all()
