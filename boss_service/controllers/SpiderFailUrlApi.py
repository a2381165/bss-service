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
from models.Boss.SpiderFailUrl import SpiderFailUrl, tableChangeDic
from common.Log import queryLog,addLog,deleteLog,updateLog



# 获取 列表
@app.route("/findSpiderFailUrlByCondition", methods=["POST"])
@jwt_required
@queryLog('spider_fail_url')
def findSpiderFailUrlBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SpiderFailUrl.__tablename__
    intColumnClinetNameList = [u'failId', u'deptId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"failId":tableData[0],
                "queueUrl":tableData[1],
                "spiderUrl":tableData[2],
                "statusCode":tableData[3],
                "deptNameKey":tableData[4],
                "deptId":tableData[5],
                "saveTime":tableData[6],}
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getSpiderFailUrlDetail", methods=["POST"])
@jwt_required
@queryLog('spider_fail_url')
def getSpiderFailUrlDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("failId", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(SpiderFailUrl, "fail_id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"failId":table.fail_id,
                "queueUrl":table.queue_url,
                "spiderUrl":table.spider_url,
                "statusCode":table.status_code,
                "deptNameKey":table.dept_name_key,
                "deptId":table.dept_id,
                "saveTime":table.save_time,}
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteSpiderFailUrl", methods=["POST"])
@jwt_required
@deleteLog('spider_fail_url')
def deleteSpiderFailUrl():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(SpiderFailUrl, ids, "fail_id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addSpiderFailUrl", methods=["POST"])
@jwt_required
@addLog('spider_fail_url')
def addSpiderFailUrl():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("queueUrl", None),dataDict.get("spiderUrl", None),dataDict.get("statusCode", None),dataDict.get("deptNameKey", None),dataDict.get("deptId", None),dataDict.get("saveTime", None))
    table = insertToSQL(SpiderFailUrl, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataSpiderFailUrl", methods=["POST"])
@jwt_required
@updateLog('spider_fail_url')
def updataSpiderFailUrl():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("failId", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'failId', u'deptId']
    table = updataById(SpiderFailUrl, dataDict, "fail_id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
