# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Zzh.BankPartner import BankPartner, BankPartnerChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取 列表
@app.route("/findBankPartnerByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_bank_partner')
def findBankPartnerByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = BankPartner.__tablename__
    intColumnClinetNameList = intList
    # orderByStr = " order by create_time desc "
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
@app.route("/getBankPartnerDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_bank_partner')
def getBankPartnerDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(BankPartner, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteBankPartner", methods=["POST"])
@jwt_required
@deleteLog('zzh_bank_partner')
def deleteBankPartner():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(BankPartner, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addBankPartner", methods=["POST"])
@jwt_required
@addLog('zzh_bank_partner')
def addBankPartner():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    name = dataDict.get("name", None)
    imageUrl = dataDict.get("imageUrl", None)
    intro = dataDict.get("intro", None)
    status = dataDict.get("status", 1)
    areaName = dataDict.get("areaName", None)
    remark = dataDict.get("remark", None)
    logoUrl = dataDict.get("logoUrl", None)
    sort = dataDict.get("sort", None)
    columsStr = (name, imageUrl, intro, status, areaName, remark, logoUrl, sort)
    table = insertToSQL(BankPartner, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataBankPartner", methods=["POST"])
@jwt_required
@updateLog('zzh_bank_partner')
def updataBankPartner():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(BankPartner, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 获取 列表
@app.route("/findViewBankProductByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_bank_product')
def findViewBankProductByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = "view_bank_partner_product"
    intColumnClinetNameList = intList + ['bankProductId', 'bankPartnerId', 'isSecular', 'bankProductStatus']
    # orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, viewChangeDict, intColumnClinetNameList, tablename)
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


def tableSort(table):
    _infoDict = {"id": table.id,
                 "name": table.name,
                 "imageUrl": table.image_url,
                 "intro": table.intro,
                 "status": table.status,
                 "areaName": table.area_name,
                 "remark": table.remark,
                 "logoUrl": table.logo_url,
                 "sort": table.sort, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "name": tableData[1],
                 "imageUrl": tableData[2],
                 "intro": tableData[3],
                 "status": tableData[4],
                 "areaName": tableData[5],
                 "remark": tableData[6],
                 "logoUrl": tableData[7],
                 "sort": tableData[8], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


viewChangeDict = {
    "id": "id",
    "name": "name",
    "imageUrl": "image_url",
    "intro": "intro",
    "status": "status",
    "areaName": "area_name",
    "remark": "remark",
    "logoUrl": "logo_url",
    "sort": "sort",
    "bankProductId": "bank_product_id",
    "productName": "product_name",
    "startTime": "start_time",
    "endTime": "end_time",
    "isSecular": "is_secular",
    "bankProductStatus": "bank_roduct_tatus",
    "bankProductIntro": "bank_roduct_intro",
}


def viewTableSortDict(tableData):
    _infoDict = {
        "id": tableData[0],
        "name": tableData[1],
        "imageUrl": tableData[2],
        "intro": tableData[3],
        "status": tableData[4],
        "areaName": tableData[5],
        "remark": tableData[6],
        "logoUrl": tableData[7],
        "sort": tableData[8],
        "bankProductId": tableData[9],
        "productName": tableData[10],
        "startTime": tableData[11],
        "endTime": tableData[12],
        "isSecular": tableData[13],
        "bankProductStatus": tableData[14],
        "bankProductIntro": tableData[15],
    }
