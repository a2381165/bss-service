# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate,getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById,deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.Zzh.BankProduct import BankProduct, BankProductChangeDic as tableChangeDic,intList
from common.Log import queryLog,addLog,deleteLog,updateLog



# 获取 列表 
@app.route("/findBankProductByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_bank_product')
def findBankProductByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = BankProduct.__tablename__
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
@app.route("/getBankProductDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_bank_product')
def getBankProductDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(BankProduct, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteBankProduct", methods=["POST"])
@jwt_required
@deleteLog('zzh_bank_product')
def deleteBankProduct():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(BankProduct, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)



# 添加 
@app.route("/addBankProduct", methods=["POST"])
@jwt_required
@addLog('zzh_bank_product')
def addBankProduct():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    bankPartnerId = dataDict.get("bankPartnerId", None)
    productName = dataDict.get("productName", None)
    startTime = dataDict.get("startTime", None)
    endTime = dataDict.get("endTime", None)
    isSecular = dataDict.get("isSecular", None)
    status = dataDict.get("status", 1)
    intro = dataDict.get("intro", None)
    sort = dataDict.get("sort", None)
    columsStr = (id,bankPartnerId,productName,startTime,endTime,isSecular,status,intro,sort)
    table = insertToSQL(BankProduct, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataBankProduct", methods=["POST"])
@jwt_required
@updateLog('zzh_bank_product')
def updataBankProduct():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(BankProduct, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

def tableSort(table):
    _infoDict = {"id":table.id,
                "bankPartnerId":table.bank_partner_id,
                "productName":table.product_name,
                "startTime":table.start_time,
                "endTime":table.end_time,
                "isSecular":table.is_secular,
                "status":table.status,
                "intro":table.intro,
                "sort":table.sort,}
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id":tableData[0],
                "bankPartnerId":tableData[1],
                "productName":tableData[2],
                "startTime":tableData[3],
                "endTime":tableData[4],
                "isSecular":tableData[5],
                "status":tableData[6],
                "intro":tableData[7],
                "sort":tableData[8],}
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict

