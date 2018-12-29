# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Data.WorkFlow import WorkFlow, WorkFlowChangeDic as tableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog
from models.Data.SubFlow import SubFlow


# 获取 列表
@app.route("/findWorkFlowByCondition", methods=["POST"])
@jwt_required
@queryLog('data_work_flow')
def findWorkFlowBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = WorkFlow.__tablename__
    intColumnClinetNameList = [u'id', u'num']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "name": tableData[1],
                        "desc": tableData[2],
                        "num": tableData[3], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getWorkFlowDetail", methods=["POST"])
@jwt_required
@queryLog('data_work_flow')
def getWorkFlowDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(WorkFlow, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "name": table.name,
                "desc": table.desc,
                "num": table.num, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteWorkFlow", methods=["POST"])
@jwt_required
@deleteLog('data_work_flow')
def deleteWorkFlow():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("ids", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in ids:
        table = findById(SubFlow, "flow_id", id)
        if table:
            resultDict = returnErrorMsg(errorCode["has_son"])
            return jsonify(resultDict)
    count = deleteByIdBoss(WorkFlow, ids, "id")
    if count == len(ids):
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addWorkFlow", methods=["POST"])
@jwt_required
@addLog('data_work_flow')
def addWorkFlow():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    now = getTimeStrfTimeStampNow()
    columsStr = (dataDict.get("name", None), dataDict.get("desc", None), dataDict.get("num", None), now)
    table = insertToSQL(WorkFlow, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataWorkFlow", methods=["POST"])
@jwt_required
@updateLog('data_work_flow')
def updataWorkFlow():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'num']
    table = updataById(WorkFlow, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
