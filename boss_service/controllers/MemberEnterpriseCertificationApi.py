# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Member.MemberEnterpriseCertification import MemberEnterpriseCertification, \
    MemberEnterpriseCertificationChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取 列表
@app.route("/findMemberEnterpriseCertificationByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_member_enterprise_certification')
def findMemberEnterpriseCertificationByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = MemberEnterpriseCertification.__tablename__
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
@app.route("/getMemberEnterpriseCertificationDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_member_enterprise_certification')
def getMemberEnterpriseCertificationDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(MemberEnterpriseCertification, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteMemberEnterpriseCertification", methods=["POST"])
@jwt_required
@deleteLog('zzh_member_enterprise_certification')
def deleteMemberEnterpriseCertification():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(MemberEnterpriseCertification, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addMemberEnterpriseCertification", methods=["POST"])
@jwt_required
@addLog('zzh_member_enterprise_certification')
def addMemberEnterpriseCertification():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    memberName = dataDict.get("memberName", None)
    memberUnitType = dataDict.get("memberUnitType", None)
    memberCreditCode = dataDict.get("memberCreditCode", None)
    memberCreditUrl = dataDict.get("memberCreditUrl", None)
    memberLegalPerson = dataDict.get("memberLegalPerson", None)
    memberRegisteredCapital = dataDict.get("memberRegisteredCapital", None)
    memberRegisteredAddress = dataDict.get("memberRegisteredAddress", None)
    memberFoundDate = dataDict.get("memberFoundDate", None)
    memberBusinessScope = dataDict.get("memberBusinessScope", None)
    memberMailingAddress = dataDict.get("memberMailingAddress", None)
    manageId = dataDict.get("manageId", None)
    columsStr = (
        memberName, memberUnitType, memberCreditCode, memberCreditUrl, memberLegalPerson, memberRegisteredCapital,
        memberRegisteredAddress, memberFoundDate, memberBusinessScope, memberMailingAddress, manageId)
    table = insertToSQL(MemberEnterpriseCertification, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataMemberEnterpriseCertification", methods=["POST"])
@jwt_required
@updateLog('zzh_member_enterprise_certification')
def updataMemberEnterpriseCertification():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(MemberEnterpriseCertification, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 分派
@app.route("/assignMemberEnterpriseCertification", methods=["POST"])
@jwt_required
@updateLog('zzh_member_enterprise_certification')
def assignMemberEnterpriseCertification():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    manageId = dataDict.get("manageId", "")
    if not (idList and manageId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    newDict = {"manageId": manageId}
    for id in idList:
        table = dbOperation.updateThis(MemberEnterpriseCertification, MemberEnterpriseCertification.id, id, newDict,
                                       tableChangeDic)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)

    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


def tableSort(table):
    _infoDict = {
        "id": table.id,
        "memberName": table.member_name,
        "memberUnitType": table.member_unit_type,
        "memberCreditCode": table.member_credit_code,
        # "memberCreditUrl": str(table.member_credit_url),
        "memberLegalPerson": table.member_legal_person,
        "memberRegisteredCapital": str(table.member_registered_capital),
        "memberRegisteredAddress": table.member_registered_address,
        "memberFoundDate": table.member_found_date,
        "memberBusinessScope": table.member_business_scope,
        "memberMailingAddress": table.member_mailing_address,
        "manageId": table.manage_id}
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {
        "id": tableData[0],
        "memberName": tableData[1],
        "memberUnitType": tableData[2],
        "memberCreditCode": tableData[3],
        # "memberCreditUrl": str(tableData[4]),
        "memberLegalPerson": tableData[5],
        "memberRegisteredCapital": str(tableData[6]),
        "memberRegisteredAddress": tableData[7],
        "memberFoundDate": tableData[8],
        "memberBusinessScope": tableData[9],
        "memberMailingAddress": tableData[10],
        "manageId": tableData[11], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict
