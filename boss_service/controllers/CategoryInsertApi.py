# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required, current_user

from common.DatatimeNow import getTimeStrfTimeStampNow
from common.Log import addLog
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg
from models.Data.Category import Category
from models.Data.Source import Source
from version.v3.bossConfig import app


# 数据录入
@app.route("/addDataSorceBySection", methods=["POST"])
@jwt_required
@addLog("data_source")
def addDataSorceBySection():
    """数据录入"""
    adminTable = current_user
    adminName = adminTable.admin_name
    dateTimeNow = getTimeStrfTimeStampNow()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    errorList = []
    repeatList = []
    failedList = []
    checkList = []
    inputList = dataDict.get("inputList", [])
    count = 0
    dbOperation = OperationOfDB()
    for inputData in inputList:
        deptUrl = inputData.get("deptUrl", "")
        deptName = inputData.get("deptName", None)
        desUrl = inputData.get("desUrl", "")
        levelCode = inputData.get("levelCode", None)
        categoryCode = inputData.get("categoryCode", None)
        areaCode = inputData.get("areaCode", None)
        deptAddress = inputData.get("deptAddress", None)
        if (len(desUrl) > 255) or (len(deptUrl) > 255):
            inputData["errorInfo"] = "url too long"
            errorList.append(inputData)
            continue
        categoryTable = Category.query.filter(Category.category_code == categoryCode).first()
        if categoryTable:
            categoryId = categoryTable.category_id
        else:
            inputData["errorInfo"] = "categoryCode incorrect"
            errorList.append(inputData)
            continue
        dataSourctTable = Source.query.filter(Source.area_code == areaCode,
                                                  Source.dept_category == categoryId,
                                                  Source.dept_name == deptName,
                                                  Source.des_url == desUrl).first()
        if dataSourctTable:
            repeatList.append(inputData)
            continue

        dataSourceList = (levelCode, areaCode, categoryId, deptName, deptAddress, deptUrl,
                          desUrl,dateTimeNow, adminName, 0, None, None, None, 0)
        inputStatus = dbOperation.insertToSQL(Source, *dataSourceList)
        if not inputStatus:
            failedList.append(inputData)
            continue
        count += 1
        if count == 100:
            commitStatus = dbOperation.commitToSQL()
            if commitStatus:
                count = 0
            else:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("add data failed!")
                return jsonify(resultDict)
    commitStatus = dbOperation.commitToSQL()
    if not commitStatus:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("add data failed!")
        return jsonify(resultDict)
    infoDict = {
        "errorList": errorList,
        "failedList": failedList,
        "repeatList": repeatList
    }
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)
