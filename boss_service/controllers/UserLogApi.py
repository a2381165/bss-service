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
from models.Boss.UserLog import UserLog, tableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取 列表 
@app.route("/findUserLogByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_user_log')
def findUserLogBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = UserLog.__tablename__
    intColumnClinetNameList = [u'id', u'userId', u'logGroup']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "userId": tableData[1],
                        "adminName": tableData[2],
                        "logGroup": tableData[3],
                        "logIp": tableData[4],
                        "logAction": tableData[5],
                        "logRemark": tableData[6],
                        "logAddTime": tableData[7], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getUserLogDetail", methods=["POST"])
@jwt_required
@queryLog('boss_user_log')
def getUserLogDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserLog, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "userId": table.user_id,
                "adminName": table.admin_name,
                "logGroup": table.log_group,
                "logIp": table.log_ip,
                "logAction": table.log_action,
                "logRemark": table.log_remark,
                "logAddTime": table.log_add_time, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserLog", methods=["POST"])
@jwt_required
@deleteLog('boss_user_log')
def deleteUserLog():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserLog, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserLog", methods=["POST"])
@jwt_required
@addLog('boss_user_log')
def addUserLog():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("userId", None), dataDict.get("adminName", None), dataDict.get("logGroup", None),
                 dataDict.get("logIp", None), dataDict.get("logAction", None), dataDict.get("logRemark", None),
                 dataDict.get("logAddTime", None))
    table = insertToSQL(UserLog, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataUserLog", methods=["POST"])
@jwt_required
@updateLog('boss_user_log')
def updataUserLog():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'userId', u'logGroup']
    table = updataById(UserLog, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
