# -*- coding: utf-8 -*-

import datetime
import time


# 获取原始时间戳，返回浮点型
def getTimeInt():
    return time.time()


def returnEmailCodeTime(deltaStr=False):
    timeNow = datetime.datetime.now()
    if deltaStr:
        delta = datetime.timedelta(deltaStr)
    else:
        delta = datetime.timedelta(minutes=30)
    expireTime = timeNow + delta
    timeNow.strftime("%Y-%m-%d %H:%M:%S")
    expireTime.strftime("%Y-%m-%d %H:%M:%S")
    return str(timeNow), str(expireTime)


def getTimeStampNow():
    timeNow = datetime.datetime.now()
    return timeNow


def getTimeStrfTimeStampNow():
    timeNow = datetime.datetime.now()
    timeNow.strftime("%Y-%m-%d %H:%M:%S")
    return str(timeNow)


def getTimeDaysLate(daysInt):
    timeNow = datetime.datetime.now()
    delta = datetime.timedelta(days=daysInt)
    getTime = timeNow - delta
    getTime.strftime("%Y-%m-%d %H:%M:%S")
    return str(getTime)


def getInTimeTimeDaysLate(inTime, daysInt):
    delta = datetime.timedelta(days=daysInt)
    getTime = inTime + delta
    getTime.strftime("%Y-%m-%d")
    return str(getTime)


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
