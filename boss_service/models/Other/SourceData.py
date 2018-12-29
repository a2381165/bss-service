# -*- coding: utf-8 -*-
from config import db


class SourceData(db.Model):
    __tablename__ = "zzh_source_data"
    __bind_key__ = "crawler"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    task_id = db.Column(db.String(64))
    dept_name_key = db.Column(db.String(64))
    dept_id = db.Column(db.Integer)
    item_title = db.Column(db.String(100))
    item_content = db.Column(db.Text)
    item_pulishdate = db.Column(db.String(32))
    key_words = db.Column(db.String(200))
    item_url = db.Column(db.String(1024))
    url_status = db.Column(db.SmallInteger)
    create_time = db.Column(db.DateTime)
    input_time = db.Column(db.DateTime)
    item_type = db.Column(db.SmallInteger)
    is_content = db.Column(db.SmallInteger)

    def __init__(self, task_id, dept_name_key, dept_id, item_title, item_content, item_pulishdate, key_words,
                 item_url, url_status, create_time, input_time, item_type, is_content):
        '''Constructor'''
        self.task_id = task_id
        self.dept_name_key = dept_name_key
        self.dept_id = dept_id
        self.item_title = item_title
        self.item_content = item_content
        self.item_pulishdate = item_pulishdate
        self.key_words = key_words
        self.item_url = item_url
        self.url_status = url_status
        self.create_time = create_time
        self.input_time = input_time
        self.item_type = item_type
        self.is_content = is_content

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'taskId', u'deptNameKey', u'deptId', u'itemTitle', u'itemContent', u'itemPulishdate',
              u'keyWords', u'itemUrl', u'urlStatus', u'createTime', u'inputTime', u'itemType', u'isContent'}
tableChangeDic = {
    "id": "id",
    "taskId": "task_id",
    "deptNameKey": "dept_name_key",
    "deptId": "dept_id",
    "itemTitle": "item_title",
    "itemContent": "item_content",
    "itemPulishdate": "item_pulishdate",
    "keyWords": "key_words",
    "itemUrl": "item_url",
    "urlStatus": "url_status",
    "createTime": "create_time",
    "inputTime": "input_time",
    "itemType": "item_type",
    "isContent": "is_content"
}

intList = {u'id', u'deptId', u'urlStatus', u'itemType', u'isContent'}

# db.create_all()
