# -*- coding: utf-8 -*-
from config import db


class ChannelGrantArea(db.Model):
    __tablename__ = "channel_grant_area"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    channel_member_id = db.Column(db.Integer)
    area_code = db.Column(db.String(6))

    def __init__(self, channel_member_id, area_code):
        '''Constructor'''
        self.channel_member_id = channel_member_id
        self.area_code = area_code

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'channelMemberId', 'areaCode']
ChannelGrantAreaChangeDic = {
    "id": "id",
    "channelMemberId": "channel_member_id",
    "areaCode": "area_code"
}

intList = ['id', 'channelMemberId']

# db.create_all()
