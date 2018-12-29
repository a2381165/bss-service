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
from models.Boss.SpiderScriptSchedule import SpiderScriptSchedule, tableChangeDic
from common.Log import queryLog,addLog,deleteLog,updateLog



# 获取 列表 
@app.route("/findSpiderScriptScheduleByCondition", methods=["POST"])
@jwt_required
@queryLog('spider_script_schedule')
def findSpiderScriptScheduleBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SpiderScriptSchedule.__tablename__
    intColumnClinetNameList = [u'id', u'scheduleId', u'scriptId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id":tableData[0],
                "scheduleId":tableData[1],
                "scriptId":tableData[2],}
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getSpiderScriptScheduleDetail", methods=["POST"])
@jwt_required
@queryLog('spider_script_schedule')
def getSpiderScriptScheduleDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(SpiderScriptSchedule, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id":table.id,
                "scheduleId":table.schedule_id,
                "scriptId":table.script_id,}
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteSpiderScriptSchedule", methods=["POST"])
@jwt_required
@deleteLog('spider_script_schedule')
def deleteSpiderScriptSchedule():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(SpiderScriptSchedule, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addSpiderScriptSchedule", methods=["POST"])
@jwt_required
@addLog('spider_script_schedule')
def addSpiderScriptSchedule():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("scheduleId", None),dataDict.get("scriptId", None))
    table = insertToSQL(SpiderScriptSchedule, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataSpiderScriptSchedule", methods=["POST"])
@jwt_required
@updateLog('spider_script_schedule')
def updataSpiderScriptSchedule():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'scheduleId', u'scriptId']
    table = updataById(SpiderScriptSchedule, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)


#添加爬虫脚本定时规则
@app.route("/deploySpiderScriptSchedule", methods=["POST"])
# @jwt_required
# @updateLog('spider_script_node')
def deploySpiderScriptSchedule():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    script_idArray = dataDict.get("scriptIdArray", "")
    schedule_id = dataDict.get("scheduleId", "")
    if not schedule_id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if script_idArray:
        try:
            scriptIdList = []
            spiderScriptScheduleList = SpiderScriptSchedule.query.all()
            for script in spiderScriptScheduleList:
                scriptIdList.append(script.script_id)
            for scriptId in script_idArray:
                if scriptId not in scriptIdList:
                    columsStr = (dataDict.get("scheduleId", None), scriptId)
                    insertToSQL(SpiderScriptSchedule, *columsStr)
                else:
                    continue
            resultDict = returnMsg({})
            return jsonify(resultDict)
        except:
            resultDict = returnErrorMsg(errorCode["system_error"])
            return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)