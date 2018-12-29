# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss, \
    executeSql
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Boss.ContractSettlement import ContractSettlement, ContractSettlementChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
import Res
from models.Data.SubFlow import SubFlow
from common.FlowCommon import sendUp, returnUp
from models.Boss.User import User
from models.Data.Aidance import Aidance
from common.FlowCommon import getFlowSort
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic, intList as aidanceCheckIntList

# 添加
@app.route("/addContractSettlement", methods=["POST"])
@jwt_required
@addLog('boss_contract_settlement')
def addContractSettlement():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskId = dataDict.get("taskId", None)
    enterpriseId = dataDict.get("enterpriseId", None)
    customerName = dataDict.get("customerName", None)
    contractName = dataDict.get("contractName", None)
    contractNo = dataDict.get("contractNo", None)
    contractPrice = dataDict.get("contractPrice", None)
    suggestPerson = dataDict.get("suggestPerson", None)
    suggestPrice = dataDict.get("suggestPrice", None)
    managePerson = dataDict.get("managePerson", None)
    managePrice = dataDict.get("managePrice", None)
    businessPerson = dataDict.get("businessPerson", None)
    businessPrice = dataDict.get("businessPrice", None)
    editPerson = dataDict.get("editPerson", None)
    editPrice = dataDict.get("editPrice", None)
    createPerson = dataDict.get("createPerson", None)
    createTime = dataDict.get("createTime", None)
    executePerson = dataDict.get("executePerson", None)
    executeTime = dataDict.get("executeTime", None)
    isDone = dataDict.get("isDone", None)
    columsStr = (
        taskId, enterpriseId, customerName, contractName, contractNo, contractPrice, suggestPerson, suggestPrice,
        managePerson, managePrice, businessPerson, businessPrice, editPerson, editPrice, createPerson, createTime,
        executePerson, executeTime, isDone)
    table = insertToSQL(ContractSettlement, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 商务经理 渠道商列表 待上报 已上报 已成功
@app.route("/findContractSettlementByCondition", methods=["POST"])
@jwt_required
@queryLog('channel_user_task')
def findContractSettlementByCondition():
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
    tablename = ContractSettlement.__tablename__
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            # suggestPerson = tableData[7]
            # managePerson = tableData[9]
            # businessPerson = tableData[11]
            # editPerson = tableData[13]
            # suggestInfo = findById(User, "admin_name", suggestPerson,isStrcheck=True)
            # manageInfo = findById(User, "admin_name", managePerson,isStrcheck=True)
            # businessInfo = findById(User, "admin_name", businessPerson,isStrcheck=True)
            # editInfo = findById(User, "admin_name", editPerson,isStrcheck=True)
            # suggestName = ""
            # manageName = ""
            # businessName = ""
            # editName = ""
            #
            # if suggestInfo:
            #     suggestName = suggestInfo.admin_real_name
            # if manageInfo:
            #     manageName = manageInfo.admin_real_name
            # if businessInfo:
            #     businessName = businessInfo.admin_real_name
            # if editInfo:
            #     editName = editInfo.admin_real_name
            # newDict = {
            #     "suggestName": suggestName,
            #     "manageName": manageName,
            #     "businessName": businessName,
            #     "editName": editName,
            # }
            infoDict = tableSortDict(tableData)
            # infoDict = dict(newDict, **infoDict)

            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务经理 被退回 列表
@app.route("/findViewInnerContractSettlementByCondition", methods=["POST"])
@jwt_required
def findViewInnerContractSettlementByCondition():
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
    tablename = "view_aidance_check_flow_boss_contract_settlement"  # view_aidance_check_channel_user
    intColumnClinetNameList = intList + ["checkStatus"]
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_aidance_check_contract_settlement_change,
                                             intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            # suggestPerson = tableData[32]
            # managePerson = tableData[34]
            # businessPerson = tableData[36]
            # editPerson = tableData[38]
            # suggestInfo = findById(User, "admin_name", suggestPerson,isStrcheck=True)
            # manageInfo = findById(User, "admin_name", managePerson,isStrcheck=True)
            # businessInfo = findById(User, "admin_name", businessPerson,isStrcheck=True)
            # editInfo = findById(User, "admin_name", editPerson,isStrcheck=True)
            # suggestName = ""
            # manageName = ""
            # businessName = ""
            # editName = ""
            #
            # if suggestInfo:
            #     suggestName = suggestInfo.admin_real_name
            # if manageInfo:
            #     manageName = manageInfo.admin_real_name
            # if businessInfo:
            #     businessName = businessInfo.admin_real_name
            # if editInfo:
            #     editName = editInfo.admin_real_name
            # newDict = {
            #     "suggestName": suggestName,
            #     "manageName": manageName,
            #     "businessName": businessName,
            #     "editName": editName,
            # }
            infoDict = view_aidance_check_contract_settlement_fun(tableData)
            # infoDict = dict(newDict, **infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 合同中间人 列表
@app.route("/findViewContractSettlementByCondition", methods=["POST"])
@jwt_required
def findViewContractSettlementByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["xmjssh"]
    sort = getFlowSort(flowId,roleId)
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
    tableName = "view_aidance_check_boss_contract_settlement"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_check_contract_settlement_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_check_contract_settlement_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务经理送审  # 上报
@app.route("/updataUpContractSettlementCheckStatus", methods=["POST"])
@jwt_required
def updataUpContractSettlementCheckStatus():
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
        table = findById(ContractSettlement, "id", id)
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
@app.route("/updataContractSettlement", methods=["POST"])
@jwt_required
def updataContractSettlement():
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
    table = dbOperation.updateThis(ContractSettlement, ContractSettlement.id, id, dataDict, tableChangeDic)
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
@app.route("/updataUpReturnContractSettlement", methods=["POST"])
@jwt_required
def updataUpReturnContractSettlement():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus")
    choicePerson = dataDict.get("choicePerson", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if choicePerson:
        dataDict.pop("choicePerson")
    if checkStatus:
        dataDict.pop("checkStatus")
    dbOperation = OperationOfDB()
    aidanceTable = findById(Aidance, "id", id)
    if not aidanceTable:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    serviceId = aidanceTable.service_id
    table = dbOperation.updateThis(ContractSettlement, ContractSettlement.id, serviceId, dataDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["update_fail"])
        return jsonify(resultDict)
    if checkStatus == 2:
        result = returnUp(aidanceTable,table, dbOperation, choicePerson)
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
@app.route("/sendUpReturnContractSettlement", methods=["POST"])
@jwt_required
def sendUpReturnContractSettlement():
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
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceId = aidanceTable.service_id
        table = findById(ContractSettlement, "id", serviceId)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        result = returnUp(aidanceTable,table, dbOperation, choicePerson)
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
@app.route("/ContractSettlementTransferOtherPerson", methods=["POST"])
@jwt_required
def ContractSettlementTransferOtherPerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    createPerson = dataDict.get("createPerson", "")
    if not (idList and createPerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.updateThis(ContractSettlement, ContractSettlement.id, id, dataDict,
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
@app.route("/deleteContractSettlement", methods=["POST"])
@jwt_required
@deleteLog('boss_contract_settlement')
def deleteContractSettlement():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(ContractSettlement, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)



# 总经理同意
@app.route("/finallyCheckContractSettlement", methods=["POST"])
@jwt_required
def finallyCheckContractSettlement():
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
        serviceTable = dbOperation.findById(ContractSettlement, "id", serviceId)
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
                 "enterpriseId": table.enterprise_id,
                 "customerName": table.customer_name,
                 "contractName": table.contract_name,
                 "contractNo": table.contract_no,
                 "contractPrice": table.contract_price,
                 "suggestPerson": table.suggest_person,
                 "suggestPrice": table.suggest_price,
                 "managePerson": table.manage_person,
                 "managePrice": table.manage_price,
                 "businessPerson": table.business_person,
                 "businessPrice": table.business_price,
                 "editPerson": table.edit_person,
                 "editPrice": table.edit_price,
                 "createPerson": table.create_person,
                 "createTime": table.create_time,
                 "executePerson": table.execute_person,
                 "executeTime": table.execute_time,
                 "isDone": table.is_done, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "taskId": tableData[1],
                 "enterpriseId": tableData[2],
                 "customerName": tableData[3],
                 "contractName": tableData[4],
                 "contractNo": tableData[5],
                 "contractPrice": tableData[6],
                 "suggestPerson": tableData[7],
                 "suggestPrice": tableData[8],
                 "managePerson": tableData[9],
                 "managePrice": tableData[10],
                 "businessPerson": tableData[11],
                 "businessPrice": tableData[12],
                 "editPerson": tableData[13],
                 "editPrice": tableData[14],
                 "createPerson": tableData[15],
                 "createTime": tableData[16],
                 "executePerson": tableData[17],
                 "executeTime": tableData[18],
                 "isDone": tableData[19], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def view_aidance_check_contract_settlement_fun(tableData):
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
        "enterpriseId": tableData[27],
        "contractCustomerName": tableData[28],
        "contractName": tableData[29],
        "contractNo": tableData[30],
        "contractPrice": tableData[31],
        "suggestPerson": tableData[32],
        "suggestPrice": tableData[33],
        "managePerson": tableData[34],
        "managePrice": tableData[35],
        "businessPerson": tableData[36],
        "businessPrice": tableData[37],
        "editPerson": tableData[38],
        "editPrice": tableData[39], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_aidance_check_contract_settlement_change = {
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
    "enterpriseId": "enterprise_id",
    "contractCustomerName": "contract_customer_name",
    "contractName": "contract_name",
    "contractNo": "contract_no",
    "contractPrice": "contract_price",
    "suggestPerson": "suggest_person",
    "suggestPrice": "suggest_price",
    "managePerson": "manage_person",
    "managePrice": "manage_price",
    "businessPerson": "business_person",
    "businessPrice": "business_price",
    "editPerson": "edit_person",
    "editPrice": "edit_price", }
