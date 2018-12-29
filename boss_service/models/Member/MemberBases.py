# -*- coding: utf-8 -*-
from config import db


class MemberBases(db.Model):
    __tablename__ = "zzh_member_bases"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer)
    is_check = db.Column(db.SmallInteger)
    member_name = db.Column(db.String(20))
    member_type = db.Column(db.SmallInteger)
    member_code = db.Column(db.String(30))
    invited_code = db.Column(db.String(30))
    member_favorite_count = db.Column(db.Integer)
    member_points = db.Column(db.Integer)
    member_balance = db.Column(db.Numeric(11, 2))
    is_vip = db.Column(db.SmallInteger)
    member_expired = db.Column(db.DateTime)
    member_contact_email = db.Column(db.String(60))
    member_contact_person = db.Column(db.String(10))
    member_contact_phone = db.Column(db.String(11))
    enterprise_id = db.Column(db.Integer)
    figure_id = db.Column(db.Integer)
    area_code = db.Column(db.String(6))
    member_credit_code = db.Column(db.String(32))

    def __init__(self, user_id, is_check, member_name, member_type, member_code, invited_code, member_favorite_count,
                 member_points, member_balance, is_vip, member_expired, member_contact_email, member_contact_person,
                 member_contact_phone, enterprise_id, figure_id, area_code, member_credit_code):
        '''Constructor'''
        self.user_id = user_id
        self.is_check = is_check
        self.member_name = member_name
        self.member_type = member_type
        self.member_code = member_code
        self.invited_code = invited_code
        self.member_favorite_count = member_favorite_count
        self.member_points = member_points
        self.member_balance = member_balance
        self.is_vip = is_vip
        self.member_expired = member_expired
        self.member_contact_email = member_contact_email
        self.member_contact_person = member_contact_person
        self.member_contact_phone = member_contact_phone
        self.enterprise_id = enterprise_id
        self.figure_id = figure_id
        self.area_code = area_code
        self.member_credit_code = member_credit_code

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = ['id', 'userId', 'isCheck', 'memberName', 'memberType', 'memberCode', 'invitedCode', 'memberFavoriteCount',
              'memberPoints', 'memberBalance', 'isVip', 'memberExpired', 'memberContactEmail', 'memberContactPerson',
              'memberContactPhone', 'enterpriseId', 'figureId', 'areaCode', 'memberCreditCode']
MemberBasesChangeDic = {
    "id": "id",
    "userId": "user_id",
    "isCheck": "is_check",
    "memberName": "member_name",
    "memberType": "member_type",
    "memberCode": "member_code",
    "invitedCode": "invited_code",
    "memberFavoriteCount": "member_favorite_count",
    "memberPoints": "member_points",
    "memberBalance": "member_balance",
    "isVip": "is_vip",
    "memberExpired": "member_expired",
    "memberContactEmail": "member_contact_email",
    "memberContactPerson": "member_contact_person",
    "memberContactPhone": "member_contact_phone",
    "enterpriseId": "enterprise_id",
    "figureId": "figure_id",
    "areaCode": "area_code",
    "memberCreditCode": "member_credit_code"
}

intList = ['id', 'userId', 'isCheck', 'memberType', 'memberFavoriteCount', 'memberPoints', 'isVip', 'enterpriseId',
           'figureId']

# db.create_all()
