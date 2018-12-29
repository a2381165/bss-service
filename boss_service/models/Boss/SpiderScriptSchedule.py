
# -*- coding: utf-8 -*-
from config import db


class SpiderScriptSchedule(db.Model):
    __tablename__ = "spider_script_schedule"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    schedule_id = db.Column(db.Integer)
    script_id = db.Column(db.Integer)

    def __init__(self, schedule_id,script_id):
        '''Constructor'''
        self.schedule_id=schedule_id
        self.script_id=script_id


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'scheduleId', u'scriptId'}
tableChangeDic = {
    "id":"id",
    "scheduleId":"schedule_id",
    "scriptId":"script_id"
}

intList = {u'id', u'scheduleId', u'scriptId'}

# db.create_all()
