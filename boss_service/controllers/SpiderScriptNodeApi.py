# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.Boss.SpiderScriptNode import SpiderScriptNode, tableChangeDic
from common.Log import queryLog,addLog,deleteLog,updateLog



# 获取 列表 
@app.route("/findSpiderScriptNodeByCondition", methods=["POST"])
@jwt_required
@queryLog('spider_script_node')
def findSpiderScriptNodeBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SpiderScriptNode.__tablename__
    intColumnClinetNameList = [u'id', u'nodeId', u'scriptId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id":tableData[0],
                "nodeId":tableData[1],
                "scriptId":tableData[2],}
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getSpiderScriptNodeDetail", methods=["POST"])
@jwt_required
@queryLog('spider_script_node')
def getSpiderScriptNodeDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(SpiderScriptNode, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id":table.id,
                "nodeId":table.node_id,
                "scriptId":table.script_id,}
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteSpiderScriptNode", methods=["POST"])
@jwt_required
@deleteLog('spider_script_node')
def deleteSpiderScriptNode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(SpiderScriptNode, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addSpiderScriptNode", methods=["POST"])
@jwt_required
@addLog('spider_script_node')
def addSpiderScriptNode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("nodeId", None),dataDict.get("scriptId", None))
    table = insertToSQL(SpiderScriptNode, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataSpiderScriptNode", methods=["POST"])
@jwt_required
@updateLog('spider_script_node')
def updataSpiderScriptNode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'nodeId', u'scriptId']
    table = updataById(SpiderScriptNode, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)

#添加爬虫脚本到节点
@app.route("/deploySpiderScriptNode", methods=["POST"])
# @jwt_required
# @updateLog('spider_script_node')
def deploySpiderScriptNode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    script_idArray = dataDict.get("scriptIdArray", "")
    node_id = dataDict.get("nodeId", "")
    if not node_id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if script_idArray:
        try:
            scriptIdList = []
            SpiderScriptNodeList = SpiderScriptNode.query.all()
            for script in SpiderScriptNodeList:
                scriptIdList.append(script.script_id)
            for scriptId in script_idArray:
                if scriptId not in scriptIdList:
                    columsStr = (dataDict.get("nodeId", None), scriptId)
                    insertToSQL(SpiderScriptNode, *columsStr)
                else:
                    resultDict = returnMsg("Data already exists")
                    return jsonify(resultDict)
            resultDict = returnMsg({})
            return jsonify(resultDict)
        except:
            resultDict = returnErrorMsg(errorCode["system_error"])
            return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
