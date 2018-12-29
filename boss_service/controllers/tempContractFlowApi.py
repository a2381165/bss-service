#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 0017 10:48
# @Site    : 
# @File    : tempContractFlowApi.py
# @Software: PyCharm

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, current_user
from common.FlowCommon import getFlowSort
import Res
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FlowCommon import sendUp, returnUp
from common.FormatStr import dictRemoveNone
from common.Log import addLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteByIdBoss
from common.OperationOfDB import insertToSQL
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from common.listMysql import getRolePersonFlow
from models.Data.Aidance import Aidance
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic, intList as aidanceCheckIntList
from models.Data.MemberTempContract import MemberTempContractChangeDic, MemberTempContract
from models.Data.SubFlow import SubFlow
from version.v3.bossConfig import app
from models.Boss.Communicate import Communicate
from models.Order.UserOrder import UserOrder


# 商务经理 添加
@app.route("/addMemberTempContract", methods=["POST"])
@jwt_required
@addLog('data_member_temp_contract')
def addMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskId = None
    orderNo = None
    serviceNo = None
    contractNo = None
    contractName = dataDict.get("contractName", None)
    contractRemark = dataDict.get("contractRemark", None)
    productName = dataDict.get("productName", None)
    contractPrice = dataDict.get("contractPrice", None)
    startFee = dataDict.get("startFee", None)
    projectFee = 0
    projectRate = dataDict.get("projectRate", None)
    contractType = dataDict.get("contractType", None)
    startTime = dataDict.get("startTime", None)
    endTime = dataDict.get("endTime", None)
    createPerson = current_user.admin_name
    createTime = getTimeStrfTimeStampNow()
    executePerson = None
    executeTime = None
    isDone = 0
    if not (contractPrice or projectRate):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    columsStr = (
        taskId, orderNo, serviceNo, contractNo, contractName, contractRemark, productName, contractPrice, startFee,
        projectFee, projectRate, contractType, startTime, endTime, createPerson, createTime, executePerson, executeTime,
        isDone)
    table = insertToSQL(MemberTempContract, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 商务经理 删除
@app.route("/deleteMemberTempContract", methods=["POST"])
@jwt_required
def deleteMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    success = 0
    fail = 0
    for id in idList:
        table = findById(MemberTempContract, "id", id)
        if not table and table.create_person != current_user.admin_name:
            fail += 1
            continue
        count = deleteByIdBoss(table, [id], "id")
        if count == 1:
            success += 1
        else:
            fail += 1
    resultDict = returnMsg({"success": success, "fail": fail})
    return jsonify(resultDict)


# 商务经理  发起者 合同列表
@app.route("/findInitiatorMembertempContractByCondition", methods=["POST"])
@jwt_required
def findInitiatorMembertempContractByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [{
        "field": "createPerson",
        "op": "equal",
        "value": current_user.admin_name
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = MemberTempContract.__tablename__
    orderByStr = " order by create_time desc "
    intColumnClinetNameList = [u'id', u'productName', u'projectRate', u'contractType', u'isDone']
    tableList, count = conditionDataListFind(dataDict, MemberTempContractChangeDic, intColumnClinetNameList, tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {
                "id": tableData[0],
                "taskId": tableData[1],
                "orderNo": tableData[2],
                "serviceNo": tableData[3],
                "contractNo": tableData[4],
                "contractName": tableData[5],
                "contractRemark": tableData[6],
                "productName": tableData[7],
                "contractPrice": tableData[8],
                "startFee": tableData[9],
                "projectFee": tableData[10],
                "projectRate": tableData[11],
                "contractType": tableData[12],
                "startTime": tableData[13],
                "endTime": tableData[14],
                "createPerson": tableData[15],
                "createTime": tableData[16],
                "executePerson": tableData[17],
                "executeTime": tableData[18],
                "isDone": tableData[19], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


#  商务合同 转移给其他商务经理
@app.route("/memberTransferOtherPerson", methods=["POST"])
@jwt_required
def memberTransferOtherPerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    createPerson = dataDict.get("createPerson", "")
    if not (idList and createPerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.updateThis(MemberTempContract, MemberTempContract.id, id, dataDict,
                                       MemberTempContractChangeDic)
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


# 商务经理送审  # 上报
@app.route("/updataUpMemberContractAidanceCheckStatus", methods=["POST"])
@jwt_required
def updataUpMemberContractAidanceCheckStatus():
    """
    :return:
    """
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")  # 单项服务id
    roleId = dataDict.get("roleId", "")
    choicePerson = dataDict.get("choicePerson", "")
    if not (idList and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = findById(MemberTempContract, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        reslut = sendUp(table, choicePerson, dbOperation, flowId=Res.workFlow["htlc"], taskType=1)
        if not reslut:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)

    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 更新 完善 并上报
@app.route("/updataMemberTempContract", methods=["POST"])
@jwt_required
@updateLog('data_member_temp_contract')
def updataMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get('checkStatus', "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.has_key("checkStatus"):
        dataDict.pop("checkStatus")
    dbOperation = OperationOfDB()
    table = dbOperation.updateThis(MemberTempContract, MemberTempContract.id, id, dataDict, MemberTempContractChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if checkStatus == 2:
        reslut = sendUp(table, None, dbOperation, flowId=Res.workFlow["htlc"], taskType=2)
        if not reslut:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 退回 重新上报
@app.route("/updataUpReturnMemberTempContract", methods=["POST"])
@jwt_required
def updataUpReturnMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus")
    choicePerson = dataDict.get("choicePerson", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["contractNo", "contractPrice", "choicePerson", "checkStatus"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    dbOperation = OperationOfDB()
    aidanceTable = findById(Aidance, "id", id)
    if not aidanceTable:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    serviceId = aidanceTable.service_id
    table = dbOperation.updateThis(MemberTempContract, MemberTempContract.id, serviceId, dataDict,
                                   MemberTempContractChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["update_fail"])
        return jsonify(resultDict)
    if checkStatus == 2:
        if not returnUp(aidanceTable, table, dbOperation, choicePerson):
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    # now = getTimeStrfTimeStampNow()
    # table = dbOperation.updateThis(MemberTempContract, MemberTempContract.id, id, dataDict, MemberTempContractChangeDic)
    # if not table:
    #     dbOperation.commitRollback()
    #     resultDict = returnErrorMsg(errorCode["update_fail"])
    #     return jsonify(resultDict)
    # aidanceId = table.task_id
    # aidanceTable = findById(Aidance, "id", aidanceId)
    # flowId = aidanceTable.flow_id
    # # 获取上一级管理人
    # if choicePerson:
    #     checkPerson = choicePerson
    # else:
    #     checkPerson = getRolePersonFlow(flowId, dbOperation)
    # if checkPerson is None:
    #     return None
    # # 添加 新的审核表 # 跟着步骤查询
    # flowStep = 1
    # aidanceStr = (aidanceId, now, current_user.admin_name, 1, None, checkPerson, None, flowStep)
    # tableCheck = dbOperation.insertToSQL(AidanceCheck, *aidanceStr)
    # if not tableCheck:
    #     dbOperation.commitRollback()
    #     resultDict = returnErrorMsg(errorCode["insert_fail"])
    #     return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 退回 上报
@app.route("/sendUpReturnMemberTempContract", methods=["POST"])
@jwt_required
def sendUpReturnMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    choicePerson = dataDict.get("choicePerson", "")
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if choicePerson:
        dataDict.pop("choicePerson")

    dbOperation = OperationOfDB()
    for id in idList:
        aidanceTable = findById(Aidance, "id", id)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        serviceId = aidanceTable.service_id
        table = findById(MemberTempContract, "id", serviceId)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        result = returnUp(aidanceTable, table, dbOperation, choicePerson)
        if not result:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 审核流程 NewAidanceApi.py | checkAidanceCheck


# 合同中间人 列表
@app.route("/findMemberContractAidanceByCondition", methods=["POST"])
@jwt_required
def findMemberContractAidanceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["htlc"]
    sort = getFlowSort(flowId, roleId)
    if not sort:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # 传入 flowId and checkStatus
    newDictList = [{
        "field": "checkPerson",
        "op": "equal",
        "value": current_user.admin_name
    }, {
        "field": "sort",
        "op": "equal",
        "value": sort
    }]
    for newDict in newDictList:
        condition.append(newDict)
    tableName = "view_aidance_check_member_temp_contract"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_member_contract_task_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_check_flow_member_temp_contract_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 合同 发起者 已退回列表
@app.route("/findFirstMemberContractAidanceByCondition", methods=["POST"])
@jwt_required
def findFirstMemberContractAidanceByCondition():
    """
    checkStatus = 3
    :return:
    """
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    # 传入 flowId and checkStatus
    newDictList = [{
        "field": "createPerson",
        "op": "equal",
        "value": current_user.admin_name
    }]
    for newDict in newDictList:
        condition.append(newDict)
    tableName = "view_aidance_check_flow_member_temp_contract"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', 'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_member_contract_task_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_check_flow_member_temp_contract_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 总经理同意
@app.route("/finallyCheckMemberContract", methods=["POST"])
@jwt_required
def finallyCheckMemberContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus", "")
    if not (id and checkStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.has_key("roleId"):
        dataDict.pop("roleId")
    aidanceTable = findById(Aidance, "id", id)
    if not aidanceTable:
        resultDict = returnErrorMsg(errorCode["query_fail"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    now = getTimeStrfTimeStampNow()
    if checkStatus == Res.AuditCode["pass"]:
        # 更新 aidance
        aidanceTable.accept_status = 1
        aidanceTable.execute_person = current_user.admin_name
        aidanceTable.is_done = 2
        aidanceTable.complete_time = now
        aidanceTable.flow_step += 1
        aidanceTable = dbOperation.addTokenToSql(aidanceTable)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        serviceId = aidanceTable.service_id
        # 更新 明细
        serviceTable = dbOperation.findById(MemberTempContract, "id", serviceId)
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceTable.is_done = 2
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        # 生成 沟通
        orderNo = serviceTable.order_no
        orderInfo = findById(UserOrder, "order_no", orderNo, isStrcheck=True)
        comServiceId = orderInfo.service_id
        serviceNo = serviceTable.service_no
        productName = serviceTable.product_name
        require = serviceTable.contract_name
        projectPath = None
        projectType = 1
        customerName = orderInfo.contact_person
        executePerson = serviceTable.create_person
        createPerson = serviceTable.create_person
        executeTime = getTimeStrfTimeStampNow()
        createTime = getTimeStrfTimeStampNow()
        isDone = 1
        isSend = 0  # 自创
        chosoType = 0
        sourceType = 6  # 商务副部长自创
        remark = None
        CommunicateStr = (
            comServiceId, orderNo, serviceNo, productName, require, projectPath, projectType, customerName,
            executePerson,
            executeTime,
            createPerson, createTime,
            isSend, isDone, remark, chosoType, sourceType)
        communicateInfo = dbOperation.insertToSQL(Communicate, *CommunicateStr)
        if not communicateInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
    elif checkStatus == Res.AuditCode["fail"]:
        aidanceTable.flow_step = 1
        aidanceTable = dbOperation.addTokenToSql(aidanceTable)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    checkId = aidanceTable.check_id
    intColumnClinetNameList = aidanceCheckIntList
    checkInfo = dbOperation.updateThis(AidanceCheck, AidanceCheck.id, checkId, dataDict, AidanceCheckChangeDic,
                                       intColumnClinetNameList=intColumnClinetNameList)
    if not checkInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["update_fail"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)





# 总经理 同意
@app.route("/acceptMemberTempContract", methods=["POST"])
@jwt_required
def acceptMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus", "")
    if not (id and checkStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    if checkStatus == Res.AuditCode["pass"]:
        # 更新任务
        # 更新明细
        # 更细审核
        pass
    elif checkStatus == Res.AuditCode["fail"]:
        # 更新审核
        # 更新步骤为1  商务经理 重新修改
        pass
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


def view_aidance_check_flow_member_temp_contract_fun(tableData):
    _infoDict = {
        "id": tableData[0],
        "customerName": tableData[1],
        "createReason": tableData[2],
        "createRealName": tableData[3],
        "createTime": tableData[4],
        "flowId": tableData[5],
        "remark": tableData[6],
        "executePerson": tableData[7],
        "createPerson": tableData[8],
        "completeTime": tableData[9],
        "checkId": tableData[10],
        "fromId": tableData[11],
        "serviceId": tableData[12],
        "flowStep": tableData[13],
        "acceptStatus": tableData[14],
        "isDone": tableData[15],
        "taskType": tableData[16],
        "submitTime": tableData[17],
        "submitPerson": tableData[18],
        "checkStatus": tableData[19],
        "checkTime": tableData[20],
        "checkPerson": tableData[21],
        "checkRemark": tableData[22],
        "sort": tableData[23],
        "name": tableData[24],
        "desc": tableData[25],
        "num": tableData[26],
        "orderNo": tableData[27],
        "serviceNo": tableData[28],
        "contractNo": tableData[29],
        "contractName": tableData[30],
        "contractRemark": tableData[31],
        "productName": tableData[32],
        "contractPrice": tableData[33],
        "startFee": tableData[34],
        "projectFee": tableData[35],
        "projectRate": tableData[36],
        "contractType": tableData[37],
        "startTime": tableData[38],
        "endTime": tableData[39],
    }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_aidance_member_contract_task_change = {
    "id": "id",
    "customerName": "customer_name",
    "createReason": "create_reason",
    "createRealName": "create_real_name",
    "createTime": "create_time",
    "flowId": "flow_id",
    "remark": "remark",
    "executePerson": "execute_person",
    "createPerson": "create_person",
    "completeTime": "complete_time",
    "checkId": "check_id",
    "fromId": "from_id",
    "serviceId": "service_id",
    "flowStep": "flow_step",
    "acceptStatus": "accept_status",
    "isDone": "is_done",
    "taskType": "task_type",
    "submitTime": "submit_time",
    "submitPerson": "submit_person",
    "checkStatus": "check_status",
    "checkTime": "check_time",
    "checkPerson": "check_person",
    "checkRemark": "check_remark",
    "sort": "sort",
    "name": "name",
    "desc": "desc",
    "num": "num",
    "orderNo": "order_no",
    "serviceNo": "service_no",
    "contractNo": "contract_no",
    "contractName": "contract_name",
    "contractRemark": "contract_remark",
    "productName": "product_name",
    "contractPrice": "contract_price",
    "startFee": "start_fee",
    "projectFee": "project_fee",
    "projectRate": "project_rate",
    "contractType": "contract_type",
    "startTime": "start_time",
    "endTime": "end_time",
}
