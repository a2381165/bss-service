# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Zzh.MemberEnterpriseContactInfoCheck import MemberEnterpriseContactInfoCheck, tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取 列表
@app.route("/findMemberEnterpriseContactInfoCheckByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_member_enterprise_contact_info_check')
def findMemberEnterpriseContactInfoCheckByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = MemberEnterpriseContactInfoCheck.__tablename__
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
@app.route("/getMemberEnterpriseContactInfoCheckDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_member_enterprise_contact_info_check')
def getMemberEnterpriseContactInfoCheckDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(MemberEnterpriseContactInfoCheck, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteMemberEnterpriseContactInfoCheck", methods=["POST"])
@jwt_required
@deleteLog('zzh_member_enterprise_contact_info_check')
def deleteMemberEnterpriseContactInfoCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(MemberEnterpriseContactInfoCheck, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addMemberEnterpriseContactInfoCheck", methods=["POST"])
@jwt_required
@addLog('zzh_member_enterprise_contact_info_check')
def addMemberEnterpriseContactInfoCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    enterpriseId = dataDict.get("enterpriseId", None)
    contractPerson = dataDict.get("contractPerson", None)
    contractPhone = dataDict.get("contractPhone", None)
    contractDuty = dataDict.get("contractDuty", None)
    contractEmail = dataDict.get("contractEmail", None)
    contractWeixin = dataDict.get("contractWeixin", None)
    auditPerson = dataDict.get("auditPerson", None)
    auditTime = dataDict.get("auditTime", None)
    auditStatus = dataDict.get("auditStatus", None)
    auditRemark = dataDict.get("auditRemark", None)
    checkMemberType = dataDict.get("checkMemberType", None)
    manageId = dataDict.get("manageId", None)
    columsStr = (
    enterpriseId, contractPerson, contractPhone, contractDuty, contractEmail, contractWeixin, auditPerson, auditTime,
    auditStatus, auditRemark, checkMemberType, manageId)
    table = insertToSQL(MemberEnterpriseContactInfoCheck, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataMemberEnterpriseContactInfoCheck", methods=["POST"])
@jwt_required
@updateLog('zzh_member_enterprise_contact_info_check')
def updataMemberEnterpriseContactInfoCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(MemberEnterpriseContactInfoCheck, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


def tableSort(table):
    _infoDict = {"id": table.id,
                 "enterpriseId": table.enterprise_id,
                 "contractPerson": table.contract_person,
                 "contractPhone": table.contract_phone,
                 "contractDuty": table.contract_duty,
                 "contractEmail": table.contract_email,
                 "contractWeixin": table.contract_weixin,
                 "auditPerson": table.audit_person,
                 "auditTime": table.audit_time,
                 "auditStatus": table.audit_status,
                 "auditRemark": table.audit_remark,
                 "checkMemberType": table.check_member_type,
                 "manageId": table.manage_id, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "enterpriseId": tableData[1],
                 "contractPerson": tableData[2],
                 "contractPhone": tableData[3],
                 "contractDuty": tableData[4],
                 "contractEmail": tableData[5],
                 "contractWeixin": tableData[6],
                 "auditPerson": tableData[7],
                 "auditTime": tableData[8],
                 "auditStatus": tableData[9],
                 "auditRemark": tableData[10],
                 "checkMemberType": tableData[11],
                 "manageId": tableData[12], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict
