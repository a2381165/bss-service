# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Boss.EditSettlement import EditSettlement, EditSettlementChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
import Res
from models.Data.SubFlow import SubFlow
from common.FlowCommon import sendUp, returnUp
from models.Data.Aidance import Aidance
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic, intList as aidanceCheckIntList
from common.FlowCommon import getFlowSort


# 添加
@app.route("/addEditSettlement", methods=["POST"])
@jwt_required
def addEditSettlement():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskId = dataDict.get("taskId", None)
    counselorId = dataDict.get("counselorId", None)
    customerName = dataDict.get("customerName", None)
    projectName = dataDict.get("projectName", None)
    declarationLimit = dataDict.get("declarationLimit", None)
    declarationPlan = dataDict.get("declarationPlan", None)
    editFee = dataDict.get("editFee", None)
    acceptFee = dataDict.get("acceptFee", None)
    royaltyBase = dataDict.get("royaltyBase", None)
    royaltyRatio = dataDict.get("royaltyRatio", None)
    projectRoyalty = dataDict.get("projectRoyalty", None)
    actualPayment = dataDict.get("actualPayment", None)
    projectStatus = dataDict.get("projectStatus", None)
    remark = dataDict.get("remark", None)
    createPerson = dataDict.get("createPerson", None)
    createTime = dataDict.get("createTime", None)
    executePerson = dataDict.get("executePerson", None)
    executeTime = dataDict.get("executeTime", None)
    isDone = dataDict.get("isDone", None)
    executeDone = dataDict.get("executeDone", None)
    columsStr = (taskId, counselorId, customerName, projectName, declarationLimit, declarationPlan, editFee, acceptFee,
                 royaltyBase, royaltyRatio, projectRoyalty, actualPayment, projectStatus, remark, createPerson,
                 createTime,
                 executePerson, executeTime, isDone, executeDone)
    table = insertToSQL(EditSettlement, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 获取详情
@app.route("/getEditSettlementDetail", methods=["POST"])
@jwt_required
def getEditSettlementDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(EditSettlement, "id", id)
    if not table:
        resultDict = returnErrorMsg(errorCode["query_fail"])
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 商务经理 渠道商列表 待上报 已上报 已成功
@app.route("/findEditSettlementByCondition", methods=["POST"])
@jwt_required
def findEditSettlementByCondition():
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
    tablename = EditSettlement.__tablename__
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


# 商务经理 被退回 列表
@app.route("/findViewInnerEditSettlementByCondition", methods=["POST"])
@jwt_required
def findViewInnerEditSettlementByCondition():
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
    tablename = "view_aidance_check_edit_settlement"  # view_aidance_check_channel_user
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_aidance_check_flow_boss_edit_settlement_change,
                                             intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = view_aidance_check_flow_boss_edit_settlement_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 合同中间人 列表
@app.route("/findViewEditSettlementByCondition", methods=["POST"])
@jwt_required
def findViewEditSettlementByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["xmjssh"]
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
    tableName = "view_aidance_check_edit_settlement"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_check_flow_boss_edit_settlement_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_check_flow_boss_edit_settlement_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务经理送审  # 上报
@app.route("/updataUpEditSettlementCheckStatus", methods=["POST"])
@jwt_required
def updataUpEditSettlementCheckStatus():
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
        table = findById(EditSettlement, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        reslut = sendUp(table, choicePerson, dbOperation, flowId=Res.workFlow["xmjssh"], taskType=None)
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
@app.route("/updataEditSettlement", methods=["POST"])
@jwt_required
def updataEditSettlement():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get('checkStatus', "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    dbOperation = OperationOfDB()
    table = dbOperation.updateThis(EditSettlement, EditSettlement.id, id, dataDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if checkStatus == 2:
        reslut = sendUp(table, None, dbOperation, flowId=Res.workFlow["xmjssh"], taskType=None)
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
@app.route("/updataUpReturnEditSettlement", methods=["POST"])
@jwt_required
def updataUpReturnEditSettlement():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus")
    choicePerson = dataDict.get("choicePerson", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus"]
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
    table = dbOperation.updateThis(EditSettlement, EditSettlement.id, serviceId, dataDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["update_fail"])
        return jsonify(resultDict)
    if checkStatus == 2:
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


# 退回 上报
@app.route("/sendUpReturnEditSettlement", methods=["POST"])
@jwt_required
def sendUpReturnEditSettlement():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    choicePerson = dataDict.get("choicePerson", "")
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    dbOperation = OperationOfDB()
    for id in idList:
        aidanceTable = findById(Aidance, "id", id)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceId = aidanceTable.service_id
        table = findById(EditSettlement, "id", serviceId)
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


#  商务合同 转移给其他商务经理
@app.route("/EditSettlementTransferOtherPerson", methods=["POST"])
@jwt_required
def EditSettlementTransferOtherPerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    createPerson = dataDict.get("createPerson", "")
    if not (idList and createPerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.updateThis(EditSettlement, EditSettlement.id, id, dataDict,
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


# 删除 
@app.route("/deleteEditSettlement", methods=["POST"])
@jwt_required
def deleteEditSettlement():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(EditSettlement, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 总经理同意
@app.route("/finallyCheckEditSettlement", methods=["POST"])
@jwt_required
def finallyCheckEditSettlement():
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
        serviceTable = dbOperation.findById(EditSettlement, "id", serviceId)
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceTable.is_done = 2
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)

        # communicateInfo = dbOperation.insertToSQL(Communicate, *CommunicateStr)
        # if not communicateInfo:
        #     dbOperation.commitRollback()
        #     resultDict = returnErrorMsg(errorCode["param_error"])
        #     return jsonify(resultDict)
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


# NewAidanceApi.py checkAidanceCheck

def tableSort(table):
    _infoDict = {"id": table.id,
                 "taskId": table.task_id,
                 "counselorId": table.counselor_id,
                 "customerName": table.customer_name,
                 "projectName": table.project_name,
                 "declarationLimit": table.declaration_limit,
                 "declarationPlan": table.declaration_plan,
                 "editFee": table.edit_fee,
                 "acceptFee": table.accept_fee,
                 "royaltyBase": table.royalty_base,
                 "royaltyRatio": table.royalty_ratio,
                 "projectRoyalty": table.project_royalty,
                 "actualPayment": table.actual_payment,
                 "projectStatus": table.project_status,
                 "remark": table.remark,
                 "createPerson": table.create_person,
                 "createTime": table.create_time,
                 "executePerson": table.execute_person,
                 "executeTime": table.execute_time,
                 "isDone": table.is_done,
                 "executeDone": table.execute_done, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "taskId": tableData[1],
                 "counselorId": tableData[2],
                 "customerName": tableData[3],
                 "projectName": tableData[4],
                 "declarationLimit": tableData[5],
                 "declarationPlan": tableData[6],
                 "editFee": tableData[7],
                 "acceptFee": tableData[8],
                 "royaltyBase": tableData[9],
                 "royaltyRatio": tableData[10],
                 "projectRoyalty": tableData[11],
                 "actualPayment": tableData[12],
                 "projectStatus": tableData[13],
                 "remark": tableData[14],
                 "createPerson": tableData[15],
                 "createTime": tableData[16],
                 "executePerson": tableData[17],
                 "executeTime": tableData[18],
                 "isDone": tableData[19],
                 "executeDone": tableData[20], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def view_aidance_check_flow_boss_edit_settlement_fun(tableData):
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
        "counselorId": tableData[27],
        "editCustomerName": tableData[28],
        "projectName": tableData[29],
        "declarationLimit": tableData[30],
        "declarationPlan": tableData[31],
        "editFee": tableData[32],
        "acceptFee": tableData[33],
        "royaltyBase": tableData[34],
        "royaltyRatio": tableData[35],
        "projectRoyalty": tableData[36],
        "actualPayment": tableData[37],
        "projectStatus": tableData[38],
        "editRemark": tableData[39], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_aidance_check_flow_boss_edit_settlement_change = {
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
    "counselorId": "counselor_id",
    "editCustomerName": "edit_customer_name",
    "projectName": "project_name",
    "declarationLimit": "declaration_limit",
    "declarationPlan": "declaration_plan",
    "editFee": "edit_fee",
    "acceptFee": "accept_fee",
    "royaltyBase": "royalty_base",
    "royaltyRatio": "royalty_ratio",
    "projectRoyalty": "project_royalty",
    "actualPayment": "actual_payment",
    "projectStatus": "project_status",
    "editRemark": "edit_remark", }
