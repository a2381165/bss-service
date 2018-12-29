
# -*- coding: utf-8 -*-
from config import db


class ItemContent(db.Model):
    __tablename__ = "data_item_content"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    item_id = db.Column(db.Integer)
    is_chapter_title = db.Column(db.SmallInteger)
    chapter_title = db.Column(db.String(200))
    chapter_content = db.Column(db.Text)
    chapter_index = db.Column(db.SmallInteger)
    album_cover = db.Column(db.String(255))

    def __init__(self,item_id,is_chapter_title,chapter_title,chapter_content,chapter_index,album_cover):
        '''Constructor'''
        self.item_id=item_id
        self.is_chapter_title=is_chapter_title
        self.chapter_title=chapter_title
        self.chapter_content=chapter_content
        self.chapter_index=chapter_index
        self.album_cover=album_cover


    def __repr__(self):
        return 'id : %s' % self.id

    def updateTable(self,dataDict):
        if dataDict.get("id", None) != None:
            self.id = dataDict.get("id")
        if dataDict.get("itemId", None) != None:
            self.item_id = dataDict.get("itemId")
        if dataDict.get("isChapterTitle", None) != None:
            self.is_chapter_title = dataDict.get("isChapterTitle")
        if dataDict.get("chapterTitle", None) != None:
            self.chapter_title = dataDict.get("chapterTitle")
        if dataDict.get("chapterContent", None) != None:
            self.chapter_content = dataDict.get("chapterContent")
        if dataDict.get("chapterIndex", None) != None:
            self.chapter_index = dataDict.get("chapterIndex")
        if dataDict.get("albumCover", None) != None:
            self.album_cover = dataDict.get("albumCover")

# Client and database attributes dictionary
clinetHead = {u'id', u'itemId', u'isChapterTitle', u'chapterTitle', u'chapterContent', u'chapterIndex', u'albumCover'}
tableChangeDic = {
    "id":"id",
    "itemId":"item_id",
    "isChapterTitle":"is_chapter_title",
    "chapterTitle":"chapter_title",
    "chapterContent":"chapter_content",
    "chapterIndex":"chapter_index",
    "albumCover":"album_cover"
}

intList = {u'id', u'itemId', u'isChapterTitle', u'chapterIndex'}

# db.create_all()
