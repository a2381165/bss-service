# coding:utf-8

###########################33
# coding:utf-8
# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from models.Base.Area import Area
from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Channel.ChannelUserTask import ChannelUserTask, UserTaskChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
import Res
from models.Data.SubFlow import SubFlow
from common.FlowCommon import sendUp, returnUp
from common.reCommon import reEmail, rePhone
from models.Data.Aidance import Aidance
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic, intList as aidanceCheckIntList
from common.FlowCommon import getFlowSort, getFlowUnderSort
from models.Channel.ChannelMember import ChannelMember
from models.Channel.ChannelUser import ChannelUser
from models.Channel.ChannelGrantArea import ChannelGrantArea
import base64
from common.UserPasswordEncrypt import make_appKey, make_appsecret, PasswordSort, codeCreate


# 添加
@app.route("/addUserTask", methods=["POST"])
@jwt_required
@addLog('channel_user_task')
def addUserTask():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskId = None
    contractNo = dataDict.get("contractNo", None)
    userName = None
    memberContactPhone = dataDict.get("memberContactPhone", None)
    memberType = dataDict.get("memberType", None)
    regType = 5
    memberName = dataDict.get("memberName", None)
    memberContactPerson = dataDict.get("memberContactPerson", None)
    if not rePhone(memberContactPhone):
        resultDict = returnErrorMsg(errorCode["phone_args_fail"])
        return jsonify(resultDict)
    memberContactAddress = dataDict.get("memberContactAddress", None)
    memberContactEmail = dataDict.get("memberContactEmail", None)
    if not reEmail(memberContactEmail):
        resultDict = returnErrorMsg(errorCode["email_fail"])
        return jsonify(resultDict)
    appKey = None
    appSecret = None
    startDate = dataDict.get("startDate", None)
    endDate = dataDict.get("endDate", None)
    socpeArea = dataDict.get("socpeArea", None)
    socpeCategory = dataDict.get("socpeCategory", None)
    scopeIndustry = dataDict.get("scopeIndustry", None)
    scopeKeyword = dataDict.get("scopeKeyword", None)
    createPerson = current_user.admin_name
    createTime = getTimeStrfTimeStampNow()
    executePerson = None
    executeTime = None
    isDone = 0
    columsStr = (taskId, contractNo, userName, memberContactPhone, memberType, regType, memberName, memberContactPerson,
                 memberContactAddress, memberContactEmail, appKey, appSecret, startDate, endDate, socpeArea,
                 socpeCategory,
                 scopeIndustry, scopeKeyword, createPerson, createTime, executePerson, executeTime, isDone)
    table = insertToSQL(ChannelUserTask, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
    else:
        resultDict = returnMsg({})
    return jsonify(resultDict)


# 商务经理 渠道商列表 待上报 已上报 已成功
@app.route("/findUserTaskByCondition", methods=["POST"])
@jwt_required
@queryLog('channel_user_task')
def findUserTaskByCondition():
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
    tablename = ChannelUserTask.__tablename__
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
@app.route("/findViewInnerUserTaskByCondition", methods=["POST"])
@jwt_required
def findViewInnerUserTaskByCondition():
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
    tablename = "view_aidance_check_flow_user_task"  # view_aidance_check_channel_user
    intColumnClinetNameList = intList + ["checkStatus", "sort"]
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_aidance_check_user_task_change, intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = view_aidance_check_user_task_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 渠道商中间人 列表
@app.route("/findViewUserTaskByCondition", methods=["POST"])
@jwt_required
def findViewUserTaskByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["qdslc"]
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
    tableName = "view_aidance_check_channel_user"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_check_user_task_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_check_user_task_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务经理送审  # 上报
@app.route("/updataUpUserTaskCheckStatus", methods=["POST"])
@jwt_required
def updataUpUserTaskCheckStatus():
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
        table = findById(ChannelUserTask, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        reslut = sendUp(table, choicePerson, dbOperation, flowId=Res.workFlow["qdslc"], taskType=None)
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
@app.route("/updataUserTask", methods=["POST"])
@jwt_required
def updataUserTask():
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
    table = dbOperation.updateThis(ChannelUserTask, ChannelUserTask.id, id, dataDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if checkStatus == 2:
        reslut = sendUp(table, None, dbOperation, flowId=Res.workFlow["qdslc"], taskType=None)
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
@app.route("/updataUpReturnUserTask", methods=["POST"])
@jwt_required
def updataUpReturnUserTask():
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
    table = dbOperation.updateThis(ChannelUserTask, ChannelUserTask.id, serviceId, dataDict, tableChangeDic)
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
@app.route("/sendUpReturnUserTask", methods=["POST"])
@jwt_required
def sendUpReturnUserTask():
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
        table = findById(ChannelUserTask, "id", serviceId)
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
@app.route("/UserTaskTransferOtherPerson", methods=["POST"])
@jwt_required
def UserTaskTransferOtherPerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    createPerson = dataDict.get("createPerson", "")
    if not (idList and createPerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.updateThis(ChannelUserTask, ChannelUserTask.id, id, dataDict,
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
@app.route("/deleteUserTask", methods=["POST"])
@jwt_required
@deleteLog('channel_user_task')
def deleteUserTask():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(ChannelUserTask, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 部长审核
@app.route("/finallyCheckUserTask", methods=["POST"])
@jwt_required
def finallyCheckUserTask():
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
        serviceTable = dbOperation.findById(ChannelUserTask, "id", serviceId)
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceTable.is_done = 2
        serviceTable = dbOperation.addTokenToSql(serviceTable)
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        # 生成channel_user and channel_member
        channelUserInfo = createChannelUser(serviceTable, dbOperation)
        if not channelUserInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["insert_fail"])
            return jsonify(resultDict)
        userId = channelUserInfo.id
        userSalt = channelUserInfo.user_salt
        chanmemberInfo = createChannelMember(userSalt, userId, serviceTable, dbOperation)
        if not chanmemberInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["insert_fail"])
            return jsonify(resultDict)
        if not createChannelGrantArea(userId, serviceTable, dbOperation):
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["insert_fail"])
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
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# NewAidanceApi.py checkAidanceCheck

def tableSort(table):
    _infoDict = {
        "id": table.id,
        "taskId": table.task_id,
        "contractNo": table.contract_no,
        "userName": table.user_name,
        "memberContactPhone": table.member_contact_phone,
        "memberType": table.member_type,
        "regType": table.reg_type,
        "memberName": table.member_name,
        "memberContactPerson": table.member_contact_person,
        "memberContactAddress": table.member_contact_address,
        "memberContactEmail": table.member_contact_email,
        "appKey": table.app_key,
        "appSecret": table.app_secret,
        "startDate": table.start_date,
        "endDate": table.end_date,
        "socpeArea": table.socpe_area,
        "socpeCategory": table.socpe_category,
        "scopeIndustry": table.scope_industry,
        "scopeKeyword": table.scope_keyword,
        "createPerson": table.create_person,
        "createTime": table.create_time,
        "executePerson": table.execute_person,
        "executeTime": table.execute_time,
        "isDone": table.is_done, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    areaCodes = tableData[15]
    areaName = getAreaName(areaCodes)
    _infoDict = {
        "id": tableData[0],
        "taskId": tableData[1],
        "contractNo": tableData[2],
        "userName": tableData[3],
        "memberContactPhone": tableData[4],
        "memberType": tableData[5],
        "regType": tableData[6],
        "memberName": tableData[7],
        "memberContactPerson": tableData[8],
        "memberContactAddress": tableData[9],
        "memberContactEmail": tableData[10],
        "appKey": tableData[11],
        "appSecret": tableData[12],
        "startDate": tableData[13],
        "endDate": tableData[14],
        "socpeArea": tableData[15],
        "socpeCategory": tableData[16],
        "scopeIndustry": tableData[17],
        "scopeKeyword": tableData[18],
        "createPerson": tableData[19],
        "createTime": tableData[20],
        "executePerson": tableData[21],
        "executeTime": tableData[22],
        "isDone": tableData[23],
        "areaName": areaName,
    }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def view_aidance_check_user_task_fun(tableData):
    areaCodes = tableData[40]
    areaName = getAreaName(areaCodes)
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
        "contractNo": tableData[27],
        "userName": tableData[28],
        "memberContactPhone": tableData[29],
        "memberType": tableData[30],
        "regType": tableData[31],
        "memberName": tableData[32],
        "memberContactPerson": tableData[33],
        "memberContactAddress": tableData[34],
        "memberContactEmail": tableData[35],
        "appKey": tableData[36],
        "appSecret": tableData[37],
        "startDate": tableData[38],
        "endDate": tableData[39],
        "socpeArea": tableData[40],
        "socpeCategory": tableData[41],
        "scopeIndustry": tableData[42],
        "scopeKeyword": tableData[43],
        "areaName": areaName,
    }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_aidance_check_user_task_change = {
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
    "contractNo": "contract_no",
    "userName": "user_name",
    "memberContactPhone": "member_contact_phone",
    "memberType": "member_type",
    "regType": "reg_type",
    "memberName": "member_name",
    "memberContactPerson": "member_contact_person",
    "memberContactAddress": "member_contact_address",
    "memberContactEmail": "member_contact_email",
    "appKey": "app_key",
    "appSecret": "app_secret",
    "startDate": "start_date",
    "endDate": "end_date",
    "socpeArea": "socpe_area",
    "socpeCategory": "socpe_category",
    "scopeIndustry": "scope_industry",
    "scopeKeyword": "scope_keyword", }


def getAreaName(areaCodes):
    _areaName = []
    for areacode in areaCodes.split(","):
        areaInfo = findById(Area, "area_code", areacode, isStrcheck=True)
        _areaName.append(areaInfo.area_name if areaInfo else "")
    areaName = ",".join(_areaName)
    return areaName


def createChannelUser(serviceTable, dbOperation):
    now = getTimeStrfTimeStampNow()
    userName = codeCreate(8)
    table = findById(ChannelUser, "user_name", userName, isStrcheck=True)
    if table:
        return None
    userSalt = codeCreate(8)
    pw = PasswordSort()
    userPassword = pw.passwordEncrypt("123456")
    userPhone = serviceTable.member_contact_phone
    userEmail = serviceTable.member_contact_email
    avatar = None
    nickName = serviceTable.member_name
    regTime = now
    regIp = None
    isCheckPhone = 0
    isCheckEmail = 0
    accessToken = None
    refreshToken = None
    regType = serviceTable.reg_type
    isLock = 1
    ChannelUserStr = (
        userName, userSalt, userPassword, userPhone, userEmail, avatar, nickName, regTime, regIp, isCheckPhone,
        isCheckEmail, accessToken, refreshToken, regType, isLock)
    channelUserInfo = dbOperation.insertToSQL(ChannelUser, *ChannelUserStr)
    if not channelUserInfo:
        return None
    # channelUserInfo.user_name = base64.b64encode(str(channelUserInfo.id))
    # channelUserInfo = dbOperation.addTokenToSql(channelUserInfo)
    # if not channelUserInfo:
    #     return None
    return channelUserInfo


def createChannelMember(userSalt, userId, serviceTable, dbOperation):
    memberName = serviceTable.member_name
    memberType = serviceTable.member_type
    idStr = str(hex(int(userId)))[2:]
    userInvitedCode = idStr + "W" + userSalt[:10 - len(idStr) - 1]
    invitedCode = userInvitedCode
    memberRank = 5
    memberPoints = 0
    memberBalance = 0
    memberContactEmail = serviceTable.member_contact_email
    memberContactPerson = serviceTable.member_contact_person
    memberContactPhone = serviceTable.member_contact_phone
    memberContactAddress = serviceTable.member_contact_address
    maidRate = 5
    areaCode = None
    memberCreditCode = None
    appKey = make_appKey(memberName)
    appSecret = make_appsecret(memberName)
    startDate = serviceTable.start_date
    endDate = serviceTable.end_date
    isWx = 0
    isQq = 0
    remark = None
    ChannelMemberStr = (
        userId, memberName, memberType, invitedCode, memberRank, memberPoints, memberBalance, memberContactEmail,
        memberContactPerson, memberContactPhone, memberContactAddress, maidRate, areaCode,
        memberCreditCode, appKey, appSecret, startDate, endDate, isWx, isQq, remark)
    channelMemberInfo = dbOperation.insertToSQL(ChannelMember, *ChannelMemberStr)
    if not channelMemberInfo:
        return None
    return channelMemberInfo


def createChannelGrantArea(userId, serviceTable, dbOperation):
    areaCodes = serviceTable.socpe_area
    for areaCode in areaCodes.split(","):
        areaStr = (userId, areaCode)
        areaTable = dbOperation.insertToSQL(ChannelGrantArea, *areaStr)
        if not areaTable:
            return None
    return True
