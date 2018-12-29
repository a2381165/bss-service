
# -*- coding: utf-8 -*-
from config import db


class SpiderScriptNode(db.Model):
    __tablename__ = "spider_script_node"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    node_id = db.Column(db.Integer)
    script_id = db.Column(db.Integer)

    def __init__(self,node_id,script_id):
        '''Constructor'''
        self.node_id=node_id
        self.script_id=script_id


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'nodeId', u'scriptId'}
tableChangeDic = {
    "id":"id",
    "nodeId":"node_id",
    "scriptId":"script_id"
}

intList = {u'id', u'nodeId', u'scriptId'}

# db.create_all()
