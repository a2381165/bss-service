# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required

from common.FormatStr import dictRemoveNone
from common.Log import addLog, updateLog, queryLog, deleteLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind, updataById
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.Industry import Industry, tableChangeDic
from version.v3.bossConfig import app


# 更新
@app.route("/updateIndustry", methods=["POST"])
@jwt_required
@updateLog("data_industry")
def updateIndustry():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "industry_id"
    intColumnClinetNameList = ("industryId", "industryPid","industrySort", "isLock")
    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    for id in idList:
        menuUp = updataById(Industry, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
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
@app.route("/deleteIndustry", methods=["POST"])
@jwt_required
@deleteLog("data_industry")
def deleteIndustry():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])

    resultDict = deleteById(Industry, idList, "industry_id")
    return jsonify(resultDict)

# 根据条件查询
@app.route("/findIndustryByCondition", methods=["POST"])
@jwt_required
@queryLog("data_industry")
def findIndustryByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList =("industryId", "industryPid","industrySort", "isLock")
    tableName = Industry.__tablename__
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {
                "industryId":tableData[0],
                "industryName":tableData[1],
                "industryPid":tableData[2],
                "industryCode":tableData[3],
                "industrySort":tableData[4],
                "isLock":tableData[5]
                }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

# 获取详情
@app.route("/findIndustryById", methods=["POST"])
@jwt_required
@queryLog("data_industry")
def findIndustryById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('industryId', None)
    if id ==None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(Industry, "industry_id", id)
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
@app.route("/addIndustry", methods=["POST"])
@jwt_required
@addLog("data_industry")
def addIndustry():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)

    columnsStr = ( dataDict.get('industryName',None),dataDict.get('industryPid', None), dataDict.get('industryCode',None),
                   dataDict.get('industrySort',None), dataDict.get('isLock',0),dataDict.get("industryRemark",None))
    table = insertToSQL(Industry, *columnsStr)
    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

def tableDictSort(table):
    infoDict = {
        "industryId":table.industry_id,
        "industryName":table.industry_name,
        "industryPid":table.industry_pid,
        "industryCode":table.industry_code,
        "industrySort":table.industry_sort,
        "isLock":table.is_lock,
        "industryRemark":table.industry_remark
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict