# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Boss.ServiceFee import ServiceFee, ServiceFeeChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
import Res


# 更新
@app.route("/updataServiceFee", methods=["POST"])
@jwt_required
@updateLog('boss_service_fee')
def updataServiceFee():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    serviceFee = dataDict.get("serviceFee", "")
    serviceRate = dataDict.get("serviceRate", "")
    roleId = dataDict.get("roleId", "")
    if not (id and (serviceFee or serviceRate) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.has_key("roleId"):
        dataDict.pop("roleId")
    dataDict["updateTime"] = getTimeStrfTimeStampNow()
    isRole = 0
    isType = 0
    if serviceRate and serviceRate > 100:
        resultDict = returnErrorMsg(errorCode["rate_not_100"])
        return jsonify(resultDict)
    serviceTable = findById(ServiceFee, "id", id)
    for value in Res.roleId.values():
        if roleId in value.keys():
            isRole = 1
            if serviceTable.fee_type in value.get(roleId, []):
                isType = 1
                break
    if serviceTable.fee_status in (0, 1):
        if not (isType and isRole and roleId in ("3","4")):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        dataDict["feeStatus"] = 1
        intColumnClinetNameList = intList
        table = updataById(ServiceFee, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)
    elif  serviceTable.fee_status in (2,3):
        if not (isType and isRole and roleId == "2"):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        dataDict["feeStatus"] = 3
        intColumnClinetNameList = intList
        table = updataById(ServiceFee, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
