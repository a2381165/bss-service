#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/7 0007 09:39
# @Site    : 
# @File    : uploadFile.py
# @Software: PyCharm
import json
import time
import base64
import os
# from config import logger
# from common.ReturnMessage import returnErrorMsg, returnMsg, errorCode
import zlib


def itemPhotoUpload(itemAlbum, itemId, temporary, picName):
    try:
        infoList = []
        for index, image in enumerate(itemAlbum):
            newDict = {}
            for _content in image.split(";"):
                if ":" in _content:
                    _content = _content.split(":")
                    newDict[_content[0]] = _content[1]
                elif "," in _content:
                    _content = _content.split(",")
                    newDict[_content[0]] = _content[1]
            imgTypeStr = newDict.get("data", "")
            imgBase = newDict.get("base64", "")
            if imgTypeStr and imgBase:
                typeList = imgTypeStr.split(r"/")
                if len(typeList) == 2:
                    dateTimeStr = str(time.time())[:-3]
                    imgType = typeList[1]
                    imgData = base64.b64decode(imgBase)
                    filePath = r"static/item/%s/%s" % (itemId, temporary)
                    saveFile = filePath + r"/%s%s%s.%s" % (picName, dateTimeStr, index, imgType)
                    if not os.path.isdir(filePath):
                        os.makedirs(filePath)
                    leniyimg = open(saveFile, "wb")
                    leniyimg.write(imgData)
                    leniyimg.close()
                    infoList.append(saveFile[7:])
                else:
                    infoList = False
            else:
                infoList = False
    except Exception, e:
        # logger.error(e)
        infoList = False
    return infoList


def zilbImage(data=None):
    if not data:
        data = """["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAALQAAAC0CAIAAACyr5FlAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDUuNi1jMTM4IDc5LjE1OTgyNCwgMjAxNi8wOS8xNC0wMTowOTowMSAgICAgICAgIj4gPHJkZjpSREYgeG1sbnM6cmRmPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5LzAyLzIyLXJkZi1zeW50YXgtbnMjIj4gPHJkZjpEZXNjcmlwdGlvbiByZGY6YWJvdXQ9IiIgeG1sbnM6eG1wPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvIiB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIgeG1sbnM6c3RSZWY9Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9zVHlwZS9SZXNvdXJjZVJlZiMiIHhtcDpDcmVhdG9yVG9vbD0iQWRvYmUgUGhvdG9zaG9wIENDIDIwMTcgKFdpbmRvd3MpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkY2REUzNkQxMDc4QTExRTdCQ0Q2OTAxODQwOUE2RTQzIiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkY2REUzNkQyMDc4QTExRTdCQ0Q2OTAxODQwOUE2RTQzIj4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RjZERTM2Q0YwNzhBMTFFN0JDRDY5MDE4NDA5QTZFNDMiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RjZERTM2RDAwNzhBMTFFN0JDRDY5MDE4NDA5QTZFNDMiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz5vxU1lAAARDklEQVR42uzd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"]"""
    print len(data)
    data = zlib.compress(data, 9)
    print len(data)
