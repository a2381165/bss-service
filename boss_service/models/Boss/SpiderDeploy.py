
# -*- coding: utf-8 -*-
from config import db


class SpiderDeploy(db.Model):
    __tablename__ = "spider_deploy"

    deploy_id = db.Column(db.Integer, primary_key=True, nullable=False)
    description = db.Column(db.String(30))
    deployed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, description,deployed_at,created_at,updated_at):
        '''Constructor'''
        self.description=description
        self.deployed_at=deployed_at
        self.created_at=created_at
        self.updated_at=updated_at


    def __repr__(self):
        return 'deploy_id : %s' % self.deploy_id


# Client and database attributes dictionary
clinetHead = {u'deployId', u'description', u'deployedAt', u'createdAt', u'updatedAt'}
tableChangeDic = {
    "deployId":"deploy_id",
    "description":"description",
    "deployedAt":"deployed_at",
    "createdAt":"created_at",
    "updatedAt":"updated_at"
}

intList = {u'deployId'}

# db.create_all()
