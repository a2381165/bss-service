# -*- coding: utf-8 -*-
from config import db


class ServiceAttach(db.Model):
    __tablename__ = "data_service_attach"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    attach_extension_name = db.Column(db.String(50))
    attach_size = db.Column(db.String(None))
    attach_title = db.Column(db.String(255))
    attach_path = db.Column(db.String(255))
    create_time = db.Column(db.DateTime)
    type = db.Column(db.SmallInteger)
    create_person = db.Column(db.String(20))

    def __init__(self, attach_extension_name, attach_size, attach_title, attach_path, create_time, type, create_person):
        '''Constructor'''
        self.attach_extension_name = attach_extension_name
        self.attach_size = attach_size
        self.attach_title = attach_title
        self.attach_path = attach_path
        self.create_time = create_time
        self.type = type
        self.create_person = create_person

    def __repr__(self):
        return 'id : %s' % self.id


# Client and database attributes dictionary
clinetHead = {u'id', u'attachExtensionName', u'attachSize', u'attachTitle', u'attachPath', u'createTime', u'type',
              u'createPerson'}
ServiceAttachChangeDic = {
    "id": "id",
    "attachExtensionName": "attach_extension_name",
    "attachSize": "attach_size",
    "attachTitle": "attach_title",
    "attachPath": "attach_path",
    "createTime": "create_time",
    "type": "type",
    "createPerson": "create_person"
}

intList = {u'id', u'type'}

# db.create_all()
