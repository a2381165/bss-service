
# -*- coding: utf-8 -*-
from config import db


class ItemContentAttach(db.Model):
    __tablename__ = "data_item_content_attach"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer)
    attach_extension_name = db.Column(db.String(50))
    attach_size = db.Column(db.String(None))
    attach_title = db.Column(db.String(255))
    attach_path = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)

    def __init__(self,item_id,attach_extension_name,attach_size,attach_title,attach_path,create_time):
        '''Constructor'''
        self.item_id=item_id
        self.attach_extension_name=attach_extension_name
        self.attach_size=attach_size
        self.attach_title=attach_title
        self.attach_path=attach_path
        self.create_time=create_time


    def __repr__(self):
        return 'id : %s' % self.id

    def updateTable(self,dataDict):
        # if dataDict.get("id", None) != None:
        #     self.id = dataDict.get("id")
        if dataDict.get("itemId", None) != None:
            self.item_id = dataDict.get("itemId")
        if dataDict.get("attachExtensionName", None) != None:
            self.attach_extension_name = dataDict.get("attachExtensionName")
        if dataDict.get("attachSize", None) != None:
            self.attach_size = dataDict.get("attachSize")
        if dataDict.get("attachTitle", None) != None:
            self.attach_title = dataDict.get("attachTitle")
        if dataDict.get("attachPath", None) != None:
            self.attach_path = dataDict.get("attachPath")
        if dataDict.get("createTime", None) != None:
            self.create_time = dataDict.get("createTime")
# Client and database attributes dictionary
clinetHead = {u'id', u'itemId', u'attachExtensionName', u'attachSize', u'attachTitle', u'attachPath', u'createTime'}
tableChangeDic = {
    "id":"id",
    "itemId":"item_id",
    "attachExtensionName":"attach_extension_name",
    "attachSize":"attach_size",
    "attachTitle":"attach_title",
    "attachPath":"attach_path",
    "createTime":"create_time"
}

intList = {u'id', u'itemId'}

# db.create_all()
