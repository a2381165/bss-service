# coding:utf-8

import requests

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required

from common.SpiderUtils import scrapyd_url
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from models.Boss.SpiderNode import SpiderNode, tableChangeDic
from version.v3.bossConfig import app


# 获取节点列表
@app.route("/findSpiderNodeByCondition", methods=["POST"])
# @jwt_required
# @queryLog('spider_node')
def findSpiderNodeBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SpiderNode.__tablename__
    intColumnClinetNameList = [u'node_id', u'nodePort', u'nodeStatus', u'deployStatus']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id":tableData[0],
                "nodeMing":tableData[1],
                "description":tableData[2],
                "nodeIp":tableData[3],
                "nodePort":tableData[4],
                "nodeStatus":tableData[5],
                "projectName":tableData[6],
                "deployStatus":tableData[7],
                "nodeIpPort":str(tableData[3]) + ':' +str(tableData[4])
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取节点详情
@app.route("/getSpiderNodeDetail", methods=["POST"])
# @jwt_required
# @queryLog('spider_node')
def getSpiderNodeDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("nodeId", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(SpiderNode, "node_id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"node_id":table.node_id,
                "nodeMing":table.node_name,
                "description":table.description,
                "nodeIp":table.node_ip,
                "nodePort":table.node_port,
                "nodeStatus":table.node_status,
                "projectName":table.project_name,
                "deployStatus":table.deploy_status,}
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除节点
@app.route("/deleteSpiderNode", methods=["POST"])
# @jwt_required
# @deleteLog('spider_node')
def deleteSpiderNode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(SpiderNode, ids, "node_id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加节点
@app.route("/addSpiderNode", methods=["POST"])
# @jwt_required
# @addLog('spider_node')
def addSpiderNode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("nodeMing", None),dataDict.get("description", None),dataDict.get("nodeIp", None),
                 dataDict.get("nodePort", None),dataDict.get("nodeStatus", 1),dataDict.get("projectName", None),
                 dataDict.get("deployStatus", 0))
    table = insertToSQL(SpiderNode, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新节点
@app.route("/updataSpiderNode", methods=["POST"])
# @jwt_required
# @updateLog('spider_node')
def updataSpiderNode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("nodeId", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'nodeId', u'nodePort', u'nodeStatus', u'deployStatus']
    table = updataById(SpiderNode, dataDict, "node_id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)



# 获取节点状态
@app.route("/getSpiderNodeStatus", methods=["POST"])
# @jwt_required
# @queryLog('spider_node')
def getSpiderNodeStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("nodeId", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(SpiderNode, "node_id", id)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    infoDict = {"nodeIp":table.node_ip,
                "nodePort":table.node_port,
                }
    try:
        result = requests.get(scrapyd_url(infoDict.get("nodeIp"),infoDict.get("nodePort")),timeout=3)
        httpCode = result.status_code
        return jsonify(returnMsg({'httpCode': httpCode}))
    except:
        resultDict = returnErrorMsg({'httpCode': 500})
        return jsonify(resultDict)







