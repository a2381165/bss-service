# -*- coding: utf-8 -*-
from config import db


class Item(db.Model):
    __tablename__ = "data_item"

    item_id = db.Column(db.Integer, primary_key=True, nullable=False)
    dept_name = db.Column(db.String(100))
    level_code = db.Column(db.SmallInteger)
    category_name = db.Column(db.String(20))
    area_code = db.Column(db.String(6))
    item_url = db.Column(db.String(255))
    item_title = db.Column(db.String(100))
    item_imgurl = db.Column(db.String(255))
    item_pulishdate = db.Column(db.String(20))
    item_type = db.Column(db.SmallInteger)
    item_sort = db.Column(db.Integer)
    is_top = db.Column(db.SmallInteger)
    is_lock = db.Column(db.SmallInteger)
    is_service = db.Column(db.SmallInteger)
    is_content_json = db.Column(db.SmallInteger)
    create_time = db.Column(db.DateTime)
    is_close = db.Column(db.SmallInteger)
    item_deadline = db.Column(db.DateTime)
    is_secular = db.Column(db.SmallInteger)
    media_type = db.Column(db.SmallInteger)
    media_url = db.Column(db.String(255))

    def __init__(self, dept_name, level_code, category_name, area_code, item_url, item_title, item_imgurl,
                 item_pulishdate, item_type, item_sort, is_top, is_lock, is_service, is_content_json, create_time,
                 is_close, item_deadline, is_secular, media_type, media_url):
        '''Constructor'''
        self.dept_name = dept_name
        self.level_code = level_code
        self.category_name = category_name
        self.area_code = area_code
        self.item_url = item_url
        self.item_title = item_title
        self.item_imgurl = item_imgurl
        self.item_pulishdate = item_pulishdate
        self.item_type = item_type
        self.item_sort = item_sort
        self.is_top = is_top
        self.is_lock = is_lock
        self.is_service = is_service
        self.is_content_json = is_content_json
        self.create_time = create_time
        self.is_close = is_close
        self.item_deadline = item_deadline
        self.is_secular = is_secular
        self.media_type = media_type
        self.media_url = media_url

    def __repr__(self):
        return 'item_id : %s' % self.item_id

    def updateTable(self, dataDict):
        # if dataDict.get("itemId", None) != None:
        #     self.item_id = dataDict.get("itemId")
        if dataDict.get("deptName", None) != None:
            self.dept_name = dataDict.get("deptName")
        if dataDict.get("levelCode", None) != None:
            self.level_code = dataDict.get("levelCode")
        if dataDict.get("categoryName", None) != None:
            self.category_name = dataDict.get("categoryName")
        if dataDict.get("areaCode", None) != None:
            self.area_code = dataDict.get("areaCode")
        if dataDict.get("itemUrl", None) != None:
            self.item_url = dataDict.get("itemUrl")
        if dataDict.get("itemTitle", None) != None:
            self.item_title = dataDict.get("itemTitle")
        if dataDict.get("itemImgurl", None) != None:
            self.item_imgurl = dataDict.get("itemImgurl")
        if dataDict.get("itemPulishdate", None) != None:
            self.item_pulishdate = dataDict.get("itemPulishdate")
        if dataDict.get("itemType", None) != None:
            self.item_type = dataDict.get("itemType")
        if dataDict.get("itemSort", None) != None:
            self.item_sort = dataDict.get("itemSort")
        if dataDict.get("isTop", None) != None:
            self.is_top = dataDict.get("isTop")
        if dataDict.get("isLock", None) != None:
            self.is_lock = dataDict.get("isLock")
        if dataDict.get("isService", None) != None:
            self.is_service = dataDict.get("isService")
        if dataDict.get("isContentJson", None) != None:
            self.is_content_json = dataDict.get("isContentJson")
        if dataDict.get("createTime", None) != None:
            self.create_time = dataDict.get("createTime")
        if dataDict.get("isClose", None) != None:
            self.is_close = dataDict.get("isClose")
        if dataDict.get("itemDeadline", None) != None:
            self.item_deadline = dataDict.get("itemDeadline")
        if dataDict.get("isSecular", None) != None:
            self.is_secular = dataDict.get("isSecular")
        if dataDict.get("mediaType", None) != None:
            self.media_type = dataDict.get("mediaType")
        if dataDict.get("mediaUrl", None) != None:
            self.media_type = dataDict.get("mediaUrl")


# Client and database attributes dictionary
clinetHead = {u'itemId', u'deptName', u'levelCode', u'categoryName', u'areaCode', u'itemUrl', u'itemTitle',
              u'itemImgurl', u'itemPulishdate', u'itemType', u'itemSort', u'isTop', u'isLock', u'isService',
              u'isContentJson', u'createTime', u'isClose', u'itemDeadline', u'isSecular', "mediaType", "mediaUrl"}
ItemChangeDic = {
    "itemId": "item_id",
    "deptName": "dept_name",
    "levelCode": "level_code",
    "categoryName": "category_name",
    "areaCode": "area_code",
    "itemUrl": "item_url",
    "itemTitle": "item_title",
    "itemImgurl": "item_imgurl",
    "itemPulishdate": "item_pulishdate",
    "itemType": "item_type",
    "itemSort": "item_sort",
    "isTop": "is_top",
    "isLock": "is_lock",
    "isService": "is_service",
    "isContentJson": "is_content_json",
    "createTime": "create_time",
    "isClose": "is_close",
    "itemDeadline": "item_deadline",
    "isSecular": "is_secular",
    "mediaType": "media_type",
    "mediaUrl": "mediaUrl",
}

intList = {u'itemId', u'levelCode', u'itemType', u'itemSort', u'isTop', u'isLock', u'isService', u'isContentJson',
           u'isClose', u'isSecular', "mediaType"}

# db.create_all()
