# coding:utf-8
from flask import jsonify, json, request, url_for
from flask_jwt_extended import jwt_required, current_user

import Res
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.Aidance import Aidance, AidanceChangeDic as tableChangeDic
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic
from models.Data.SingleService import SingleService, SingleServiceChangeDic
from models.Data.SubFlow import SubFlow
from models.Data.WholeService import WholeService, WholeServiceChangeDic
from version.v3.bossConfig import app
from common.listMysql import getRolePerson
from common.FlowCommon import getFlowSort


# 委托创建 商务经理 第一步
@app.route("/addEntrustAidance", methods=["POST"])
@jwt_required
def addEntrustAidance():
    now = getTimeStrfTimeStampNow()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    createReason = dataDict.get("createReason", None)
    flowId = dataDict.get("flowId", None)
    taskType = dataDict.get("taskType", 1)
    remark = dataDict.get("remark", None)
    customerName = dataDict.get("customerName", None)
    createTime = now
    createRealName = current_user.admin_real_name
    createPerson = current_user.admin_name

    if not (createReason and flowId and taskType):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # 创建协助表
    executePerson = None
    checkId = 0
    fromId = None
    serviceId = None
    acceptStatus = 0
    isDone = 0
    setpFlow = 1
    aidanceStr = (customerName, createReason, createRealName, str(createTime), flowId, remark, executePerson,
                  createPerson, None, checkId, fromId, serviceId, setpFlow, acceptStatus, isDone, taskType)
    dbOperation = OperationOfDB()
    table = dbOperation.insertToSQL(Aidance, *aidanceStr)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
    return jsonify(resultDict)


# 商务经理 删除
@app.route("/deleteAidance", methods=["POST"])
def deleteAidance():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(Aidance, idList, "id")
    if len(idList) == count:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["delete_fail"])
    return jsonify(resultDict)


# 商务经理 查询 创建列表 咨询师通用 # checkId
@app.route("/findBusinessAssignAidanceByCondition", methods=["POST"])
@jwt_required
def findBusinessAssignAidanceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if not (dataDict.has_key("condition")):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newDictList = [{
        "field": "createPerson",
        "op": "equal",
        "value": current_user.admin_name
    }]
    for newDict in newDictList:
        condition.append(newDict)
    tableName = "view_aidance_check"  # aidacne_id
    orderByStr = " order by create_time desc"
    intColumnClinetNameList = [u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep', u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]
    resultList, count = conditionDataListFind(dataDict, findBusinessAssignAidanceByConditionChange,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = {
                "id": tableData[0],
                "createReason": tableData[1],
                "createRealName": tableData[2],
                "createTime": tableData[3],
                "flowId": tableData[4],
                "remark": tableData[5],
                "executePerson": tableData[6],
                "createPerson": tableData[7],
                "completeTime": tableData[8],
                "checkId": tableData[9],
                "fromId": tableData[10],
                "serviceId": tableData[11],
                "flowStep": tableData[12],
                "acceptStatus": tableData[13],
                "isDone": tableData[14],
                "submitTime": tableData[15],
                "submitPerson": tableData[16],
                "checkStatus": tableData[17],
                "checkTime": tableData[18],
                "checkPerson": tableData[19],
                "checkRemark": tableData[20],
                "aidanceId": tableData[21],
                "customerName": tableData[22],
                "name": tableData[23],
                "desc": tableData[24],
                "num": tableData[25],
                "sort": tableData[26],
                "taskType": tableData[27],
            }
            _infoDict = dictRemoveNone(_infoDict)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务经理 已同意
@app.route("/findBusinessAssignAidanceCheckByCondition", methods=["POST"])
@jwt_required
def findBusinessAssignAidanceCheckByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if not (dataDict.has_key("condition")):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newDictList = [{
        "field": "createPerson",
        "op": "equal",
        "value": current_user.admin_name
    }, {
        "field": "isDone",
        "op": "equal",
        "value": 1
    }]
    for newDict in newDictList:
        condition.append(newDict)
    tableName = "view_aidance_check_demo"
    orderByStr = " order by create_time desc"

    intColumnClinetNameList = [u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep', u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', "num"]
    resultList, count = conditionDataListFind(dataDict, findBusinessAssignAidanceByConditionChange,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            nextTable = findById(Aidance, "from_id", tableData[0])
            pdfPath = ""
            aidanceId = ""
            taskType = ""
            if nextTable:
                aidanceId = nextTable.id
                service_id = nextTable.id
                taskType = nextTable.task_type
                pdfPath = lookO(service_id, taskType)
                if pdfPath:
                    pdfPath = url_for("static", filename=pdfPath, _external=True)
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
                # "taskType": tableData[16],
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
                "aidanceId": aidanceId,
                "pdfPath": pdfPath,
                "taskType": taskType,
            }
            _infoDict = dictRemoveNone(_infoDict)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 流程列表 通用 咨询师 待接收 也是 这个列表 # view check
@app.route("/findWaitAidanceByConditionCheck", methods=["POST"])
@jwt_required
def findWaitAidanceByConditionCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = 10
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
    tableName = "view_aidance_check"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, findBusinessAssignAidanceByConditionChange,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = {
                "id": tableData[0],
                "createReason": tableData[1],
                "createRealName": tableData[2],
                "createTime": tableData[3],
                "flowId": tableData[4],
                "remark": tableData[5],
                "executePerson": tableData[6],
                "createPerson": tableData[7],
                "completeTime": tableData[8],
                "checkId": tableData[9],
                "fromId": tableData[10],
                "serviceId": tableData[11],
                "flowStep": tableData[12],
                "acceptStatus": tableData[13],
                "isDone": tableData[14],
                "submitTime": tableData[15],
                "submitPerson": tableData[16],
                "checkStatus": tableData[17],
                "checkTime": tableData[18],
                "checkPerson": tableData[19],
                "checkRemark": tableData[20],
                "aidanceId": tableData[21],
                "customerName": tableData[22],
                "name": tableData[23],
                "desc": tableData[24],
                "num": tableData[25],
                "sort": tableData[26],
                "taskType": tableData[27],
            }
            _infoDict = dictRemoveNone(_infoDict)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务经理送审
@app.route("/updataUpAidanceCheckStatus", methods=["POST"])
@jwt_required
def updataUpAidanceCheckStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")  # AidanceCheckId
    roleId = dataDict.get("roleId", "")
    if not (idList and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = findById(Aidance, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        # 获取上一级管理人
        flowId = table.flow_id
        checkPerson = getRolePerson(table, flowId, dbOperation)
        if checkPerson is None:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        now = getTimeStrfTimeStampNow()
        # 添加 新的审核表 # 跟着步骤查询
        flowStep = 1
        aidanceStr = (id, now, current_user.admin_name, 1, None, checkPerson, None, flowStep)
        tableCheck = dbOperation.insertToSQL(AidanceCheck, *aidanceStr)
        if not tableCheck:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        # 更新task
        table.check_id = tableCheck.id
        table = dbOperation.addTokenToSql(table)
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


# 商务经理退回送审
@app.route("/updateAidanceUp", methods=["POST"])
@jwt_required
def updateAidanceSend():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids")
    roleId = dataDict.get("roleId")
    if not (idList and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dataDict.pop("roleId")
    dbOperation = OperationOfDB()
    for id in idList:
        table = findById(Aidance, "id", id)
        if not table:
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        # 创建新的审核表
        # 获取上一级管理人
        flowId = table.flow_id
        checkPerson = getRolePerson(table, flowId, dbOperation)
        if checkPerson is None:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        now = getTimeStrfTimeStampNow()
        # 添加 新的审核表
        flowStep = 1
        aidanceStr = (id, now, current_user.admin_name, 1, None, checkPerson, None, flowStep)
        tableCheck = dbOperation.insertToSQL(AidanceCheck, *aidanceStr)
        if not tableCheck:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        # 更新task
        table.check_id = tableCheck.id
        table = dbOperation.addTokenToSql(table)
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


# 商务经理上报 商务副部长退回 重新修改
@app.route("/updateAidanceUps", methods=["POST"])
@jwt_required
def updateAidanceUps():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id")
    if not (id):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    # 更新task
    table = dbOperation.updateThis(Aidance, Aidance.id, id, dataDict, tableChangeDic)
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


# 审核流程 分派
@app.route("/checkAidanceCheck", methods=["POST"])
@jwt_required
def checkAidanceCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    checkStatus = dataDict.get("checkStatus", "")
    roleId = dataDict.get("roleId", "")
    choicePersonName = dataDict.get("choicePerson", "")
    popList = ["roleId", "choicePerson"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    if not (idList and checkStatus and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        #  查询协助表
        aidanceTable = findById(Aidance, "id", id)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        checkId = aidanceTable.check_id
        flowId = aidanceTable.flow_id
        # 查询审核表是否存在
        aidanceCheckTable = AidanceCheck.query.filter(AidanceCheck.aidance_id == id, AidanceCheck.id == checkId).first()
        if not aidanceCheckTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        now = getTimeStrfTimeStampNow()  # 提交时间
        submit_person = current_user.admin_name  # 提交人
        # 审核通过
        if checkStatus == Res.AuditCode["pass"]:
            if not choicePersonName:
                checkPerson = getRolePerson(aidanceTable, flowId, dbOperation)
                if checkPerson is None:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg(errorCode["query_fail"])
                    return jsonify(resultDict)
            else:
                checkPerson = choicePersonName
            # 创建下一级
            flowStep = aidanceTable.flow_step + 1
            checkAidanceStr = (aidanceTable.id, now, submit_person, 1, None, checkPerson, None, flowStep)
            checkTable = dbOperation.insertToSQL(AidanceCheck, *checkAidanceStr)
            if not checkTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("insert checktable fail")
                return jsonify(resultDict)
            # aidance 更新内容
            checkId = checkTable.id
            setpFlow = aidanceTable.flow_step + 1
        # 审核不通过
        elif checkStatus == Res.AuditCode["fail"]:
            # 更新步骤为一
            setpFlow = 1
            # 商务经理通过 checkId查看
            checkId = aidanceTable.check_id
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        # 更新 aidanceCheck
        intColumnClinetNameList = [u'id', u'aidanceId', u'checkStatus']
        updateCheckTable = dbOperation.updateThis(AidanceCheck, AidanceCheck.id, aidanceCheckTable.id, dataDict,
                                                  AidanceCheckChangeDic,
                                                  intColumnClinetNameList=intColumnClinetNameList)
        if not updateCheckTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("update checktable fail")
            return jsonify(resultDict)
        # 更新aidance
        aidanceTable.check_id = checkId
        aidanceTable.flow_step = setpFlow
        aidanceTable = dbOperation.addTokenToSql(aidanceTable)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("update checktable fail")
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("commit fail")
    return jsonify(resultDict)

#
# # 咨询师接收
# @app.route("/acceptAidance", methods=["POST"])
# @jwt_required
# def acceptAidance():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     id = dataDict.get("id", "")
#     checkId = dataDict.get("checkId", "")
#     if not id:
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     dbOperation = OperationOfDB()
#     table = findById(Aidance, "id", id)
#     if not table:
#         resultDict = returnErrorMsg(errorCode["query_fail"])
#         return jsonify(resultDict)
#     # 更新 aidance
#     table.accept_status = 1
#     table.flow_step += 1
#     table.execute_person = current_user.admin_name
#     table = dbOperation.addTokenToSql(table)
#     if not table:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["update_fail"])
#         return jsonify(resultDict)
#     # 接收
#     checkInfo = findById(AidanceCheck, "id", checkId)
#     checkInfo.check_status = 2
#     checkInfo = dbOperation.addTokenToSql(checkInfo)
#     if not checkInfo:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["update_fail"])
#         return jsonify(resultDict)
#     # 创建临时 总体
#     now = getTimeStrfTimeStampNow()
#     serviceAgency = Res.serviceAgency
#     servicePerson = Res.servicePerson
#     # 创建总体
#     # task_type
#     if table.task_type == Res.taskType["wtZt"]:
#         WholeServiceSTr = [None, table.customer_name, None, serviceAgency, servicePerson]  # 18
#         WholeServiceSTr.extend([None, ] * 13)
#         WholeServiceSTr[13] = now
#         WholeServiceSTr[14] = current_user.admin_name
#         WholeServiceSTr[15] = 1
#         WholeTable = dbOperation.insertToSQL(WholeService, *WholeServiceSTr)
#         if not WholeTable:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["system_error"])
#             return jsonify(resultDict)
#         serviceId = WholeTable.id
#     # 创建临时 单项
#     elif table.task_type == Res.taskType["wtDx"]:
#         TempSingleServiceSTr = [None, table.customer_name, serviceAgency, servicePerson]  # 18
#         TempSingleServiceSTr.extend([None, ] * 14)
#         TempSingleServiceSTr[13] = now
#         TempSingleServiceSTr[14] = current_user.admin_name
#         TempSingleServiceSTr[15] = 1
#         singleTable = dbOperation.insertToSQL(SingleService, *TempSingleServiceSTr)
#         if not singleTable:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["system_error"])
#             return jsonify(resultDict)
#         serviceId = singleTable.id
#     else:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     # 更新aidance 写入服务id
#     # 创建新的任务表
#     now = getTimeStrfTimeStampNow()
#     createPerson = executePerson = current_user.admin_name
#     completeTime = None
#     checkId = 0
#     fromId = table.id
#     acceptStatus = 1
#     flowId = 3
#     flowStep = 1
#     aidanceStr = (
#         table.customer_name, table.create_reason, current_user.admin_real_name, now, flowId,
#         table.remark, executePerson, createPerson, completeTime, checkId, fromId,
#         serviceId, flowStep, acceptStatus, table.is_done, table.task_type)
#     dbOperation.insertToSQL(Aidance, *aidanceStr)
#     if dbOperation.commitToSQL():
#         resultDict = returnMsg({})
#     else:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["system_error"])
#     return jsonify(resultDict)





########################第二流程#########################

# 自主创建
@app.route("/addAutonomyAidance", methods=["POST"])
@jwt_required
def addAutonomyAidance():
    now = getTimeStrfTimeStampNow()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)  #
    customerName = dataDict.get("customerName", None)
    createReason = dataDict.get("createReason", None)
    flowId = dataDict.get("flowId", "")
    serviceAgency = dataDict.get("serviceAgency", None)
    servicePerson = dataDict.get("servicePerson", None)
    remark = dataDict.get("remark", None)
    taskType = dataDict.get("taskType", None)
    createTime = now
    createRealName = current_user.admin_real_name
    createPerson = current_user.admin_name
    executePerson = current_user.admin_name
    if not (createReason and flowId and servicePerson and serviceAgency and taskType):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    # 创建协助表
    checkId = 0
    serviceId = 0
    acceptStatus = 1
    isDone = 0
    setpFlow = 1
    fromId = 0
    aidanceStr = (customerName, createReason, createRealName, createTime, flowId, remark, executePerson,
                  createPerson, checkId, fromId, serviceId, setpFlow, acceptStatus, isDone, taskType)
    table = dbOperation.insertToSQL(Aidance, *aidanceStr)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    # 创建临时 总体
    now = getTimeStrfTimeStampNow()
    serviceAgency = Res.serviceAgency
    servicePerson = Res.servicePerson
    # 创建总体
    if table.flow_id == 2:
        WholeServiceSTr = [None, table.customer_name, None, serviceAgency, servicePerson]  # 18
        WholeServiceSTr.extend([None, ] * 13)
        WholeServiceSTr[13] = now
        WholeServiceSTr[14] = current_user.admin_name
        WholeServiceSTr[15] = 1
        WholeTable = dbOperation.insertToSQL(WholeService, *WholeServiceSTr)
        if not WholeTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["system_error"])
            return jsonify(resultDict)
        serviceId = WholeTable.id
    # 创建临时 单项
    elif table.flow_id == 1:
        TempSingleServiceSTr = [None, table.customer_name, serviceAgency, servicePerson]  # 18
        TempSingleServiceSTr.extend([None, ] * 14)
        TempSingleServiceSTr[13] = now
        TempSingleServiceSTr[14] = current_user.admin_name
        TempSingleServiceSTr[15] = 1
        singleTable = dbOperation.insertToSQL(SingleService, *TempSingleServiceSTr)
        if not singleTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["system_error"])
            return jsonify(resultDict)
        serviceId = singleTable.id
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table.service_id = serviceId
    table = dbOperation.addTokenToSql(table)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
    return jsonify(resultDict)


# # 单项服务列表 - 咨询师
# @app.route("/findSingleServiceByCondition", methods=["POST"])
# @jwt_required
# def findSingleServiceByCondition():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     if not (dataDict.has_key("condition")):
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     condition = dataDict.get("condition")
#     newDictList = [{
#         "field": "createPerson",
#         "op": "equal",
#         "value": current_user.admin_name
#     }, {
#         "field": "flowId",
#         "op": "equal",
#         "value": 3
#     }]
#     for newDict in newDictList:
#         condition.append(newDict)
#     # tableName = SingleService.__tablename__
#     tableName = "view_single_service_aidance_check"
#     intColumnClinetNameList = [u'id', u'serviceId', u'aidanceType', "checkStatus", "checkId", "flowId", "aidanceId"]
#     newDict = {"checkStatus": "check_status", "checkId": "check_id", "flowId": "flow_id"}
#     newDict = dict(SingleServiceChangeDic, **newDict)
#     resultList, count = conditionDataListFind(dataDict, newDict,
#                                               intColumnClinetNameList=intColumnClinetNameList,
#                                               tableName=tableName)
#     if resultList:
#         infoList = []
#         for tableData in resultList:
#             _infoDict = {
#                 "id": tableData[0],
#                 "serviceId": tableData[1],
#                 "customerName": tableData[2],
#                 "serviceAgency": tableData[3],
#                 "servicePerson": tableData[4],
#                 "serviceContent": tableData[5],
#                 "declareDirection": tableData[6],
#                 "manageDept": tableData[7],
#                 "applyAmount": tableData[8],
#                 "subsidyMethod": tableData[9],
#                 "serviceDeadline": tableData[10],
#                 "declareConditions": tableData[11],
#                 "declareData": tableData[12],
#                 "otherRemark": tableData[13],
#                 "createTime": tableData[14],
#                 "createPerson": tableData[15],
#                 "aidanceType": tableData[16],
#                 "remark": tableData[17],
#                 "pdfPath": tableData[18],
#                 "checkStatus": tableData[19],
#                 "checkId": tableData[20],
#                 "flowId": tableData[21],
#                 "flowStep": tableData[22],
#                 "aidanceId": tableData[23],
#             }
#             _infoDict = dictRemoveNone(_infoDict)
#             infoList.append(_infoDict)
#         resultDict = returnMsg(infoList)
#         resultDict["total"] = count
#     else:
#         resultDict = returnErrorMsg()
#     return jsonify(resultDict)

#
# # 总体服务列表 - 咨询师
# @app.route("/findWholeServiceByCondition", methods=["POST"])
# @jwt_required
# def findWholeServiceByCondition():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     if not (dataDict.has_key("condition")):
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     condition = dataDict.get("condition")
#     newDictList = [{
#         "field": "createPerson",
#         "op": "equal",
#         "value": current_user.admin_name
#     }]
#     for newDict in newDictList:
#         condition.append(newDict)
#     tableName = "view_whole_service_aidance_check"
#     intColumnClinetNameList = [u'id', u'serviceId', u'aidanceType', "sort"]
#     resultList, count = conditionDataListFind(dataDict, view_whole_service_aidance_check,
#                                               intColumnClinetNameList=intColumnClinetNameList,
#                                               tableName=tableName)
#     if resultList:
#         infoList = []
#         for tableData in resultList:
#             _infoDict = {
#                 "id": tableData[0],
#                 "serviceId": tableData[1],
#                 "customerName": tableData[2],
#                 "serviceStartTime": tableData[3],
#                 "serviceAgency": tableData[4],
#                 "servicePerson": tableData[5],
#                 "policyFinancingAdviser": tableData[6],
#                 "companyProfile": tableData[7],
#                 "declareProject": tableData[8],
#                 "policyService": tableData[9],
#                 "zzhService": tableData[10],
#                 "qualificationBack": tableData[11],
#                 "declareRecommend": tableData[12],
#                 "declareProposal": tableData[13],
#                 "createTime": tableData[14],
#                 "createPerson": tableData[15],
#                 "aidanceType": tableData[16],
#                 "remark": tableData[17],
#                 "pdfPath": tableData[18],
#                 "aidanceId": tableData[19],
#                 "checkId": tableData[20],
#                 "flowId": tableData[21],
#                 "flowStep": tableData[22],
#                 "checkStatus": tableData[23],
#             }
#             _infoDict = dictRemoveNone(_infoDict)
#             infoList.append(_infoDict)
#         resultDict = returnMsg(infoList)
#         resultDict["total"] = count
#     else:
#         resultDict = returnErrorMsg()
#     return jsonify(resultDict)
#
#

# 查看 总体 单项
@app.route("/getAdianceInfo", methods=["POST"])
# @jwt_required
def getAdianceInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    aidanceTable = findById(Aidance, "id", id)
    if not aidanceTable:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    serviceId = aidanceTable.service_id
    if aidanceTable.task_type == 1:
        wholeTable = WholeService.query.filter(WholeService.id == serviceId).first()
        if wholeTable:
            _infoDict = {
                "id": wholeTable.id,
                "serviceId": wholeTable.service_id,
                # "aidanceId": wholeTable.aidance_id,
                "customerName": wholeTable.customer_name,
                "serviceStartTime": wholeTable.service_start_time,
                "serviceAgency": wholeTable.service_agency,
                "servicePerson": wholeTable.service_person,
                "policyFinancingAdviser": wholeTable.policy_financing_adviser,
                "companyProfile": wholeTable.company_profile,
                "declareProject": wholeTable.declare_project,
                "policyService": wholeTable.policy_service,
                "zzhService": wholeTable.zzh_service,
                "qualificationBack": wholeTable.qualification_back,
                "declareRecommend": wholeTable.declare_recommend,
                "declareProposal": wholeTable.declare_proposal,
                "createTime": wholeTable.create_time,
                "createPerson": wholeTable.create_person,
                "aidanceType": wholeTable.aidance_type,
                "remark": wholeTable.remark,
                "pdfPath": wholeTable.pdf_path,
            }
        else:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
    elif aidanceTable.task_type == 2:
        singleTable = SingleService.query.filter(SingleService.id == serviceId).first()
        if singleTable:
            _infoDict = {
                "id": singleTable.id,
                "serviceId": singleTable.service_id,
                "customerName": singleTable.customer_name,
                "serviceAgency": singleTable.service_agency,
                "servicePerson": singleTable.service_person,
                "serviceContent": singleTable.service_content,
                "declareDirection": singleTable.declare_direction,
                "manageDept": singleTable.manage_dept,
                "applyAmount": singleTable.apply_amount,
                "subsidyMethod": singleTable.subsidy_method,
                "serviceDeadline": singleTable.service_deadline,
                "declareConditions": singleTable.declare_conditions,
                "declareData": singleTable.declare_data,
                "otherRemark": singleTable.other_remark,
                "createTime": singleTable.create_time,
                "createPerson": singleTable.create_person,
                "aidanceType": singleTable.aidance_type,
                "remark": singleTable.remark,
                "pdfPath": singleTable.pdf_path,
            }
        else:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
    else:
        _infoDict = {}
    _infoDict = dictRemoveNone(_infoDict)
    resultDict = returnMsg(_infoDict)
    return jsonify(resultDict)

#
# # 编辑单项服务 - 送审
# @app.route("updataSingleService", methods=["POST"])
# @jwt_required
# def updataSingleService():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     idList = dataDict.get("ids", "")
#     checkStatus = dataDict.get("checkStatus", "")
#     if dataDict.has_key("checkStatus"):
#         dataDict.pop("checkStatus")
#     if not idList:
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     dbOperation = OperationOfDB()
#     intColumnClinetNameList = [u'id', u'serviceId', u'aidanceId']
#     for id in idList:
#         if len(dataDict.keys()) != 1:
#             table = dbOperation.updateThis(SingleService, SingleService.id, id, dataDict, SingleServiceChangeDic,
#                                            intColumnClinetNameList=intColumnClinetNameList)
#             if not table:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["update_fail"])
#                 return jsonify(resultDict)
#         else:
#             table = findById(SingleService, "id", id)
#             if not table:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["update_fail"])
#                 return jsonify(resultDict)
#         aidanceInfo = findById(Aidance, "service_id", id)
#         if aidanceInfo:
#             # checkId = aidanceInfo.check_id
#             flowId = aidanceInfo.flow_id
#         else:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["query_fail"])
#             return jsonify(resultDict)
#         if checkStatus:
#             now = getTimeStrfTimeStampNow()
#             checkPerson = getRolePerson(aidanceInfo, flowId, dbOperation)
#             if checkPerson is None:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["query_fail"])
#                 return jsonify(resultDict)
#             # 创建下一级
#             flowStep = 1
#             checkAidanceStr = (aidanceInfo.id, now, current_user.admin_name, 1, None, checkPerson, None, flowStep)
#             checkTable = dbOperation.insertToSQL(AidanceCheck, *checkAidanceStr)
#             if not checkTable:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg("insert checktable fail")
#                 return jsonify(resultDict)
#             # 更新下一步
#             aidanceInfo.flow_step += 1
#             aidanceInfo.check_id = checkTable.id
#             aidanceInfo = dbOperation.addTokenToSql(aidanceInfo)
#             if not aidanceInfo:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["param_error"])
#                 return jsonify(resultDict)
#     if dbOperation.commitToSQL():
#         resultDict = returnMsg({})
#     else:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["commit_fail"])
#     return jsonify(resultDict)
#
#
# # 编辑总体服务 - 送审
# @app.route("updataWholeService", methods=["POST"])
# @jwt_required
# def updataWholeService():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     checkStatus = dataDict.get("checkStatus", None)
#     if dataDict.has_key("checkStatus"):
#         dataDict.pop("checkStatus")
#     idList = dataDict.get("ids")
#     if not idList:
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     dbOperation = OperationOfDB()
#     intColumnClinetNameList = [u'id', u'serviceId', u'aidanceType']
#     for id in idList:
#         if len(dataDict.keys()) != 1:
#             table = dbOperation.updateThis(WholeService, WholeService.id, id, dataDict, WholeServiceChangeDic,
#                                            intColumnClinetNameList=intColumnClinetNameList)
#             if not table:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["update_fail"])
#                 return jsonify(resultDict)
#         else:
#             table = findById(WholeService, "id", id)
#             if not table:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["update_fail"])
#                 return jsonify(resultDict)
#         aidanceInfo = findById(Aidance, "service_id", id)
#         if aidanceInfo:
#             flowId = aidanceInfo.flow_id
#         else:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["query_fail"])
#             return jsonify(resultDict)
#         if checkStatus:
#             now = getTimeStrfTimeStampNow()
#             checkPerson = getRolePerson(aidanceInfo, flowId, dbOperation)
#             if checkPerson is None:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["query_fail"])
#                 return jsonify(resultDict)
#             # 创建下一级
#             flowStep = 1
#             checkAidanceStr = (aidanceInfo.id, now, current_user.admin_name, 1, None, checkPerson, None, flowStep)
#             checkTable = dbOperation.insertToSQL(AidanceCheck, *checkAidanceStr)
#             if not checkTable:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg("insert checktable fail")
#                 return jsonify(resultDict)
#             # 更新下一步
#             aidanceInfo.flow_step += 1
#             aidanceInfo.check_id = checkTable.id
#             aidanceInfo = dbOperation.addTokenToSql(aidanceInfo)
#             if not aidanceInfo:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["param_error"])
#                 return jsonify(resultDict)
#     if dbOperation.commitToSQL():
#         resultDict = returnMsg({})
#     else:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["commit_fail"])
#     return jsonify(resultDict)
#
#
# # 咨询副部长 审核 通过 服务方案
# @app.route("checkAidanceService", methods=["POST"])
# @jwt_required
# def checkAidanceService():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     id = dataDict.get("id", "")
#     checkStatus = dataDict.get("checkStatus", "")
#     if not (id and checkStatus):
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     table = findById(Aidance, "id", id)
#     if not table:
#         resultDict = returnErrorMsg(errorCode["query_fail"])
#         return jsonify(resultDict)
#     dbOperation = OperationOfDB()
#     now = getTimeStrfTimeStampNow()
#     if checkStatus == 2:
#         ###now
#         table.is_done = 1
#         table.complete_time = now
#         table.flow_step += 1
#         table = dbOperation.addTokenToSql(table)
#         if not table:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["query_fail"])
#             return jsonify(resultDict)
#         fromId = table.from_id
#         serviceId = table.service_id
#         if fromId:
#             # last
#             lastTable = findById(Aidance, "id", fromId)
#             if not lastTable:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["query_fail"])
#                 return jsonify(resultDict)
#             lastTable.is_done = 1
#             lastTable.complete_time = now
#             lastTable.service_id = serviceId
#             lastTable = dbOperation.addTokenToSql(lastTable)
#             if not lastTable:
#                 dbOperation.commitRollback()
#                 resultDict = returnErrorMsg(errorCode["query_fail"])
#                 return jsonify(resultDict)
#     elif checkStatus == 3:
#         ###now
#         table.flow_step = 1
#         table = dbOperation.addTokenToSql(table)
#         if not table:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["query_fail"])
#             return jsonify(resultDict)
#     else:
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     # 更新check
#     checkId = table.check_id
#     intColumnClinetNameList = ['id', u'aidanceId', u'checkStatus', "sort"]
#     checkInfo = dbOperation.updateThis(AidanceCheck, AidanceCheck.id, checkId, dataDict, AidanceCheckChangeDic,
#                                        intColumnClinetNameList=intColumnClinetNameList)
#     if not checkInfo:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     if dbOperation.commitToSQL():
#         resultDict = returnMsg({})
#     else:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["commit_fail"])
#     return jsonify(resultDict)
#
#
# # 咨询师 删除自主方案
# @app.route("/deleteZxsAidanceServie", methods=["POST"])
# @jwt_required
# def deleteZxsAidanceServie():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     idList = dataDict.get("ids", "")
#     if not idList:
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     dbOperation = OperationOfDB()
#     count = 0
#     for id in idList:
#         table = findById(Aidance, "id", id)
#         if not table:
#             continue
#         # 总体
#         if table.task_type == 1:
#             ServiceName = WholeService
#         elif table.task_type == 2:
#             ServiceName = SingleService
#         else:
#             continue
#         table = findById(ServiceName, "id", table.service_id)
#         if not table:
#             continue
#         is_delete = dbOperation.deleteByIdBoss(ServiceName, id, "id")
#         if not is_delete:
#             dbOperation.commitRollback()
#             resultDict = returnErrorMsg(errorCode["delete_fail"])
#             return jsonify(resultDict)
#         count += 1
#     if dbOperation.commitToSQL():
#         infoDict = {
#             "success": count,
#             "fail": len(idList) - count
#         }
#         resultDict = returnMsg(infoDict)
#     else:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg(errorCode["commit_fail"])
#     return jsonify(resultDict)


def lookO(serviceId, taskType):
    pdfPath = None
    if taskType == 1:
        wholeTable = WholeService.query.filter(WholeService.id == serviceId).first()
        if wholeTable:
            pdfPath = wholeTable.pdf_path
    elif taskType == 2:
        singleTable = SingleService.query.filter(SingleService.id == serviceId).first()
        if singleTable:
            pdfPath = singleTable.pdf_path
    return pdfPath


findBusinessAssignAidanceByConditionChange = {
    "id": "id",
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
    "submitTime": "submit_time",
    "submitPerson": "submit_person",
    "checkStatus": "check_status",
    "checkTime": "check_time",
    "checkPerson": "check_person",
    "checkRemark": "check_remark",
    "aidanceCheckId": "aidance_check_id",
    "customerName": "customer_name",
    "name": "name",
    "desc": "desc",
    "num": "num",
    "sort": "sort",
}

checkIdChange = {
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
}

view_whole_service_aidance_check = {
    "id": "id",
    "serviceId": "service_id",
    "customerName": "customer_name",
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
    "createTime": "create_time",
    "createPerson": "create_person",
    "aidanceType": "aidance_type",
    "remark": "remark",
    "pdfPath": "pdf_path",
    "aidanceId": "aidance_id",
    "checkId": "check_id",
    "flowId": "flow_id",
    "flowStep": "flow_step",
    "checkStatus": "check_status", }


# ###################temp############3
# # 商务经理 单项服务加载
# # 商务经理 单项服务加载
# @app.route("/findBusinessSingleServiceByCondition", methods=["POST"])
# @jwt_required
# def findBusinessSingleServiceByCondition():
#     """
#     isDone 0 待上报,1 流程中,2 完成
#     :return:
#     """
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     if not (dataDict.has_key("condition")):
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     condition = dataDict.get("condition")
#     newDictList = [{
#         "field": "createPerson",
#         "op": "equal",
#         "value": current_user.admin_name
#     }]
#     for newDict in newDictList:
#         condition.append(newDict)
#     tableName = SingleService.__tablename__
#     orderByStr = " order by create_time desc"
#     intColumnClinetNameList = ['id', 'serviceId', 'aidanceType', 'isDone']
#     resultList, count = conditionDataListFind(dataDict, SingleServiceChangeDic,
#                                               intColumnClinetNameList=intColumnClinetNameList,
#                                               tableName=tableName, orderByStr=orderByStr)
#     if resultList:
#         infoList = []
#         for tableData in resultList:
#             _infoDict = {
#                 "id": tableData[0],
#                 "serviceId": tableData[1],
#                 "customerName": tableData[2],
#                 "serviceAgency": tableData[3],
#                 "servicePerson": tableData[4],
#                 "serviceContent": tableData[5],
#                 "declareDirection": tableData[6],
#                 "manageDept": tableData[7],
#                 "applyAmount": tableData[8],
#                 "subsidyMethod": tableData[9],
#                 "serviceDeadline": tableData[10],
#                 "declareConditions": tableData[11],
#                 "declareData": tableData[12],
#                 "otherRemark": tableData[13],
#                 "createTime": tableData[14],
#                 "createPerson": tableData[15],
#                 "aidanceType": tableData[16],
#                 "remark": tableData[17],
#                 "pdfPath": tableData[18],
#                 "executePerson": tableData[19],
#                 "executeTime": tableData[20],
#                 "isDone": tableData[21],
#             }
#             _infoDict = dictRemoveNone(_infoDict)
#             infoList.append(_infoDict)
#         resultDict = returnMsg(infoList)
#         resultDict["total"] = count
#     else:
#         resultDict = returnErrorMsg()
#     return jsonify(resultDict)
#
#
# # 商务经理 总体服务加载
# @app.route("/findBusinessWholeServiceByCondition", methods=["POST"])
# @jwt_required
# def findBusinessWholeServiceByCondition():
#     """
#        isDone 0 待上报,1 流程中,2 完成
#        :return:
#        """
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     if not (dataDict.has_key("condition")):
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     condition = dataDict.get("condition")
#     newDictList = [{
#         "field": "createPerson",
#         "op": "equal",
#         "value": current_user.admin_name
#     }]
#     for newDict in newDictList:
#         condition.append(newDict)
#     tableName = WholeService.__tablename__
#     orderByStr = " order by create_time desc"
#     intColumnClinetNameList = ['id', 'serviceId', 'aidanceType', 'isDone']
#     resultList, count = conditionDataListFind(dataDict, WholeServiceChangeDic,
#                                               intColumnClinetNameList=intColumnClinetNameList,
#                                               tableName=tableName, orderByStr=orderByStr)
#     if resultList:
#         infoList = []
#         for tableData in resultList:
#             _infoDict = {
#                 "id": tableData[0],
#                 "serviceId": tableData[1],
#                 "customerName": tableData[2],
#                 "serviceStartTime": tableData[3],
#                 "serviceAgency": tableData[4],
#                 "servicePerson": tableData[5],
#                 "policyFinancingAdviser": tableData[6],
#                 "companyProfile": tableData[7],
#                 "declareProject": tableData[8],
#                 "policyService": tableData[9],
#                 "zzhService": tableData[10],
#                 "qualificationBack": tableData[11],
#                 "declareRecommend": tableData[12],
#                 "declareProposal": tableData[13],
#                 "createTime": tableData[14],
#                 "createPerson": tableData[15],
#                 "aidanceType": tableData[16],
#                 "remark": tableData[17],
#                 "pdfPath": tableData[18],
#                 "executePerson": tableData[19],
#                 "executeTime": tableData[20],
#                 "isDone": tableData[21],
#             }
#             _infoDict = dictRemoveNone(_infoDict)
#             infoList.append(_infoDict)
#         resultDict = returnMsg(infoList)
#         resultDict["total"] = count
#     else:
#         resultDict = returnErrorMsg()
#     return jsonify(resultDict)
