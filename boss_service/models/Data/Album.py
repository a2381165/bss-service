
# -*- coding: utf-8 -*-
from config import db


class Album(db.Model):
    __tablename__ = "data_album"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer)
    album_index = db.Column(db.Integer)
    album_path = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)

    def __init__(self,item_id,album_index,album_path,create_time):
        '''Constructor'''
        self.item_id=item_id
        self.album_index=album_index
        self.album_path=album_path
        self.create_time=create_time


    def __repr__(self):
        return 'id : %s' % self.id

    def updateTable(self,dataDict):
        if dataDict.get("id", None) != None:
            self.id = dataDict.get("id")
        if dataDict.get("itemId", None) != None:
            self.item_id = dataDict.get("itemId")
        if dataDict.get("albumIndex", None) != None:
            self.album_index = dataDict.get("albumIndex")
        if dataDict.get("albumPath", None) != None:
            self.album_path = dataDict.get("albumPath")
        if dataDict.get("createTime", None) != None:
            self.create_time = dataDict.get("createTime")
# Client and database attributes dictionary
clinetHead = {u'id', u'itemId', u'albumIndex', u'albumPath', u'createTime'}
tableChangeDic = {
    "id":"id",
    "itemId":"item_id",
    "albumIndex":"album_index",
    "albumPath":"album_path",
    "createTime":"create_time"
}

intList = {u'id', u'itemId', u'albumIndex'}

# db.create_all()
