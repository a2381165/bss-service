# -*- coding: utf-8 -*-
from config import db


class TempItem(db.Model):
    __tablename__ = "data_temp_item"

    item_id = db.Column(db.Integer, primary_key=True, nullable=False)
    dept_id = db.Column(db.Integer)
    item_url = db.Column(db.String(255))
    item_title = db.Column(db.String(100))
    item_imgurl = db.Column(db.String(255))
    item_pulishdate = db.Column(db.String(20))
    item_album = db.Column(db.Text)
    item_content = db.Column(db.Text)
    item_industry_ids = db.Column(db.String(200))
    item_label_ids = db.Column(db.String(200))
    check_person = db.Column(db.String(100))
    check_status = db.Column(db.SmallInteger)
    check_remark = db.Column(db.String(200))
    check_time = db.Column(db.DateTime)
    create_person = db.Column(db.String(100))
    create_time = db.Column(db.DateTime)
    item_type = db.Column(db.SmallInteger)
    item_content_attach = db.Column(db.Text)
    temp_item_status = db.Column(db.SmallInteger)
    is_content_json = db.Column(db.SmallInteger)
    is_close = db.Column(db.SmallInteger)
    item_deadline = db.Column(db.DateTime)
    is_secular = db.Column(db.SmallInteger)
    media_type = db.Column(db.SmallInteger)
    media_url = db.Column(db.String(255))

    def __init__(self, dept_id, item_url, item_title, item_imgurl, item_pulishdate, item_album, item_content,
                 item_industry_ids, item_label_ids, check_person, check_status, check_remark, check_time, create_person,
                 create_time, item_type, item_content_attach, temp_item_status, is_content_json, is_close,
                 item_deadline, is_secular, media_type,media_url ):
        '''Constructor'''
        self.dept_id = dept_id
        self.item_url = item_url
        self.item_title = item_title
        self.item_imgurl = item_imgurl
        self.item_pulishdate = item_pulishdate
        self.item_album = item_album
        self.item_content = item_content
        self.item_industry_ids = item_industry_ids
        self.item_label_ids = item_label_ids
        self.check_person = check_person
        self.check_status = check_status
        self.check_remark = check_remark
        self.check_time = check_time
        self.create_person = create_person
        self.create_time = create_time
        self.item_type = item_type
        self.item_content_attach = item_content_attach
        self.temp_item_status = temp_item_status
        self.is_content_json = is_content_json
        self.is_close = is_close
        self.item_deadline = item_deadline
        self.is_secular = is_secular
        self.media_type = media_type
        self.media_url  = media_url

    def __repr__(self):
        return 'item_id : %s' % self.item_id

    def updateTable(self, dataDict):
        # if dataDict.get("itemId", None) != None:
        #     self.item_id = dataDict.get("itemId")
        if dataDict.get("deptId", None) != None:
            self.dept_id = dataDict.get("deptId")
        if dataDict.get("itemUrl", None) != None:
            self.item_url = dataDict.get("itemUrl")
        if dataDict.get("itemTitle", None) != None:
            self.item_title = dataDict.get("itemTitle")
        if dataDict.get("itemImgurl", None) != None:
            self.item_imgurl = dataDict.get("itemImgurl")
        if dataDict.get("itemPulishdate", None) != None:
            self.item_pulishdate = dataDict.get("itemPulishdate")
        if dataDict.get("itemAlbum", None) != None:
            self.item_album = dataDict.get("itemAlbum")
        if dataDict.get("itemContent", None) != None:
            self.item_content = dataDict.get("itemContent")
        if dataDict.get("itemIndustryIds", None) != None:
            self.item_industry_ids = dataDict.get("itemIndustryIds")
        if dataDict.get("itemLabelIds", None) != None:
            self.item_label_ids = dataDict.get("itemLabelIds")
        if dataDict.get("checkPerson", None) != None:
            self.check_person = dataDict.get("checkPerson")
        if dataDict.get("checkStatus", None) != None:
            self.check_status = dataDict.get("checkStatus")
        if dataDict.get("checkRemark", None) != None:
            self.check_remark = dataDict.get("checkRemark")
        if dataDict.get("checkTime", None) != None:
            self.check_time = dataDict.get("checkTime")
        if dataDict.get("createPerson", None) != None:
            self.create_person = dataDict.get("createPerson")
        if dataDict.get("createTime", None) != None:
            self.create_time = dataDict.get("createTime")
        if dataDict.get("itemType", None) != None:
            self.item_type = dataDict.get("itemType")
        if dataDict.get("itemContentAttach", None) != None:
            self.item_content_attach = dataDict.get("itemContentAttach")
        if dataDict.get("tempItemStatus", None) != None:
            self.temp_item_status = dataDict.get("tempItemStatus")
        if dataDict.get("isContentJson", None) != None:
            self.is_content_json = dataDict.get("isContentJson")
        if dataDict.get("isClose", None) != None:
            self.is_close = dataDict.get("isClose")
        if dataDict.get("itemDeadline", None) != None:
            self.item_deadline = dataDict.get("itemDeadline")
        if dataDict.get("isSecular", None) != None:
            self.is_secular = dataDict.get("isSecular")
        if dataDict.get("mediaType", None) != None:
            self.is_secular = dataDict.get("mediaType")
        if dataDict.get("mediaUrl", None) != None:
            self.is_secular = dataDict.get("mediaUrl")


# Client and database attributes dictionary
clinetHead = {u'itemId', u'deptId', u'itemUrl', u'itemTitle', u'itemImgurl', u'itemPulishdate', u'itemAlbum',
              u'itemContent', u'itemIndustryIds', u'itemLabelIds', u'checkPerson', u'checkStatus', u'checkRemark',
              u'checkTime', u'createPerson', u'createTime', u'itemType', u'itemContentAttach', u'tempItemStatus',
              u'isContentJson', u'isClose', u'itemDeadline', u'isSecular', "mediaType","mediaUrl"}
TempItemChangeDic = {
    "itemId": "item_id",
    "deptId": "dept_id",
    "itemUrl": "item_url",
    "itemTitle": "item_title",
    "itemImgurl": "item_imgurl",
    "itemPulishdate": "item_pulishdate",
    "itemAlbum": "item_album",
    "itemContent": "item_content",
    "itemIndustryIds": "item_industry_ids",
    "itemLabelIds": "item_label_ids",
    "checkPerson": "check_person",
    "checkStatus": "check_status",
    "checkRemark": "check_remark",
    "checkTime": "check_time",
    "createPerson": "create_person",
    "createTime": "create_time",
    "itemType": "item_type",
    "itemContentAttach": "item_content_attach",
    "tempItemStatus": "temp_item_status",
    "isContentJson": "is_content_json",
    "isClose": "is_close",
    "itemDeadline": "item_deadline",
    "isSecular": "is_secular",
    "mediaType": "media_type",
    "mediaUrl": "media_url",
}

intList = {u'itemId', u'deptId', u'checkStatus', u'itemType', u'tempItemStatus', u'isContentJson', u'isClose',
           u'isSecular', "mediaType"}

# db.create_all()
