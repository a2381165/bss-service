
# -*- coding: utf-8 -*-
from config import db


class SpiderProject(db.Model):
    __tablename__ = "spider_project"

    project_id = db.Column(db.Integer, primary_key=True, nullable=False)
    project_desc = db.Column(db.String(20))
    project_name = db.Column(db.String(20))
    spider_egg = db.Column(db.String(50))
    configurable = db.Column(db.Integer)
    built_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, project_desc,project_name,spider_egg,configurable,built_at,created_at,updated_at):
        '''Constructor'''
        self.project_desc=project_desc
        self.project_name=project_name
        self.spider_egg=spider_egg
        self.configurable=configurable
        self.built_at=built_at
        self.created_at=created_at
        self.updated_at=updated_at


    def __repr__(self):
        return 'project_id : %s' % self.project_id


# Client and database attributes dictionary
clinetHead = {u'projectId', u'projectDesc', u'projectName', u'spiderEgg', u'configurable', u'builtAt', u'createdAt', u'updatedAt'}
tableChangeDic = {
    "projectId":"project_id",
    "projectDesc":"project_desc",
    "projectName":"project_name",
    "spiderEgg":"spider_egg",
    "configurable":"configurable",
    "builtAt":"built_at",
    "createdAt":"created_at",
    "updatedAt":"updated_at"
}

intList = {u'projectId', u'configurable'}

# db.create_all()
