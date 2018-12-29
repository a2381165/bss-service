# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.Boss.SpiderSchedule import SpiderSchedule, tableChangeDic
from common.Log import queryLog,addLog,deleteLog,updateLog



# 获取定时任务列表
@app.route("/findSpiderScheduleByCondition", methods=["POST"])
# @jwt_required
# @queryLog('spider_schedule')
def findSpiderScheduleBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SpiderSchedule.__tablename__
    intColumnClinetNameList = [u'scheduleId',u'isLock']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"scheduleId":tableData[0],
                "scheduleName":tableData[1],
                "scheduleDesc":tableData[2],
                "cronMinutes":tableData[3],
                "cronHour":tableData[4],
                "cronDayOfMonth":tableData[5],
                "cronDayOfWeek":tableData[6],
                "cronMonth":tableData[7],
                "createTime":str(tableData[8]),
                "isLock":tableData[9]
                                 }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取定时任务详情
@app.route("/getSpiderScheduleDetail", methods=["POST"])
# @jwt_required
# @queryLog('spider_schedule')
def getSpiderScheduleDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("scheduleId", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(SpiderSchedule, "schedule_id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"scheduleId":table.schedule_id,
                "scheduleName":table.schedule_name,
                "scheduleDesc":table.schedule_desc,
                "cronMinutes":table.cron_minutes,
                "cronHour":table.cron_hour,
                "cronDayOfMonth":table.cron_day_of_month,
                "cronDayOfWeek":table.cron_day_of_week,
                "cronMonth":table.cron_month,
                "createTime":table.create_time,
                "isLock":table.is_lock}
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除定时任务
@app.route("/deleteSpiderSchedule", methods=["POST"])
# @jwt_required
# @deleteLog('spider_schedule')
def deleteSpiderSchedule():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(SpiderSchedule, ids, "schedule_id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加定时任务
@app.route("/addSpiderSchedule", methods=["POST"])
# @jwt_required
# @addLog('spider_schedule')
def addSpiderSchedule():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("scheduleName", None),dataDict.get("scheduleDesc", None),dataDict.get("cronMinutes", None),
                 dataDict.get("cronHour", None),dataDict.get("cronDayOfMonth", None),dataDict.get("cronDayOfWeek", None),
                 dataDict.get("cronMonth", None),dataDict.get("createTime", None),dataDict.get("isLock",0))
    table = insertToSQL(SpiderSchedule, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新定时任务
@app.route("/updataSpiderSchedule", methods=["POST"])
# @jwt_required
# @updateLog('spider_schedule')
def updataSpiderSchedule():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("scheduleId", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'scheduleId',u'isLock']
    table = updataById(SpiderSchedule, dataDict, "schedule_id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)


