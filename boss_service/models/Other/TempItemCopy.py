# -*- coding: utf-8 -*-
from config import db


class TempItemCopy(db.Model):
    __tablename__ = "boss_temp_item_copy"

    item_id = db.Column(db.Integer, primary_key=True, nullable=False)
    dept_id = db.Column(db.Integer)
    item_title = db.Column(db.String(100))
    item_content = db.Column(db.Text)
    item_pulishdate = db.Column(db.String(32))
    item_contact = db.Column(db.String(200))
    item_pricerange = db.Column(db.String(50))
    item_deadline = db.Column(db.DateTime)
    item_submit_address = db.Column(db.String(100))
    item_url = db.Column(db.String(255))
    item_imgurl = db.Column(db.String(255))
    item_industry_ids = db.Column(db.String(200))
    item_category_ids = db.Column(db.String(200))
    check_status_one = db.Column(db.SmallInteger)
    check_person_one = db.Column(db.String(20))
    check_remark_one = db.Column(db.String(200))
    check_time_one = db.Column(db.DateTime)
    check_status_two = db.Column(db.SmallInteger)
    check_person_two = db.Column(db.String(20))
    check_remark_two = db.Column(db.String(200))
    check_time_two = db.Column(db.DateTime)
    check_status_three = db.Column(db.SmallInteger)
    check_person_three = db.Column(db.String(20))
    check_remark_three = db.Column(db.String(200))
    check_time_three = db.Column(db.DateTime)
    service_name = db.Column(db.String(50))
    service_code = db.Column(db.String(30))
    service_startdate = db.Column(db.DateTime)
    service_enddate = db.Column(db.DateTime)
    service_price = db.Column(db.Numeric(12,2),server_default="0.00")
    service_rate = db.Column(db.Integer)
    service_content = db.Column(db.Text)
    service_process = db.Column(db.String(255))
    service_protocol = db.Column(db.String(255))
    service_list = db.Column(db.String(500))
    service_contact_person = db.Column(db.String(20))
    service_contact_phone = db.Column(db.String(20))
    is_product = db.Column(db.SmallInteger)
    item_enter_person = db.Column(db.String(20))
    item_enter_time = db.Column(db.DateTime)
    temp_item_status = db.Column(db.SmallInteger)
    type_of_contract = db.Column(db.Integer)
    publish_dept = db.Column(db.String(20))

    def __init__(self, dept_id, item_title, item_content, item_pulishdate, item_contact, item_pricerange, item_deadline,
                 item_submit_address, item_url, item_imgurl, item_industry_ids, item_category_ids, check_status_one,
                 check_person_one, check_remark_one, check_time_one, check_status_two, check_person_two,
                 check_remark_two, check_time_two, check_status_three, check_person_three, check_remark_three,
                 check_time_three, service_name, service_code, service_startdate, service_enddate, service_price,
                 service_rate, service_content, service_process, service_protocol, service_list, service_contact_person,
                 service_contact_phone, is_product, item_enter_person, item_enter_time, temp_item_status,
                 type_of_contract, publish_dept):
        '''Constructor'''
        self.dept_id = dept_id
        self.item_title = item_title
        self.item_content = item_content
        self.item_pulishdate = item_pulishdate
        self.item_contact = item_contact
        self.item_pricerange = item_pricerange
        self.item_deadline = item_deadline
        self.item_submit_address = item_submit_address
        self.item_url = item_url
        self.item_imgurl = item_imgurl
        self.item_industry_ids = item_industry_ids
        self.item_category_ids = item_category_ids
        self.check_status_one = check_status_one
        self.check_person_one = check_person_one
        self.check_remark_one = check_remark_one
        self.check_time_one = check_time_one
        self.check_status_two = check_status_two
        self.check_person_two = check_person_two
        self.check_remark_two = check_remark_two
        self.check_time_two = check_time_two
        self.check_status_three = check_status_three
        self.check_person_three = check_person_three
        self.check_remark_three = check_remark_three
        self.check_time_three = check_time_three
        self.service_name = service_name
        self.service_code = service_code
        self.service_startdate = service_startdate
        self.service_enddate = service_enddate
        self.service_price = service_price
        self.service_rate = service_rate
        self.service_content = service_content
        self.service_process = service_process
        self.service_protocol = service_protocol
        self.service_list = service_list
        self.service_contact_person = service_contact_person
        self.service_contact_phone = service_contact_phone
        self.is_product = is_product
        self.item_enter_person = item_enter_person
        self.item_enter_time = item_enter_time
        self.temp_item_status = temp_item_status
        self.type_of_contract = type_of_contract
        self.publish_dept = publish_dept

    def __repr__(self):
        return 'item_id : %s' % self.item_id


# Client and database attributes dictionary
clinetHead = {u'itemId', u'deptId', u'itemTitle', u'itemContent', u'itemPulishdate', u'itemContact', u'itemPricerange',
              u'itemDeadline', u'itemSubmitAddress', u'itemUrl', u'itemImgurl', u'itemIndustryIds', u'itemCategoryIds',
              u'checkStatusOne', u'checkPersonOne', u'checkRemarkOne', u'checkTimeOne', u'checkStatusTwo',
              u'checkPersonTwo', u'checkRemarkTwo', u'checkTimeTwo', u'checkStatusThree', u'checkPersonThree',
              u'checkRemarkThree', u'checkTimeThree', u'serviceName', u'serviceCode', u'serviceStartdate',
              u'serviceEnddate', u'servicePrice', u'serviceRate', u'serviceContent', u'serviceProcess',
              u'serviceProtocol', u'serviceList', u'serviceContactPerson', u'serviceContactPhone', u'isProduct',
              u'itemEnterPerson', u'itemEnterTime', u'tempItemStatus', u'typeOfContract', u'publishDept'}
tableChangeDic = {
    "itemId": "item_id",
    "deptId": "dept_id",
    "itemTitle": "item_title",
    "itemContent": "item_content",
    "itemPulishdate": "item_pulishdate",
    "itemContact": "item_contact",
    "itemPricerange": "item_pricerange",
    "itemDeadline": "item_deadline",
    "itemSubmitAddress": "item_submit_address",
    "itemUrl": "item_url",
    "itemImgurl": "item_imgurl",
    "itemIndustryIds": "item_industry_ids",
    "itemCategoryIds": "item_category_ids",
    "checkStatusOne": "check_status_one",
    "checkPersonOne": "check_person_one",
    "checkRemarkOne": "check_remark_one",
    "checkTimeOne": "check_time_one",
    "checkStatusTwo": "check_status_two",
    "checkPersonTwo": "check_person_two",
    "checkRemarkTwo": "check_remark_two",
    "checkTimeTwo": "check_time_two",
    "checkStatusThree": "check_status_three",
    "checkPersonThree": "check_person_three",
    "checkRemarkThree": "check_remark_three",
    "checkTimeThree": "check_time_three",
    "serviceName": "service_name",
    "serviceCode": "service_code",
    "serviceStartdate": "service_startdate",
    "serviceEnddate": "service_enddate",
    "servicePrice": "service_price",
    "serviceRate": "service_rate",
    "serviceContent": "service_content",
    "serviceProcess": "service_process",
    "serviceProtocol": "service_protocol",
    "serviceList": "service_list",
    "serviceContactPerson": "service_contact_person",
    "serviceContactPhone": "service_contact_phone",
    "isProduct": "is_product",
    "itemEnterPerson": "item_enter_person",
    "itemEnterTime": "item_enter_time",
    "tempItemStatus": "temp_item_status",
    "typeOfContract": "type_of_contract",
    "publishDept": "publish_dept"
}

intList = {u'itemId', u'deptId', u'checkStatusOne', u'checkStatusTwo', u'checkStatusThree', u'serviceRate',
           u'isProduct', u'tempItemStatus', u'typeOfContract'}

# db.create_all()
