# -*- coding: utf-8 -*-
from config import db


class ChannelMember(db.Model):
    __tablename__ = "channel_member"

    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    member_name = db.Column(db.String(20))
    member_type = db.Column(db.Integer)
    invited_code = db.Column(db.String(30))
    member_rank = db.Column(db.Integer)
    member_points = db.Column(db.Integer)
    member_balance = db.Column(db.Numeric(11, 2))
    member_contact_email = db.Column(db.String(60))
    member_contact_person = db.Column(db.String(10))
    member_contact_phone = db.Column(db.String(11))
    member_contact_address = db.Column(db.String(255))
    maid_rate = db.Column(db.Integer)
    area_code = db.Column(db.String(6))
    member_credit_code = db.Column(db.String(32))
    app_key = db.Column(db.String(255))
    app_secret = db.Column(db.String(255))
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_wx = db.Column(db.SmallInteger)
    is_qq = db.Column(db.SmallInteger)
    remark = db.Column(db.String(255))

    def __init__(self, user_id, member_name, member_type, invited_code, member_rank, member_points, member_balance,
                 member_contact_email, member_contact_person, member_contact_phone, member_contact_address, maid_rate,
                 area_code, member_credit_code, app_key, app_secret, start_date, end_date, is_wx, is_qq, remark):
        '''Constructor'''
        self.user_id = user_id
        self.member_name = member_name
        self.member_type = member_type
        self.invited_code = invited_code
        self.member_rank = member_rank
        self.member_points = member_points
        self.member_balance = member_balance
        self.member_contact_email = member_contact_email
        self.member_contact_person = member_contact_person
        self.member_contact_phone = member_contact_phone
        self.member_contact_address = member_contact_address
        self.maid_rate = maid_rate
        self.area_code = area_code
        self.member_credit_code = member_credit_code
        self.app_key = app_key
        self.app_secret = app_secret
        self.start_date = start_date
        self.end_date = end_date
        self.is_wx = is_wx
        self.is_qq = is_qq
        self.remark = remark

    def __repr__(self):
        return 'user_id : %s' % self.user_id


# Client and database attributes dictionary
clinetHead = ['userId', 'memberName', 'memberType', 'invitedCode', 'memberRank', 'memberPoints', 'memberBalance',
              'memberContactEmail', 'memberContactPerson', 'memberContactPhone', 'memberContactAddress', 'maidRate',
              'areaCode', 'memberCreditCode', 'appKey', 'appSecret', 'startDate', 'endDate', 'isWx', 'isQq', 'remark']
ChannelMemberChangeDic = {
    "userId": "user_id",
    "memberName": "member_name",
    "memberType": "member_type",
    "invitedCode": "invited_code",
    "memberRank": "member_rank",
    "memberPoints": "member_points",
    "memberBalance": "member_balance",
    "memberContactEmail": "member_contact_email",
    "memberContactPerson": "member_contact_person",
    "memberContactPhone": "member_contact_phone",
    "memberContactAddress": "member_contact_address",
    "maidRate": "maid_rate",
    "areaCode": "area_code",
    "memberCreditCode": "member_credit_code",
    "appKey": "app_key",
    "appSecret": "app_secret",
    "startDate": "start_date",
    "endDate": "end_date",
    "isWx": "is_wx",
    "isQq": "is_qq",
    "remark": "remark"
}

intList = ['userId', 'memberType', 'memberRank', 'memberPoints', 'maidRate', 'isWx', 'isQq']

# db.create_all()
