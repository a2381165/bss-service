# coding:utf-8
from flask import json
from decimal import Decimal
# from bson.objectid import ObjectId
from datetime import date, datetime


def dictRemoveNone(infoDict):
    if not isinstance(infoDict, dict):
        return infoDict
    for key, value in infoDict.items():
        infoDict[key] = getTimeToStrfdate(value)
        if value == "null" or value == None or value == "None":
            infoDict[key] = ""
    return infoDict


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, (date, datetime)):
            return str(o)
        # if isinstance(o, ObjectId):
        #     return str(o)
        if isinstance(o, Decimal):
            return float(o)
        return json.JSONEncoder.default(self, o)

def getTimeToStrftime(time):
    if time:
        strftime = time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        strftime = ""
    return strftime


def getTimeToStrfdate(strftime):
    if strftime:
        try:
            strftime = strftime.strftime("%Y-%m-%d")
        except:
            return strftime
    return strftime