# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Data.Service import Service, ServiceChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog


# 已归档查询 就是正式服务 正式项目
# 获取 列表
@app.route("/findServiceByCondition", methods=["POST"])
@jwt_required
@queryLog('data_service')
def findServiceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = Service.__tablename__
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


# 已归档查询 就是正式服务 正式项目
# 获取 列表
@app.route("/findViewServiceByCondition", methods=["POST"])
@jwt_required
@queryLog('data_service')
def findViewServiceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = "view_service_item"
    intColumnClinetNameList = intList + [u'itemId', u'levelCode', u'itemType', u'itemSort', u'isTop', u'isLock',
                                         u'isService', u'isContentJson', u'isClose', u'isSecular', "mediaType"]
    tableList, count = conditionDataListFind(dataDict, viewServiceItemChangeDict, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = tableSortDictView(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情
@app.route("/getServiceDetail", methods=["POST"])
@jwt_required
@queryLog('data_service')
def getServiceDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(Service, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除
@app.route("/deleteService", methods=["POST"])
@jwt_required
@deleteLog('data_service')
def deleteService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(Service, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addService", methods=["POST"])
@jwt_required
@addLog('data_service')
def addService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    itemId = dataDict.get("itemId", None)
    serviceName = dataDict.get("serviceName", None)
    policySource = dataDict.get("policySource", None)
    servicePrice = dataDict.get("servicePrice", None)
    serviceStarttime = dataDict.get("serviceStarttime", None)
    serviceDeadline = dataDict.get("serviceDeadline", None)
    directionName = dataDict.get("directionName", None)
    serviceContent = dataDict.get("serviceContent", None)
    sheetContent = dataDict.get("sheetContent", None)
    materialList = dataDict.get("materialList", None)
    forecastPath = dataDict.get("forecastPath", None)
    serviceContactPerson = dataDict.get("serviceContactPerson", None)
    serviceContactPhone = dataDict.get("serviceContactPhone", None)
    isSecular = dataDict.get("isSecular", None)
    isEvaluate = dataDict.get("isEvaluate", None)
    declareList = dataDict.get("declareList", None)
    createTime = dataDict.get("createTime", None)
    categoryType = dataDict.get("categoryType", None)
    servciceProcess = dataDict.get("servciceProcess", None)
    columsStr = (id, itemId, serviceName, policySource, servicePrice, serviceStarttime, serviceDeadline, directionName,
                 serviceContent, sheetContent, materialList, forecastPath, serviceContactPerson, serviceContactPhone,
                 isSecular, isEvaluate, declareList, createTime, categoryType, servciceProcess)
    table = insertToSQL(Service, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新
@app.route("/updataService", methods=["POST"])
@jwt_required
@updateLog('data_service')
def updataService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(Service, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


def tableSort(table):
    _infoDict = {"id": table.id,
                 "itemId": table.item_id,
                 "serviceName": table.service_name,
                 "policySource": table.policy_source,
                 "servicePrice": table.service_price,
                 "serviceStarttime": table.service_starttime,
                 "serviceDeadline": table.service_deadline,
                 "directionName": table.direction_name,
                 "serviceContent": table.service_content,
                 "sheetContent": table.sheet_content,
                 "materialList": table.material_list,
                 "forecastPath": table.forecast_path,
                 "serviceContactPerson": table.service_contact_person,
                 "serviceContactPhone": table.service_contact_phone,
                 "isSecular": table.is_secular,
                 "isEvaluate": table.is_evaluate,
                 "declareList": table.declare_list,
                 "createTime": table.create_time,
                 "categoryType": table.category_type,
                 "servciceProcess": table.servcice_process, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "itemId": tableData[1],
                 "serviceName": tableData[2],
                 "policySource": tableData[3],
                 "servicePrice": str(tableData[4]),
                 "serviceStarttime": tableData[5],
                 "serviceDeadline": tableData[6],
                 "directionName": tableData[7],
                 "serviceContent": tableData[8],
                 "sheetContent": tableData[9],
                 "materialList": tableData[10],
                 "forecastPath": tableData[11],
                 "serviceContactPerson": tableData[12],
                 "serviceContactPhone": tableData[13],
                 "isSecular": tableData[14],
                 "isEvaluate": tableData[15],
                 "declareList": tableData[16],
                 "createTime": tableData[17],
                 "categoryType": tableData[18],
                 "servciceProcess": tableData[19], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDictView(tableData):
    _infoDict = {"id": tableData[0],
                 "itemId": tableData[1],
                 "serviceName": tableData[2],
                 "policySource": tableData[3],
                 "servicePrice": str(tableData[4]),
                 "serviceStarttime": tableData[5],
                 "serviceDeadline": tableData[6],
                 "directionName": tableData[7],
                 "serviceContent": tableData[8],
                 "sheetContent": tableData[9],
                 "materialList": tableData[10],
                 "forecastPath": tableData[11],
                 "serviceContactPerson": tableData[12],
                 "serviceContactPhone": tableData[13],
                 "isSecular": tableData[14],
                 "isEvaluate": tableData[15],
                 "declareList": tableData[16],
                 "createTime": tableData[17],
                 "categoryType": tableData[18],
                 "servciceProcess": tableData[19],
                 "deptName": tableData[20],
                 "levelCode": tableData[21],
                 "categoryName": tableData[22],
                 "areaCode": tableData[23],
                 "itemUrl": tableData[24],
                 "itemTitle": tableData[25],
                 "itemImgurl": tableData[26],
                 "itemPulishdate": tableData[27],
                 "itemType": tableData[28],
                 "itemSort": tableData[29],
                 "isTop": tableData[30],
                 "isLock": tableData[31],
                 "isService": tableData[32],
                 "isContentJson": tableData[33],
                 "isClose": tableData[34],
                 "itemDeadline": tableData[35],
                 "mediaType": tableData[36],
                 "mediaUrl": tableData[37], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


viewServiceItemChangeDict = {
    "id": "id",
    "itemId": "item_id",
    "serviceName": "service_name",
    "policySource": "policy_source",
    "servicePrice": "service_price",
    "serviceStarttime": "service_starttime",
    "serviceDeadline": "service_deadline",
    "directionName": "direction_name",
    "serviceContent": "service_content",
    "sheetContent": "sheet_content",
    "materialList": "material_list",
    "forecastPath": "forecast_path",
    "serviceContactPerson": "service_contact_person",
    "serviceContactPhone": "service_contact_phone",
    "isSecular": "is_secular",
    "isEvaluate": "is_evaluate",
    "declareList": "declare_list",
    "createTime": "create_time",
    "categoryType": "category_type",
    "servciceProcess": "servcice_process",
    "deptName": "dept_name",
    "levelCode": "level_code",
    "categoryName": "category_name",
    "areaCode": "area_code",
    "itemUrl": "item_url",
    "itemTitle": "item_title",
    "itemImgurl": "item_imgurl",
    "itemPulishdate": "item_pulishdate",
    "itemType": "item_type",
    "itemSort": "item_sort",
    "isTop": "is_top",
    "isLock": "is_lock",
    "isService": "is_service",
    "isContentJson": "is_content_json",
    "isClose": "is_close",
    "itemDeadline": "item_deadline",
    "mediaType": "media_type",
    "mediaUrl": "media_url",
}
