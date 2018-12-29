
# -*- coding: utf-8 -*-
from config import db


class SpiderSchedule(db.Model):
    __tablename__ = "spider_schedule"

    schedule_id = db.Column(db.Integer, primary_key=True, nullable=False)
    schedule_name = db.Column(db.String(20))
    schedule_desc = db.Column(db.String(30))
    cron_minutes = db.Column(db.String(20))
    cron_hour = db.Column(db.String(20))
    cron_day_of_month = db.Column(db.String(20))
    cron_day_of_week = db.Column(db.String(20))
    cron_month = db.Column(db.String(20))
    create_time = db.Column(db.DateTime)
    is_lock = db.Column(db.SmallInteger)

    def __init__(self, schedule_name,schedule_desc,cron_minutes,cron_hour,cron_day_of_month,cron_day_of_week,cron_month,create_time,is_lock):
        '''Constructor'''
        self.schedule_name=schedule_name
        self.schedule_desc=schedule_desc
        self.cron_minutes=cron_minutes
        self.cron_hour=cron_hour
        self.cron_day_of_month=cron_day_of_month
        self.cron_day_of_week=cron_day_of_week
        self.cron_month=cron_month
        self.create_time=create_time
        self.is_lock = is_lock


    def __repr__(self):
        return 'schedule_id : %s' % self.schedule_id


# Client and database attributes dictionary
clinetHead = {u'scheduleId', u'scheduleName', u'scheduleDesc', u'cronMinutes', u'cronHour', u'cronDayOfMonth', u'cronDayOfWeek', u'cronMonth', u'createTime',u'is_lock'}
tableChangeDic = {
    "scheduleId":"schedule_id",
    "scheduleName":"schedule_name",
    "scheduleDesc":"schedule_desc",
    "cronMinutes":"cron_minutes",
    "cronHour":"cron_hour",
    "cronDayOfMonth":"cron_day_of_month",
    "cronDayOfWeek":"cron_day_of_week",
    "cronMonth":"cron_month",
    "createTime":"create_time",
    "isLock":"is_lock"
}

intList = {u'scheduleId',u'is_lock'}

# db.create_all()
