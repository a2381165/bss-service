# -*- coding: utf-8 -*-
from config import db


class UserOrderComment(db.Model):
    __tablename__ = "zzh_user_order_comment"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    comment_type = db.Column(db.SmallInteger)
    from_id = db.Column(db.Integer)
    from_name = db.Column(db.String(255))
    comment_starts = db.Column(db.SmallInteger)
    comment_content = db.Column(db.String(255))
    sevice_type = db.Column(db.SmallInteger)
    comment_time = db.Column(db.DateTime)
    is_anonymous = db.Column(db.SmallInteger)
    counselor_id = db.Column(db.Integer)

    def __init__(self, order_no, comment_type, from_id, from_name, comment_starts, comment_content, sevice_type,
                 comment_time, is_anonymous, counselor_id):
        '''Constructor'''
        self.order_no = order_no
        self.comment_type = comment_type
        self.from_id = from_id
        self.from_name = from_name
        self.comment_starts = comment_starts
        self.comment_content = comment_content
        self.sevice_type = sevice_type
        self.comment_time = comment_time
        self.is_anonymous = is_anonymous
        self.counselor_id = counselor_id

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'commentType', u'fromId', u'fromName', u'commentStarts', u'commentContent',
              u'seviceType', u'commentTime', u'isAnonymous', u'counselorId'}
UserOrderCommentChangeDic = {
    "id": "id",
    "orderNo": "order_no",
    "commentType": "comment_type",
    "fromId": "from_id",
    "fromName": "from_name",
    "commentStarts": "comment_starts",
    "commentContent": "comment_content",
    "seviceType": "sevice_type",
    "commentTime": "comment_time",
    "isAnonymous": "is_anonymous",
    "counselorId": "counselor_id"
}

intList = {u'id', u'commentType', u'fromId', u'commentStarts', u'seviceType', u'isAnonymous', u'counselorId'}

# db.create_all()
