# coding:utf-8
from flask import jsonify, json, request, url_for
from flask_jwt_extended import jwt_required, current_user

import Res
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FlowCommon import getFlowSort
from common.FlowCommon import sendUp, returnUp
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog
from common.OperationOfDB import conditionDataListFind, findById, insertToSQL, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.Aidance import Aidance
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic, intList as aidanceCheckIntList
from models.Data.Transfer import Transfer
from models.Data.WholeService import WholeService, WholeServiceChangeDic as tableChangeDic, intList
from version.v3.bossConfig import app
from common.listMysql import getRolePerson
from models.Boss.User import User
from common.CreatePdf import createWholePdf

# 添加
@app.route("/addWholeService", methods=["POST"])
@jwt_required
@addLog('data_whole_service')
def addWholeService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskId = None
    serviceId = None
    customerName = dataDict.get("customerName", None)
    serviceStartTime = dataDict.get("serviceStartTime", None)
    serviceAgency = dataDict.get("serviceAgency", Res.serviceAgency)
    servicePerson = dataDict.get("servicePerson", Res.servicePerson)
    policyFinancingAdviser = dataDict.get("policyFinancingAdviser", None)
    companyProfile = dataDict.get("companyProfile", None)
    declareProject = dataDict.get("declareProject", None)
    policyService = dataDict.get("policyService", None)
    zzhService = dataDict.get("zzhService", None)
    qualificationBack = dataDict.get("qualificationBack", None)
    declareRecommend = dataDict.get("declareRecommend", None)
    declareProposal = dataDict.get("declareProposal", None)
    aidanceType = 1
    remark = dataDict.get("remark", None)
    pdfPath = dataDict.get("pdfPath", None)
    createPerson = current_user.admin_name
    createTime = getTimeStrfTimeStampNow()
    executePerson = None
    executeTime = None
    isDone = 0
    columsStr = (
        taskId, serviceId, customerName, serviceStartTime, serviceAgency, servicePerson, policyFinancingAdviser,
        companyProfile, declareProject, policyService, zzhService, qualificationBack, declareRecommend, declareProposal,
        aidanceType, remark, pdfPath, createPerson, createTime, executePerson, executeTime, isDone)
    table = insertToSQL(WholeService, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 获取详情
@app.route("/getWholeServiceDetail", methods=["POST"])
# @jwt_required
# @queryLog('data_single_service')
def getWholeServiceDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(WholeService, "id", id)
    if not table:
        resultDict = returnErrorMsg(errorCode["query_fail"])
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 商务经理 渠道商列表 待上报 已上报 已成功 findWholeServiceByCondition
@app.route("/findBusinessWholeServiceByCondition", methods=["POST"])
@jwt_required
@queryLog('channel_user_task')
def findBusinessWholeServiceByCondition():
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
    tablename = WholeService.__tablename__
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
@app.route("/findViewInnerWholeServiceByCondition", methods=["POST"])
@jwt_required
def findViewInnerWholeServiceByCondition():
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
    }, {
        "field": "flowId",
        "op": "equal",
        "value": Res.workFlow["wtZt"]
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = "view_aidance_check_flow_data_whole_service"  # view_aidance_check_channel_user
    intColumnClinetNameList = intList + ["checkStatus", "flowId"]
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_aidance_check_whole_service_change, intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = view_aidance_check_whole_service_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 合同中间人 列表
@app.route("/findViewWholeServiceByCondition", methods=["POST"])
@jwt_required
def findViewWholeServiceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["wtZt"]
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
    }, {
        "field": "flowId",
        "op": "equal",
        "value": flowId
    }]
    for newDict in newDictList:
        condition.append(newDict)
    tableName = "view_aidance_check_data_whole_service"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_check_whole_service_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_check_whole_service_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务经理送审  # 上报
@app.route("/updataUpWholeServiceCheckStatus", methods=["POST"])
@jwt_required
def updataUpWholeServiceCheckStatus():
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
        table = findById(WholeService, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        reslut = sendUp(table, choicePerson, dbOperation, flowId=Res.workFlow["wtZt"], taskType=None)
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
@app.route("/updataWholeService", methods=["POST"])
@jwt_required
def updataWholeService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get('checkStatus', "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus", "isReset"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    dbOperation = OperationOfDB()
    table = dbOperation.updateThis(WholeService, WholeService.id, id, dataDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if checkStatus == 2:
        reslut = sendUp(table, None, dbOperation, flowId=Res.workFlow["wtZt"], taskType=None)
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
@app.route("/updataUpReturnWholeService", methods=["POST"])
@jwt_required
def updataUpReturnWholeService():
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
    if dataDict.has_key("serviceStartTime") and not dataDict.get("serviceStartTime"):
        dataDict.pop("serviceStartTime")
    dbOperation = OperationOfDB()
    aidanceTable = findById(Aidance, "id", id)
    if not aidanceTable:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    aidanceTable.customer_name = dataDict.get("customerName", aidanceTable.customer_name)
    aidanceTable = dbOperation.addTokenToSql(aidanceTable)
    if not aidanceTable:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    serviceId = aidanceTable.service_id
    table = dbOperation.updateThis(WholeService, WholeService.id, serviceId, dataDict, tableChangeDic)
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
@app.route("/sendUpReturnWholeService", methods=["POST"])
@jwt_required
def sendUpReturnWholeService():
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
        table = findById(WholeService, "id", serviceId)
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
@app.route("/WholeServiceTransferOtherPerson", methods=["POST"])
@jwt_required
def WholeServiceTransferOtherPerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    createPerson = dataDict.get("createPerson", "")
    if not (idList and createPerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.updateThis(WholeService, WholeService.id, id, dataDict,
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
@app.route("/deleteWholeService", methods=["POST"])
@jwt_required
@deleteLog('data_whole_service')
def deleteWholeService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(WholeService, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


#  咨询师同意
@app.route("/finallyCheckWholeService", methods=["POST"])
@jwt_required
def finallyCheckWholeService():
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
        serviceTable = dbOperation.findById(WholeService, "id", serviceId)
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceTable.is_done = 1
        serviceTable.execute_person = current_user.admin_name
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


# 咨询师转移
@app.route("/wholeTransferOther", methods=["POST"])
@jwt_required
def wholeTransferOther():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    executePerson = dataDict.get("executePerson", "")
    reason = dataDict.get("reason", "")
    if not (executePerson and id):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.has_key("reason"):
        dataDict.pop("reason")
    intColumnClinetNameList = [u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep', u'acceptStatus',
                               u'isDone']
    dbOperation = OperationOfDB()
    # 更新aidance 执行人
    table = dbOperation.updateThis(Aidance, Aidance.id, id, dataDict, tableChangeDic,
                                   intColumnClinetNameList=intColumnClinetNameList)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["update_fail"])
        return jsonify(resultDict)
    # 更新审核人
    newDict = {"checkPerson": executePerson}
    aidanceCheckInfo = dbOperation.updateThis(AidanceCheck, AidanceCheck.id, table.check_id, newDict,
                                              AidanceCheckChangeDic)
    if not aidanceCheckInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["update_fail"])
        return jsonify(resultDict)
    # 创建记录
    now = getTimeStrfTimeStampNow()
    TransferStr = (id, current_user.admin_name, executePerson, now, reason)
    transferInfo = dbOperation.insertToSQL(Transfer, *TransferStr)
    if not transferInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["insert_fail"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 商务经理 总体服务加载
@app.route("/findWholeServiceByCondition", methods=["POST"])
@jwt_required
def findWholeServiceByCondition():
    """
       isDone 0 待上报,1 流程中,2 完成
       :return:
       """
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if not (dataDict.has_key("condition")):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newDictList = [{
        "field": "executePerson",
        "op": "equal",
        "value": current_user.admin_name
    }]
    for newDict in newDictList:
        condition.append(newDict)
    tableName = WholeService.__tablename__
    orderByStr = " order by execute_time desc"
    intColumnClinetNameList = ['id', 'serviceId', 'aidanceType', 'isDone']
    resultList, count = conditionDataListFind(dataDict, tableChangeDic,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = tableSortDict(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 更新 完善 并上报
@app.route("/updataCounselorWholeService", methods=["POST"])
@jwt_required
def updataCounselorWholeService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get('checkStatus', "")
    isReset = dataDict.get('isReset', 1)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus", "isReset"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    if dataDict.has_key("serviceStartTime") and not dataDict.get("serviceStartTime"):
        dataDict.pop("serviceStartTime")
    dbOperation = OperationOfDB()
    table = dbOperation.updateThis(WholeService, WholeService.id, id, dataDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if checkStatus == 2:
        if isReset == 1:
            reslut = sendUp(table, None, dbOperation, flowId=Res.workFlow["zxFW"], taskType=None)
            if not reslut:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["update_fail"])
                return jsonify(resultDict)
            table.is_done = 3
            table = dbOperation.addTokenToSql(table)
            if not table:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["param_error"])
                return jsonify(resultDict)
        elif isReset == 2:
            aidanceId = table.task_id
            AidanceTable = findById(Aidance, "id", aidanceId)
            if not AidanceTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["query_fail"])
                return jsonify(resultDict)
            # 创建新的审核表
            # 获取上一级管理人
            flowId = AidanceTable.flow_id
            checkPerson = getRolePerson(AidanceTable, flowId, dbOperation)
            if checkPerson is None:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["query_fail"])
                return jsonify(resultDict)
            now = getTimeStrfTimeStampNow()
            # 添加 新的审核表
            sort = 1
            aidanceStr = (aidanceId, now, current_user.admin_name, 1, None, checkPerson, None, sort)
            tableCheck = dbOperation.insertToSQL(AidanceCheck, *aidanceStr)
            if not tableCheck:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["update_fail"])
                return jsonify(resultDict)
            # 更新task
            AidanceTable.check_id = tableCheck.id
            AidanceTable = dbOperation.addTokenToSql(AidanceTable)
            if not AidanceTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["update_fail"])
                return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 咨询师 送审  # 上报
@app.route("/updataUpCounselorWholeServiceCheckStatus", methods=["POST"])
@jwt_required
def updataUpCounselorWholeServiceCheckStatus():
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
        table = findById(WholeService, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        reslut = sendUp(table, choicePerson, dbOperation, flowId=Res.workFlow["zxFW"], taskType=None)
        if not reslut:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        table.is_done = 3
        table = dbOperation.addTokenToSql(table)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 咨询师 被退回 列表
@app.route("/findCounselorViewInnerWholeServiceByCondition", methods=["POST"])
@jwt_required
def findCounselorViewInnerWholeServiceByCondition():
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
    }, {
        "field": "flowId",
        "op": "equal",
        "value": Res.workFlow["zxFW"]
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = "view_aidance_check_flow_data_whole_service"  # view_aidance_check_channel_user
    intColumnClinetNameList = intList + ["checkStatus", "flowId"]
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_aidance_check_whole_service_change,
                                             intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = view_aidance_check_whole_service_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 合同中间人 列表
@app.route("/findCounserloViewWholeServiceByCondition", methods=["POST"])
@jwt_required
def findCounserloViewWholeServiceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["zxFW"]
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
    }, {
        "field": "flowId",
        "op": "equal",
        "value": flowId
    }]
    for newDict in newDictList:
        condition.append(newDict)
    tableName = "view_aidance_check_data_whole_service"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_check_whole_service_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_check_whole_service_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 咨询副部长 审核 通过 服务方案
@app.route("checkWholeAidanceService", methods=["POST"])
@jwt_required
def checkWholeAidanceService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus", "")
    if not (id and checkStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(Aidance, "id", id)
    if not table:
        resultDict = returnErrorMsg(errorCode["query_fail"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    now = getTimeStrfTimeStampNow()
    if checkStatus == 2:
        ###now
        table.is_done = 2
        table.complete_time = now
        table.flow_step += 1
        table = dbOperation.addTokenToSql(table)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        fromId = table.from_id
        serviceId = table.service_id
        serviceInfo = findById(WholeService, "id", serviceId)
        if not serviceInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceInfo.is_done = 2
        pdfPath = createWholePdf(serviceId)
        if pdfPath:
            serviceInfo.pdf_path = pdfPath
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        serviceInfo = dbOperation.addTokenToSql(serviceInfo)
        if not serviceInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        if fromId:
            # last
            lastTable = findById(Aidance, "id", fromId)
            if not lastTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["query_fail"])
                return jsonify(resultDict)
            lastTable.is_done = 2
            lastTable.complete_time = now
            lastTable.service_id = serviceId
            lastTable = dbOperation.addTokenToSql(lastTable)
            if not lastTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["query_fail"])
                return jsonify(resultDict)
    elif checkStatus == 3:
        ###now
        table.flow_step = 1
        table = dbOperation.addTokenToSql(table)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # 更新check
    checkId = table.check_id
    intColumnClinetNameList = ['id', u'aidanceId', u'checkStatus', "sort"]
    checkInfo = dbOperation.updateThis(AidanceCheck, AidanceCheck.id, checkId, dataDict, AidanceCheckChangeDic,
                                       intColumnClinetNameList=intColumnClinetNameList)
    if not checkInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 删除
@app.route("/deleteCounselorWholeService", methods=["POST"])
@jwt_required
@deleteLog('data_whole_service')
def deleteCounselorWholeService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    del_list = []
    for id in idList:
        wholeInfo = findById(WholeService, "id", id)
        if wholeInfo:
            if wholeInfo.execute_person == current_user.admin_name and wholeInfo.aidance_type == 2:
                del_list.append(id)
    if not del_list:
        resultDict = returnErrorMsg(errorCode["whole_single_service_not_del"])
        return jsonify(resultDict)
    count = deleteByIdBoss(WholeService, del_list, "id")

    if count == len(del_list):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addCounselorWholeService", methods=["POST"])
@jwt_required
@addLog('data_whole_service')
def addCounselorWholeService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskId = None
    serviceId = dataDict.get("serviceId", None)
    customerName = dataDict.get("customerName", None)
    serviceStartTime = dataDict.get("serviceStartTime", None)
    serviceAgency = dataDict.get("serviceAgency", Res.serviceAgency)
    servicePerson = dataDict.get("servicePerson", Res.servicePerson)
    policyFinancingAdviser = dataDict.get("policyFinancingAdviser", None)
    companyProfile = dataDict.get("companyProfile", None)
    declareProject = dataDict.get("declareProject", None)
    policyService = dataDict.get("policyService", None)
    zzhService = dataDict.get("zzhService", None)
    qualificationBack = dataDict.get("qualificationBack", None)
    declareRecommend = dataDict.get("declareRecommend", None)
    declareProposal = dataDict.get("declareProposal", None)
    aidanceType = 2
    remark = dataDict.get("remark", None)
    pdfPath = dataDict.get("pdfPath", None)
    createPerson = None
    createTime = None
    executePerson = current_user.admin_name
    executeTime = getTimeStrfTimeStampNow()
    isDone = 1
    columsStr = (
        taskId, serviceId, customerName, serviceStartTime, serviceAgency, servicePerson, policyFinancingAdviser,
        companyProfile, declareProject, policyService, zzhService, qualificationBack, declareRecommend, declareProposal,
        aidanceType, remark, pdfPath, createPerson, createTime, executePerson, executeTime, isDone)
    table = insertToSQL(WholeService, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)



#
# # 咨询师 - 退回送审
# @app.route("/updateZxsReasetAidanceCheckStatus", methods=["POST"])
# @jwt_required
# def updateZxsReasetAidanceCheckStatus():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     idList = dataDict.get("ids", "")
#     roleId = dataDict.get("roleId", "")
#     if not (idList and roleId):
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     dataDict.pop("roleId")
#     dbOperation = OperationOfDB()
#     for id in idList:
#         table = findById(Aidance, "id", id)
#         if not table:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["query_fail"])
#             return jsonify(resultDict)
#         # 创建新的审核表
#         # 获取上一级管理人
#         flowId = table.flow_id
#         checkPerson = getRolePerson(table, flowId, dbOperation)
#         if checkPerson is None:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["query_fail"])
#             return jsonify(resultDict)
#         now = getTimeStrfTimeStampNow()
#         # 添加 新的审核表
#         sort = 1
#         aidanceStr = (id, now, current_user.admin_name, 1, None, checkPerson, None, sort)
#         tableCheck = dbOperation.insertToSQL(AidanceCheck, *aidanceStr)
#         if not tableCheck:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["update_fail"])
#             return jsonify(resultDict)
#         # 更新task
#         table.check_id = tableCheck.id
#         table = dbOperation.addTokenToSql(table)
#         if not table:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["update_fail"])
#             return jsonify(resultDict)
#     if dbOperation.commitToSQL():
#         resultDict = returnMsg({})
#     else:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["commit_fail"])
#     return jsonify(resultDict)
# NewAidanceApi.py checkAidanceCheck

def tableSort(table):
    _infoDict = {"id": table.id,
                 "taskId": table.task_id,
                 "serviceId": table.service_id,
                 "customerName": table.customer_name,
                 "serviceStartTime": table.service_start_time,
                 "serviceAgency": table.service_agency,
                 "servicePerson": table.service_person,
                 "policyFinancingAdviser": table.policy_financing_adviser,
                 "companyProfile": table.company_profile,
                 "declareProject": table.declare_project,
                 "policyService": table.policy_service,
                 "zzhService": table.zzh_service,
                 "qualificationBack": table.qualification_back,
                 "declareRecommend": table.declare_recommend,
                 "declareProposal": table.declare_proposal,
                 "aidanceType": table.aidance_type,
                 "remark": table.remark,
                 "pdfPath": table.pdf_path,
                 "createPerson": table.create_person,
                 "createTime": table.create_time,
                 "executePerson": table.execute_person,
                 "executeTime": table.execute_time,
                 "isDone": table.is_done, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    creaetPerson = tableData[18]
    businessRealName = ""
    if creaetPerson:
        userInfo = findById(User, "admin_name", creaetPerson, isStrcheck=True)
        businessRealName = userInfo.admin_real_name if userInfo else ""
    pdfPath = tableData[17]
    if pdfPath:
        pdfPath = url_for("static", filename=pdfPath, _external=True)
    _infoDict = {"id": tableData[0],
                 "taskId": tableData[1],
                 "serviceId": tableData[2],
                 "customerName": tableData[3],
                 "serviceStartTime": tableData[4],
                 "serviceAgency": tableData[5],
                 "servicePerson": tableData[6],
                 "policyFinancingAdviser": tableData[7],
                 "companyProfile": tableData[8],
                 "declareProject": tableData[9],
                 "policyService": tableData[10],
                 "zzhService": tableData[11],
                 "qualificationBack": tableData[12],
                 "declareRecommend": tableData[13],
                 "declareProposal": tableData[14],
                 "aidanceType": tableData[15],
                 "remark": tableData[16],
                 "pdfPath": pdfPath,
                 "createPerson": tableData[18],
                 "createTime": tableData[19],
                 "executePerson": tableData[20],
                 "executeTime": tableData[21],
                 "isDone": tableData[22],
                 "createRealName": businessRealName,
                 }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def view_aidance_check_whole_service_fun(tableData):
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
        "wholeServiceId": tableData[27],
        "wholeCustomerName": tableData[28],
        "serviceStartTime": tableData[29],
        "serviceAgency": tableData[30],
        "servicePerson": tableData[31],
        "policyFinancingAdviser": tableData[32],
        "companyProfile": tableData[33],
        "declareProject": tableData[34],
        "policyService": tableData[35],
        "zzhService": tableData[36],
        "qualificationBack": tableData[37],
        "declareRecommend": tableData[38],
        "declareProposal": tableData[39],
        "aidanceType": tableData[40],
        "wholeRemark": tableData[41],
        "pdfPath": tableData[42], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_aidance_check_whole_service_change = {
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
    "wholeServiceId": "whole_service_id",
    "wholeCustomerName": "whole_customer_name",
    "serviceStartTime": "service_start_time",
    "serviceAgency": "service_agency",
    "servicePerson": "service_person",
    "policyFinancingAdviser": "policy_financing_adviser",
    "companyProfile": "company_profile",
    "declareProject": "declare_project",
    "policyService": "policy_service",
    "zzhService": "zzh_service",
    "qualificationBack": "qualification_back",
    "declareRecommend": "declare_recommend",
    "declareProposal": "declare_proposal",
    "aidanceType": "aidance_type",
    "wholeRemark": "whole_remark",
    "pdfPath": "pdf_path", }
