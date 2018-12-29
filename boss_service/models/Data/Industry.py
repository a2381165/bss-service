
# -*- coding: utf-8 -*-
from config import db


class Industry(db.Model):
    __tablename__ = "data_industry"

    industry_id = db.Column(db.Integer, primary_key=True, nullable=False)
    industry_name = db.Column(db.String(50))
    industry_pid = db.Column(db.Integer)
    industry_code = db.Column(db.String(20))
    industry_sort = db.Column(db.Integer)
    is_lock = db.Column(db.SmallInteger)
    industry_remark = db.Column(db.Text)

    def __init__(self, industry_id,industry_name,industry_pid,industry_code,industry_sort,is_lock,industry_remark):
        '''Constructor'''
        self.industry_id=industry_id
        self.industry_name=industry_name
        self.industry_pid=industry_pid
        self.industry_code=industry_code
        self.industry_sort=industry_sort
        self.is_lock=is_lock
        self.industry_remark=industry_remark


    def __repr__(self):
        return 'industry_id : %s' % self.industry_id


# Client and database attributes dictionary
clinetHead = {u'industryId', u'industryName', u'industryPid', u'industryCode', u'industrySort', u'isLock', u'industryRemark'}
tableChangeDic = {
    "industryId":"industry_id",
    "industryName":"industry_name",
    "industryPid":"industry_pid",
    "industryCode":"industry_code",
    "industrySort":"industry_sort",
    "isLock":"is_lock",
    "industryRemark":"industry_remark"
}

intList = {u'industryId', u'industryPid', u'industrySort', u'isLock'}

# db.create_all()
