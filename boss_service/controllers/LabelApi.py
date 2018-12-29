# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required

from common.Log import addLog, updateLog, deleteLog, queryLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind, updataById
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.Label import Label, tableChangeDic
from version.v3.bossConfig import app


# 更新
@app.route("/updateLabel", methods=["POST"])
@jwt_required
@updateLog("data_label")
def updateLabel():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "label_id"
    intColumnClinetNameList = ("labelId", "labelPid", "isLock")
    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in idList:
        menuUp = updataById(Label, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if menuUp == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif menuUp == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        else:
            infoDict = tableDictSort(menuUp)
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 删除
@app.route("/deleteLabel", methods=["POST"])
@jwt_required
@deleteLog("data_label")
def deleteLabel():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    resultDict = deleteById(Label, idList, "label_id")
    return jsonify(resultDict)


# 根据条件查询
@app.route("/findLabelByCondition", methods=["POST"])
@jwt_required
@queryLog("data_label")
def findLabelByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("labelId", "labelPid", "isLock")
    tableName = Label.__tablename__
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {
                "labelId": tableData[0],
                "labelPid": tableData[1],
                "labelName": tableData[2],
                "isLock": tableData[3],
                "sort": tableData[4],
                "labelRemark": tableData[5],
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情
@app.route("/findLabelById", methods=["POST"])
@jwt_required
@queryLog("data_label")
def findLabelById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    label_id = dataDict.get('labelId', None)
    if label_id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(Label, "label_id", id)
    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    elif table == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 添加
@app.route("addLabel", methods=["POST"])
@jwt_required
@addLog("data_label")
def addLabel():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnStr = (
        dataDict.get("labelPid", None), dataDict.get("labelName", None), dataDict.get("isLock", 0),
        dataDict.get("sort", 1),
        dataDict.get("labelRemark", ""))
    table = insertToSQL(Label, *columnStr)
    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def tableDictSort(table):
    infoDict = {
        "labelId": table.label_id,
        "labelPid": table.label_pid,
        "labelName": table.label_name,
        "isLock": table.is_lock,
        "sort": table.sort,
        "labelRemark": table.label_remark,
    }
    return infoDict
