
# -*- coding: utf-8 -*-
from config import db


class UserOrderCoupon(db.Model):
    __tablename__ = "zzh_user_order_coupon"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    order_no = db.Column(db.String(64))
    member_coupon_id = db.Column(db.Integer)
    coupon_name = db.Column(db.String(20))
    coupon_description = db.Column(db.String(255))
    coupon_code = db.Column(db.String(50))
    coupon_expirationdate = db.Column(db.DateTime)
    coupon_type = db.Column(db.SmallInteger)
    coupon_conditions = db.Column(db.SmallInteger)
    coupon_discount = db.Column(db.SmallInteger)
    coupon_need_price = db.Column(db.Numeric(10,2))
    coupon_top_price = db.Column(db.Numeric(10,2))
    coupon_percentage = db.Column(db.Integer)

    def __init__(self, id,order_no,member_coupon_id,coupon_name,coupon_description,coupon_code,coupon_expirationdate,coupon_type,coupon_conditions,coupon_discount,coupon_need_price,coupon_top_price,coupon_percentage):
        '''Constructor'''
        self.id=id
        self.order_no=order_no
        self.member_coupon_id=member_coupon_id
        self.coupon_name=coupon_name
        self.coupon_description=coupon_description
        self.coupon_code=coupon_code
        self.coupon_expirationdate=coupon_expirationdate
        self.coupon_type=coupon_type
        self.coupon_conditions=coupon_conditions
        self.coupon_discount=coupon_discount
        self.coupon_need_price=coupon_need_price
        self.coupon_top_price=coupon_top_price
        self.coupon_percentage=coupon_percentage


    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'orderNo', u'memberCouponId', u'couponName', u'couponDescription', u'couponCode', u'couponExpirationdate', u'couponType', u'couponConditions', u'couponDiscount', u'couponNeedPrice', u'couponTopPrice', u'couponPercentage'}
UserOrderCouponChangeDic = {
    "id":"id",
    "orderNo":"order_no",
    "memberCouponId":"member_coupon_id",
    "couponName":"coupon_name",
    "couponDescription":"coupon_description",
    "couponCode":"coupon_code",
    "couponExpirationdate":"coupon_expirationdate",
    "couponType":"coupon_type",
    "couponConditions":"coupon_conditions",
    "couponDiscount":"coupon_discount",
    "couponNeedPrice":"coupon_need_price",
    "couponTopPrice":"coupon_top_price",
    "couponPercentage":"coupon_percentage"
}

intList = {u'id', u'memberCouponId', u'couponType', u'couponConditions', u'couponDiscount', u'couponPercentage'}

# db.create_all()
