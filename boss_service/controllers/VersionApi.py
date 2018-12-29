# -*- coding: utf-8 -*-
import datetime
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required, current_user
from models.Boss.Version import Version, tableChangeDic

from common.FormatStr import dictRemoveNone
from common.Log import deleteLog, queryLog, updateLog
from common.OperationOfDB import deleteById, insertToSQL, conditionDataListFind, updataById, addTokenToSql
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app


# 更新版本号
@app.route("/updateVersion", methods=["POST"])
@jwt_required
@updateLog("boss_version")
def updateVersion():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    isLock = dataDict.get("isLock", None)
    appType = dataDict.get("appType", None)
    columnId = "id"
    intColumnClinetNameList = ("id", "updateType", "isLock", "appType")
    infoList = []
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg("not find ids!")
        return jsonify(resultDict)
    if isLock and int(isLock) not in (0, 1):
        resultDict = returnErrorMsg("isLock not in 0,1")
        return jsonify(resultDict)
    if  isLock and int(isLock) == 1 and (len(idList) > 1 or appType == None):
        resultDict = returnErrorMsg("lock version must be unique!")
        return jsonify(resultDict)
    elif isLock and int(isLock) == 1 and len(idList) == 1 and int(appType) == 1:
        versionTable = Version.query.filter(Version.is_lock == 1, Version.app_type == 1).first()
        if versionTable:
            versionTable.is_lock = 0
            addTokenToSql(versionTable)
    elif isLock and int(isLock) == 1 and len(idList) == 1 and int(appType) == 2:
        versionTable = Version.query.filter(Version.is_lock == 1, Version.app_type == 2).first()
        if versionTable:
            versionTable.is_lock = 0
            addTokenToSql(versionTable)

    for id in idList:
        versionUpTable = updataById(Version, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if versionUpTable == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif versionUpTable == 0:
            resultDict = returnErrorMsg("this version not exit!")
            return jsonify(resultDict)
        else:
            infoDict = tableDictSort(versionUpTable)
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 删除版本号
@app.route("/deleteVersion", methods=["POST"])
@jwt_required
@deleteLog("boss_version")
def deleteVersionByIds():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])

    resultDict = deleteById(Version, idList, "id")
    return jsonify(resultDict)


# 通过条件 筛选
@app.route("/findVersionByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_version")
def findVersionByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get("condition", None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    intColumnClinetNameList = ("id", "updateType", "isLock")
    tableName = Version.__tablename__
    versionList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    if versionList:
        InfoList = []
        for tableData in versionList:
            infoDict = {
                "id": tableData[0],
                "appId": tableData[1],
                "appType": tableData[2],
                "updateType": tableData[3],
                "version": tableData[4],
                "urlOne": tableData[5],
                "urlTwo": tableData[6],
                "urlThree": tableData[7],
                "isLock": tableData[8],
                "createTime": tableData[9],
                "createPerson": tableData[10],
                "verisonRemark": tableData[11]
            }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 查看详情
@app.route("/findVersionById", methods=["POST"])
@jwt_required
@queryLog("boss_version")
def findVersionById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    Id = dataDict.get("Id")
    if Id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    versionTable = Version.query.filter(Version.id == Id).first()
    if versionTable:
        infoDict = tableDictSort(versionTable)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg("this version not exit!")
    return jsonify(resultDict)


# 添加
@app.route("/insertVersion", methods=["POST"])
@jwt_required
def insertVersion():
    adminTable = current_user
    createPerson = adminTable.admin_name
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    appId = dataDict.get("appId", None)
    appType = dataDict.get("appType", None)
    updateType = dataDict.get("updateType", None)
    version = dataDict.get("version", None)
    urlOne = dataDict.get("urlOne", None)
    urlTwo = dataDict.get("urlTwo", None)
    urlThree = dataDict.get("urlThree", None)
    isLock = dataDict.get("isLock", 0)
    if not (appId and appType and updateType and version and (urlOne or urlThree or urlTwo) and (
            int(isLock) in (0, 1))):
        resultDict = returnErrorMsg("args not enough")
        return jsonify(resultDict)

    if int(isLock) == 1 and appType == None:
        resultDict = returnErrorMsg("lock version must be unique!")
        return jsonify(resultDict)
    elif int(isLock) == 1 and int(appType) == 1:
        versionTables = Version.query.filter(Version.is_lock == 1, Version.app_type == 1).first()
        if versionTables:
            versionTables.is_lock = 0
            addTokenToSql(versionTables)
    elif int(isLock) == 1 and int(appType) == 2:
        versionTables = Version.query.filter(Version.is_lock == 1, Version.app_type == 2).first()
        if versionTables:
            versionTables.is_lock = 0
            addTokenToSql(versionTables)
    dateTimeNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    columnsStr = (appId, appType, updateType, version, urlOne, urlTwo, urlThree, isLock, dateTimeNow, createPerson,
                  dataDict.get("verisonRemark", ""))

    versionTable = insertToSQL(Version, *columnsStr)
    if versionTable:
        infoDict = tableDictSort(versionTable)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def tableDictSort(table):
    infoDict = {
        "id": table.id,
        "appId": table.app_id,
        "appType": table.app_type,
        "updateType": table.update_type,
        "version": table.version,
        "urlOne": table.url_one,
        "urlTwo": table.url_two,
        "urlThree": table.url_three,
        "isLock": table.is_lock,
        "createTime": table.create_time,
        "createPerson": table.create_person,
        "verisonRemark": table.verison_remark,
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict
