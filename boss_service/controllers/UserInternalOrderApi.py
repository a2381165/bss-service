# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Order.UserInternalOrder import UserInternalOrder, UserInternalOrderChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
import Res
from models.Data.SubFlow import SubFlow
from common.FlowCommon import sendUp, returnUp
from models.Data.Aidance import Aidance
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic, intList as aidanceCheckIntList
from common.FlowCommon import getFlowSort
from models.Order.UserOrder import UserOrder


# 发起者 渠道商列表 待上报 已上报 已成功
@app.route("/findUserInternalOrderByCondition", methods=["POST"])
@jwt_required
@queryLog('channel_user_task')
def findUserInternalOrderByCondition():
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
    tablename = "view_zzh_user_internal_order_member_item"
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, viewtableSortChange, intColumnClinetNameList, tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = ViewtableSortDict(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 发起者 被退回 列表
@app.route("/findViewInnerUserInternalOrderByCondition", methods=["POST"])
@jwt_required
def findViewInnerUserInternalOrderByCondition():
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
    tablename = "view_aidance_check_user_internal_order"  # view_aidance_check_channel_user
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_aidance_check_user_internal_order_change,
                                             intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = view_aidance_check_user_internal_order_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 合同中间人 列表
@app.route("/findViewUserInternalOrderByCondition", methods=["POST"])
@jwt_required
def findViewUserInternalOrderByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["ddff"]
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
    tableName = "view_aidance_check_zzh_user_internal_order"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_check_user_internal_order_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_check_user_internal_order_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 发起者送审  # 上报
@app.route("/updataUpUserInternalOrderCheckStatus", methods=["POST"])
@jwt_required
def updataUpUserInternalOrderCheckStatus():
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
        table = findById(UserInternalOrder, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        reslut = sendUp(table, choicePerson, dbOperation, flowId=Res.workFlow["ddff"], taskType=None)
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


#  发起者 转移给其他发起者
@app.route("/UserInternalOrderTransferOtherPerson", methods=["POST"])
@jwt_required
def UserInternalOrderTransferOtherPerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    createPerson = dataDict.get("createPerson", "")
    if not (idList and createPerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    dbOperation = OperationOfDB()
    for id in idList:
        UserInternalOrderTask = findById(UserInternalOrder,"id",id)
        if not UserInternalOrderTask:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        table = findById(Aidance,"id",UserInternalOrderTask.task_id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        checkInfo = findById(AidanceCheck,"id",table.check_id)
        checkInfo.check_person = createPerson
        checkInfo = dbOperation.addTokenToSql(checkInfo)
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


# 删除 
@app.route("/deleteUserInternalOrder", methods=["POST"])
@jwt_required
@deleteLog('zzh_user_internal_order')
def deleteUserInternalOrder():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(UserInternalOrder, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 同意
@app.route("/finallyCheckUserInternalOrder", methods=["POST"])
@jwt_required
def finallyCheckUserInternalOrder():
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
        serviceTable = dbOperation.findById(UserInternalOrder, "id", serviceId)
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceTable.is_done = 2
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        # 更新月度记录表之类
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
                 "internalOrderNo": table.internal_order_no,
                 "orderNo": table.order_no,
                 "internalDeclareStatus": table.internal_declare_status,
                 "internalOrderType": table.internal_order_type,
                 "createPerson": table.create_person,
                 "createTime": table.create_time,
                 "executePerson": table.execute_person,
                 "executeTime": table.execute_time,
                 "isDone": table.is_done,
                 "closeTime": table.close_time,
                 "closePerson": table.close_person,
                 "closeReason": table.close_reason,
                 "closeType": table.close_type, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "taskId": tableData[1],
                 "internalOrderNo": tableData[2],
                 "orderNo": tableData[3],
                 "internalDeclareStatus": tableData[4],
                 "internalOrderType": tableData[5],
                 "createPerson": tableData[6],
                 "createTime": tableData[7],
                 "executePerson": tableData[8],
                 "executeTime": tableData[9],
                 "isDone": tableData[10],
                 "closeTime": tableData[11],
                 "closePerson": tableData[12],
                 "closeReason": tableData[13],
                 "closeType": tableData[14], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


viewtableSortChange = {
    "id": "id",
    "taskId": "task_id",
    "internalOrderNo": "internal_order_no",
    "orderNo": "order_no",
    "internalDeclareStatus": "internal_declare_status",
    "internalOrderType": "internal_order_type",
    "createPerson": "create_person",
    "createTime": "create_time",
    "executePerson": "execute_person",
    "executeTime": "execute_time",
    "isDone": "is_done",
    "closeTime": "close_time",
    "closePerson": "close_person",
    "closeReason": "close_reason",
    "closeType": "close_type",
    "userId": "user_id",
    "memberName": "member_name",
    "memberContactEmail": "member_contact_email",
    "memberContactPerson": "member_contact_person",
    "memberContactPhone": "member_contact_phone",
    "itemTitle": "item_title",
}


def ViewtableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "taskId": tableData[1],
                 "internalOrderNo": tableData[2],
                 "orderNo": tableData[3],
                 "internalDeclareStatus": tableData[4],
                 "internalOrderType": tableData[5],
                 "createPerson": tableData[6],
                 "createTime": tableData[7],
                 "executePerson": tableData[8],
                 "executeTime": tableData[9],
                 "isDone": tableData[10],
                 "closeTime": tableData[11],
                 "closePerson": tableData[12],
                 "closeReason": tableData[13],
                 "closeType": tableData[14],
                 "userId": tableData[15],
                 "memberName": tableData[16],
                 "memberContactEmail": tableData[17],
                 "memberContactPerson": tableData[18],
                 "memberContactPhone": tableData[19],
                 "itemTitle": tableData[20],
                 "preOrderNo": tableData[3],
                 }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def view_aidance_check_user_internal_order_fun(tableData):
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
        "internalOrderNo": tableData[27],
        "orderNo": tableData[28],
        "internalDeclareStatus": tableData[29],
        "internalOrderType": tableData[30],
        "closeTime": tableData[31],
        "closePerson": tableData[32],
        "closeReason": tableData[33],
        "closeType": tableData[34],
        "contactPerson": tableData[35],
        "contactPhone": tableData[36],
        "contactEmail": tableData[37],
        "memberName": tableData[38],
        "memberContactEmail": tableData[39],
        "memberContactPerson": tableData[40],
        "memberContactPhone": tableData[41],
        "itemTitle": tableData[42], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_aidance_check_user_internal_order_change = {
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
    "internalOrderNo": "internal_order_no",
    "orderNo": "order_no",
    "internalDeclareStatus": "internal_declare_status",
    "internalOrderType": "internal_order_type",
    "closeTime": "close_time",
    "closePerson": "close_person",
    "closeReason": "close_reason",
    "closeType": "close_type",
    "contactPerson": "contact_person",
    "contactPhone": "contact_phone",
    "contactEmail": "contact_email",
    "memberName": "member_name",
    "memberContactEmail": "member_contact_email",
    "memberContactPerson": "member_contact_person",
    "memberContactPhone": "member_contact_phone",
    "itemTitle": "item_title", }


####未用 删除####
# 添加
@app.route("/addUserInternalOrder", methods=["POST"])
@jwt_required
@addLog('zzh_user_internal_order')
def addUserInternalOrder():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskId = dataDict.get("taskId", None)
    internalOrderNo = dataDict.get("internalOrderNo", None)
    orderNo = dataDict.get("orderNo", None)
    internalDeclareStatus = dataDict.get("internalDeclareStatus", None)
    internalOrderType = dataDict.get("internalOrderType", None)
    createPerson = dataDict.get("createPerson", None)
    createTime = dataDict.get("createTime", None)
    executePerson = dataDict.get("executePerson", None)
    executeTime = dataDict.get("executeTime", None)
    isDone = dataDict.get("isDone", None)
    closeTime = dataDict.get("closeTime", None)
    closePerson = dataDict.get("closePerson", None)
    closeReason = dataDict.get("closeReason", None)
    closeType = dataDict.get("closeType", None)
    columsStr = (
        id, taskId, internalOrderNo, orderNo, internalDeclareStatus, internalOrderType, createPerson, createTime,
        executePerson, executeTime, isDone, closeTime, closePerson, closeReason, closeType)
    table = insertToSQL(UserInternalOrder, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)

# 获取详情
@app.route("/getUserInternalOrderDetail", methods=["POST"])
@jwt_required
@queryLog('data_single_service')
def getUserInternalOrderDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserInternalOrder, "id", id)
    if not table:
        resultDict = returnErrorMsg(errorCode["query_fail"])
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)



# 退回 重新上报
@app.route("/updataUpReturnUserInternalOrder", methods=["POST"])
@jwt_required
def updataUpReturnUserInternalOrder():
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
    table = dbOperation.updateThis(UserInternalOrder, UserInternalOrder.id, serviceId, dataDict, tableChangeDic)
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
@app.route("/sendUpReturnUserInternalOrder", methods=["POST"])
@jwt_required
def sendUpReturnUserInternalOrder():
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
        table = findById(UserInternalOrder, "id", serviceId)
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


# 更新 完善 并上报
@app.route("/updataUserInternalOrder", methods=["POST"])
@jwt_required
def updataUserInternalOrder():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get('checkStatus', 2)
    choicePerson = dataDict.get("choicePerson", "")
    if not (id and checkStatus and choicePerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    dbOperation = OperationOfDB()
    table = findById(UserInternalOrder, "id", id)
    orderInfo = findById(UserOrder, "order_no", table.order_no, isStrcheck=True)
    from models.Member.MemberBases import MemberBases
    memberInfo = MemberBases.query.filter(MemberBases.user_id == orderInfo.user_id).first()
    customerName = memberInfo.member_name

    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if checkStatus == 2:
        reslut = sendUp(table, choicePerson, dbOperation, flowId=Res.workFlow["ddff"], taskType=None,
                        customerName=customerName)
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