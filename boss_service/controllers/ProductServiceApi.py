# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Data.ProductService import ProductService, ProductServiceChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取 列表
@app.route("/findProductServiceByCondition", methods=["POST"])
@jwt_required
@queryLog('data_product_service')
def findProductServiceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = ProductService.__tablename__
    intColumnClinetNameList = intList
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
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
@app.route("/getProductServiceDetail", methods=["POST"])
@jwt_required
@queryLog('data_product_service')
def getProductServiceDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(ProductService, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteProductService", methods=["POST"])
@jwt_required
@deleteLog('data_product_service')
def deleteProductService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(ProductService, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addProductService", methods=["POST"])
@jwt_required
@addLog('data_product_service')
def addProductService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    productName = dataDict.get("productName", None)
    productDesc = dataDict.get("productDesc", None)
    productOrigin = dataDict.get("productOrigin", None)
    createTime = dataDict.get("createTime", None)
    createPerson = dataDict.get("createPerson", None)
    isLock = dataDict.get("isLock", None)
    serviceProcess = dataDict.get("serviceProcess", None)
    serviceContent = dataDict.get("serviceContent", None)
    servicePrice = dataDict.get("servicePrice", None)
    columsStr = (
        productName, productDesc, productOrigin, createTime, createPerson, isLock, serviceProcess, serviceContent,
        servicePrice)
    table = insertToSQL(ProductService, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataProductService", methods=["POST"])
@jwt_required
@updateLog('data_product_service')
def updataProductService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(ProductService, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


def tableSort(table):
    _infoDict = {
        "id": table.id,
        "productName": table.product_name,
        "productDesc": table.product_desc,
        "productOrigin": table.product_origin,
        "createTime": table.create_time,
        "createPerson": table.create_person,
        "isLock": table.is_lock,
        "serviceProcess": table.service_process,
        "serviceContent": table.service_content,
        "servicePrice": table.service_price, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {
        "id": tableData[0],
        "productName": tableData[1],
        "productDesc": tableData[2],
        "productOrigin": tableData[3],
        "createTime": tableData[4],
        "createPerson": tableData[5],
        "isLock": tableData[6],
        "serviceProcess": tableData[7],
        "serviceContent": tableData[8],
        "servicePrice": tableData[9], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict
