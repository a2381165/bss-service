
# -*- coding: utf-8 -*-
from config import db


class SpiderNode(db.Model):
    __tablename__ = "spider_node"

    node_id = db.Column(db.Integer, primary_key=True, nullable=False)
    node_name = db.Column(db.String(20))
    description = db.Column(db.String(30))
    node_ip = db.Column(db.String(39))
    node_port = db.Column(db.Integer)
    node_status = db.Column(db.SmallInteger)
    project_name = db.Column(db.String(39))
    deploy_status = db.Column(db.SmallInteger)

    def __init__(self, node_name,description,node_ip,node_port,node_status,project_name,deploy_status):
        '''Constructor'''
        # self.node_id=node_id
        self.node_name=node_name
        self.description=description
        self.node_ip=node_ip
        self.node_port=node_port
        self.node_status=node_status
        self.project_name=project_name
        self.deploy_status=deploy_status


    def __repr__(self):
        return 'node_id : %s' % self.node_id


# Client and database attributes dictionary
clinetHead = {u'nodeId', u'nodeMing', u'description', u'nodeIp', u'nodePort', u'nodeStatus', u'projectName', u'deployStatus'}
tableChangeDic = {
    "nodeId":"node_id",
    "nodeMing":"node_name",
    "description":"description",
    "nodeIp":"node_ip",
    "nodePort":"node_port",
    "nodeStatus":"node_status",
    "projectName":"project_name",
    "deployStatus":"deploy_status"
}

intList = {u'nodeId', u'nodePort', u'nodeStatus', u'redisPort'}

# db.create_all()
