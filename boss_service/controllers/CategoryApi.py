# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required

from common.FormatStr import dictRemoveNone
from common.Log import addLog, updateLog, queryLog, deleteLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind, updataById
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.Category import Category, tableChangeDic
from version.v3.bossConfig import app


# 更新分类
@app.route("/updateCategory", methods=["POST"])
@jwt_required
@updateLog("data_category")
def updateCategory():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "category_id"
    intColumnClinetNameList = ("categoryId", "categoryPid", "categorySort", "isLock", "categoryCode")
    infoList = []
    idList = dataDict.get("ids", None)

    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in idList:
        table = updataById(Category, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if table == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif table == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        else:
            infoDic = dictInfoSort(table)
        infoList.append(infoDic)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 删除分类
@app.route("/deleteCategory", methods=["POST"])
@jwt_required
@deleteLog("data_category")
def deleteCategory():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])

    resultDict = deleteById(Category, idList, "category_id")
    return jsonify(resultDict)


# 根据条件查询
@app.route("/findCategoryByCondition", methods=["POST"])
@jwt_required
@queryLog("data_category")
def findCategoryByCondition():
    if not request.json:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    else:
        intColumnClinetNameList = ("categoryId", "categoryPid", "categorySort", "isLock", "categoryCode")
        tableName = Category.__tablename__
        tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
        if tableList:
            InfoList = []
            for tableData in tableList:
                infoDict = {
                    "categoryId": tableData[0],
                    "categoryName": tableData[1],
                    "categoryPid": tableData[2],
                    "categorySort": tableData[3],
                    "isLock": tableData[4],
                    "categoryCode": tableData[5]
                }
                InfoList.append(infoDict)
            resultDict = returnMsg(InfoList)
            resultDict["total"] = count
        else:
            resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 获取详情
@app.route("/findCategoryById", methods=["POST"])
@jwt_required
@queryLog("data_category")
def findCategoryById():
    if not request.json:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('categoryId', None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    else:
        table = findById(Category, "category_id", id)
        if table:
            infoDict = dictInfoSort(table)
            resultDict = returnMsg(infoDict)
        elif table == 0:
            infoDict = {}
            resultDict = returnMsg(infoDict)
        else:
            resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 添加数据
@app.route("/addCategory", methods=["POST"])
@jwt_required
@addLog("data_category")
def addCategory():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)

    columnsStr = (dataDict.get('categoryName'), dataDict.get('categoryPid'), dataDict.get('categorySort'),
                  dataDict.get('isLock', 0), dataDict.get("categoryCode"))
    table = insertToSQL(Category, *columnsStr)
    if table:
        infoDict = dictInfoSort(table)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def dictInfoSort(table):
    infoDict = {
        "categoryId": table.category_id,
        "categoryName": table.category_name,
        "categoryPid": table.category_pid,
        "categorySort": table.category_sort,
        "isLock": table.is_lock,
        "categoryCode": table.category_code
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict
