# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Boss.PotentialCustomers import PotentialCustomers, PotentialCustomersChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
from models.Boss.Communicate import Communicate


# 获取 列表
@app.route("/findPotentialCustomersByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_potential_customers')
def findPotentialCustomersByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = PotentialCustomers.__tablename__
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = tableSortDict(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getPotentialCustomersDetail", methods=["POST"])
@jwt_required
@queryLog('boss_potential_customers')
def getPotentialCustomersDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(PotentialCustomers, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deletePotentialCustomers", methods=["POST"])
@jwt_required
@deleteLog('boss_potential_customers')
def deletePotentialCustomers():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(PotentialCustomers, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addPotentialCustomers", methods=["POST"])
@jwt_required
@addLog('boss_potential_customers')
def addPotentialCustomers():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    serviceId = dataDict.get("serviceId", None)
    customerName = dataDict.get("customerName", None)
    address = dataDict.get("address", None)
    contactPerson = dataDict.get("contactPerson", None)
    contactPhone = dataDict.get("contactPhone", None)
    require = dataDict.get("require", None)
    excelPath = dataDict.get("excelPath", None)
    companyScope = dataDict.get("companyScope", None)
    registeredCapital = dataDict.get("registeredCapital", None)
    isChoose = dataDict.get("isChoose", None)
    sourceType = dataDict.get("sourceType", None)
    createPerson = dataDict.get("createPerson", None)
    createTime = dataDict.get("createTime", None)
    columsStr = (
        serviceId, customerName, address, contactPerson, contactPhone, require, excelPath, companyScope,
        registeredCapital,
        isChoose, sourceType, createPerson, createTime)
    table = insertToSQL(PotentialCustomers, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataPotentialCustomers", methods=["POST"])
@jwt_required
@updateLog('boss_potential_customers')
def updataPotentialCustomers():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(PotentialCustomers, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

# 剔除

# 筛选
@app.route("/eliminateCustomes", methods=["POST"])
@jwt_required
def eliminateCustomes():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get('ids', "")
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    newDict = {"isChoose": -1}
    otherNum = 0
    failNum = 0
    successNum = 0
    for id in idList:
        table = findById(PotentialCustomers, "id", id)
        if not table:
            failNum += 1
            continue
        if table.create_person:
            otherNum += 1
            continue
        table = updataById(PotentialCustomers, newDict, "id", id, tableChangeDic, intList)
        if not table:
            failNum += 1
        else:
            successNum += 1
    resultDict = returnMsg({"success": successNum, "fail": failNum, "otherPerson": otherNum})
    return jsonify(resultDict)


# 筛选
@app.route("/filterCustomes", methods=["POST"])
@jwt_required
def filterCustomes():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get('ids', "")
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    newDict = {"isChoose": 1}
    otherNum = 0
    failNum = 0
    successNum = 0
    for id in idList:
        table = findById(PotentialCustomers, "id", id)
        if not table:
            failNum += 1
            continue
        if table.create_person:
            otherNum += 1
            continue
        serviceId = table.service_id
        orderNo = None
        serviceNo = None
        productName = table.customer_name
        require = table.require
        projectPath = table.excel_path
        projectType = 1
        customerName = table.customer_name
        executePerson = None
        executeTime = None
        createPerson = current_user.admin_name
        createTime = getTimeStrfTimeStampNow()
        isSend = 0
        isDone = 0
        remark = None
        chooseType = 0  # 1 无需求 2 战略 3 单项
        sourceType = 1
        CommunicateStr = (
            serviceId, orderNo, serviceNo, productName, require, projectPath, projectType, customerName, executePerson,
            executeTime, createPerson, createTime, isSend, isDone, remark, chooseType, sourceType)

        CommunicateTable = insertToSQL(Communicate, *CommunicateStr)
        if not CommunicateTable:
            resultDict = returnErrorMsg(errorCode["insert_fail"])
            return jsonify(resultDict)
        table = updataById(PotentialCustomers, newDict, "id", id, tableChangeDic, intList)
        if not table:
            failNum += 1
        else:
            successNum += 1
    resultDict = returnMsg({"success": successNum, "fail": failNum, "otherPerson": otherNum})
    return jsonify(resultDict)


def tableSort(table):
    _infoDict = {
        "id": table.id,
        "serviceId": table.service_id,
        "customerName": table.customer_name,
        "address": table.address,
        "contactPerson": table.contact_person,
        "contactPhone": table.contact_phone,
        "require": table.require,
        "excelPath": table.excel_path,
        "companyScope": table.company_scope,
        "registeredCapital": table.registered_capital,
        "isChoose": table.is_choose,
        "sourceType": table.source_type,
        "createPerson": table.create_person,
        "createTime": table.create_time, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {
        "id": tableData[0],
        "serviceId": tableData[1],
        "customerName": tableData[2],
        "address": tableData[3],
        "contactPerson": tableData[4],
        "contactPhone": tableData[5],
        "require": tableData[6],
        "excelPath": tableData[7],
        "companyScope": tableData[8],
        "registeredCapital": tableData[9],
        "isChoose": tableData[10],
        "sourceType": tableData[11],
        "createPerson": tableData[12],
        "createTime": tableData[13], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict
