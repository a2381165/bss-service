# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Member.MemberEnterpriseCertificationCheck import MemberEnterpriseCertificationCheck, \
    MemberEnterpriseCertificationCheckChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
from models.Member.MemberBases import MemberBases
from models.Member.MemberEnterpriseCertification import MemberEnterpriseCertification, \
    MemberEnterpriseCertificationChangeDic


# 获取 列表
@app.route("/findMemberEnterpriseCertificationCheckByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_member_enterprise_certification_check')
def findMemberEnterpriseCertificationCheckByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = MemberEnterpriseCertificationCheck.__tablename__
    intColumnClinetNameList = intList
    orderByStr = " order by audit_time desc "
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
@app.route("/getMemberEnterpriseCertificationCheckDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_member_enterprise_certification_check')
def getMemberEnterpriseCertificationCheckDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(MemberEnterpriseCertificationCheck, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除
@app.route("/deleteMemberEnterpriseCertificationCheck", methods=["POST"])
@jwt_required
@deleteLog('zzh_member_enterprise_certification_check')
def deleteMemberEnterpriseCertificationCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(MemberEnterpriseCertificationCheck, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addMemberEnterpriseCertificationCheck", methods=["POST"])
@jwt_required
@addLog('zzh_member_enterprise_certification_check')
def addMemberEnterpriseCertificationCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    memberId = dataDict.get("memberId", None)
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
    auditPerson = dataDict.get("auditPerson", None)
    auditTime = dataDict.get("auditTime", None)
    auditStatus = dataDict.get("auditStatus", None)
    auditRemark = dataDict.get("auditRemark", None)
    checkMemberType = dataDict.get("checkMemberType", None)
    memberEnterpriseId = dataDict.get("memberEnterpriseId", None)
    manageId = dataDict.get("manageId", None)
    columsStr = (id, memberId, memberName, memberUnitType, memberCreditCode, memberCreditUrl, memberLegalPerson,
                 memberRegisteredCapital, memberRegisteredAddress, memberFoundDate, memberBusinessScope,
                 memberMailingAddress, auditPerson, auditTime, auditStatus, auditRemark, checkMemberType,
                 memberEnterpriseId, manageId)
    table = insertToSQL(MemberEnterpriseCertificationCheck, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新
@app.route("/updataMemberEnterpriseCertificationCheck", methods=["POST"])
@jwt_required
@updateLog('zzh_member_enterprise_certification_check')
def updataMemberEnterpriseCertificationCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(MemberEnterpriseCertificationCheck, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 审核
@app.route("/checkMemberEnterpriseCertificationCheck", methods=["POST"])
@jwt_required
def checkMemberEnterpriseCertificationCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("auditStatus", "")
    if not (id and checkStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dataDict["auditPerson"] = current_user.admin_name
    dataDict["auditTime"] = getTimeStrfTimeStampNow()

    dbOperation = OperationOfDB()
    table = findById(MemberEnterpriseCertificationCheck, "id", id)
    if not table:
        resultDict = returnErrorMsg(errorCode["query_fail"])
        return jsonify(resultDict)
    if checkStatus == 2:
        # 线上
        if table.member_id != 0:
            userInfo = findById(MemberBases, "user_id", table.member_id)
            if userInfo:
                if userInfo.enterprise_id:
                    # 更新
                    updateOrAdd = "update"
                else:
                    # 新增
                    updateOrAdd = "add"
            else:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["query_fail"])
                return jsonify(resultDict)
        # 线下
        elif table.member_id == 0 or table.member_id == None:
            if table.member_enterprise_id:
                # 更新
                updateOrAdd = "update"
            elif table.member_enterprise_id == 0:
                # 新增
                updateOrAdd = "add"
            else:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["query_fail"])
                return jsonify(resultDict)
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
    elif checkStatus == 3:
        # 更新企业check
        updateOrAdd = None
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if updateOrAdd == "update":
        memberInfo = findById(MemberEnterpriseCertification, "id", table.member_enterprise_id)
        memberInfo.member_name = table.member_name
        memberInfo.member_unit_type = table.member_unit_type
        memberInfo.member_credit_code = table.member_credit_code
        memberInfo.member_credit_url = table.member_credit_url
        memberInfo.member_legal_person = table.member_legal_person
        memberInfo.member_registered_capital = table.member_registered_capital
        memberInfo.member_registered_address = table.member_registered_address
        memberInfo.member_found_date = table.member_found_date
        memberInfo.member_business_scope = table.member_business_scope
        memberInfo.member_mailing_address = table.member_mailing_address
        memberInfo = dbOperation.addTokenToSql(memberInfo)
        if not memberInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    elif updateOrAdd == "add":
        MemberEnterpriseCertificationStr = (
            table.member_name, table.member_unit_type, table.member_credit_code, table.member_credit_url,
            table.member_legal_person, table.member_registered_capital, table.member_registered_address,
            table.member_found_date, table.member_business_scope, table.member_mailing_address, table.manage_id)
        insertMembeTable = dbOperation.insertToSQL(MemberEnterpriseCertification, *MemberEnterpriseCertificationStr)
        if not insertMembeTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["insert_fail"])
            return jsonify(resultDict)
    table = dbOperation.updateThis(MemberEnterpriseCertificationCheck, MemberEnterpriseCertificationCheck.id, id,
                                   dataDict, tableChangeDic)
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
        "memberId": table.member_id,
        "memberName": table.member_name,
        "memberUnitType": table.member_unit_type,
        "memberCreditCode": table.member_credit_code,
        "memberCreditUrl": table.member_credit_url,
        "memberLegalPerson": table.member_legal_person,
        "memberRegisteredCapital": str(table.member_registered_capital),
        "memberRegisteredAddress": table.member_registered_address,
        "memberFoundDate": table.member_found_date,
        "memberBusinessScope": table.member_business_scope,
        "memberMailingAddress": table.member_mailing_address,
        "auditPerson": table.audit_person,
        "auditTime": table.audit_time,
        "auditStatus": table.audit_status,
        "auditRemark": table.audit_remark,
        "memberEnterpriseId": table.member_enterprise_id,
        "manageId": table.manage_id,
    }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {
        "id": tableData[0],
        "memberId": tableData[1],
        "memberName": tableData[2],
        "memberUnitType": tableData[3],
        "memberCreditCode": tableData[4],
        "memberCreditUrl": tableData[5],
        "memberLegalPerson": tableData[6],
        "memberRegisteredCapital": str(tableData[7]),
        "memberRegisteredAddress": tableData[8],
        "memberFoundDate": tableData[9],
        "memberBusinessScope": tableData[10],
        "memberMailingAddress": tableData[11],
        "auditPerson": tableData[12],
        "auditTime": tableData[13],
        "auditStatus": tableData[14],
        "auditRemark": tableData[15],
        "checkMemberType": tableData[16],
        "memberEnterpriseId": tableData[17],
        "manageId": tableData[18],
    }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict
