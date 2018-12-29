# -*- coding: utf-8 -*-
from config import db


class UserPost(db.Model):
    __tablename__ = "boss_user_post"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, post_id, user_id):
        '''Constructor'''
        self.post_id = post_id
        self.user_id = user_id

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'postId', u'userId'}
tableChangeDic = {
    "id": "id",
    "postId": "post_id",
    "userId": "user_id"
}

intList = {u'id', u'postId', u'userId'}

# db.create_all()
