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
from models.Boss.SpiderDeploy import SpiderDeploy, tableChangeDic
from common.Log import queryLog,addLog,deleteLog,updateLog



# 获取 列表
@app.route("/findSpiderDeployByCondition", methods=["POST"])
# @jwt_required
# @queryLog('spider_deploy')
def findSpiderDeployBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SpiderDeploy.__tablename__
    intColumnClinetNameList = [u'deployId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"deployId":tableData[0],
                "description":tableData[1],
                "deployedAt":tableData[2],
                "createdAt":tableData[3],
                "updatedAt":tableData[4],}
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getSpiderDeployDetail", methods=["POST"])
# @jwt_required
# @queryLog('spider_deploy')
def getSpiderDeployDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("deployId", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(SpiderDeploy, "deploy_id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"deployId":table.deploy_id,
                "description":table.description,
                "deployedAt":table.deployed_at,
                "createdAt":table.created_at,
                "updatedAt":table.updated_at,}
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteSpiderDeploy", methods=["POST"])
# @jwt_required
# @deleteLog('spider_deploy')
def deleteSpiderDeploy():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(SpiderDeploy, ids, "deploy_id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addSpiderDeploy", methods=["POST"])
# @jwt_required
# @addLog('spider_deploy')
def addSpiderDeploy():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("description", None),dataDict.get("deployedAt", None),dataDict.get("createdAt", None),
                 dataDict.get("updatedAt", None))
    table = insertToSQL(SpiderDeploy, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataSpiderDeploy", methods=["POST"])
# @jwt_required
# @updateLog('spider_deploy')
def updataSpiderDeploy():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("deployId", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'deployId']
    table = updataById(SpiderDeploy, dataDict, "deploy_id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
