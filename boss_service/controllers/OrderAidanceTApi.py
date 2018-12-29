# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, current_user

import Res
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FlowCommon import getFlowSort
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteByIdBoss
from common.OperationOfDB import insertToSQL, updataById, executeSqlFirst
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from common.listMysql import getRolePersonFlow
from models.Boss.Communicate import Communicate
from models.Boss.OrderAidance import OrderAidance, intList, OrderAidanceChangeDic as tableChangeDic
from models.Data.Aidance import Aidance, AidanceChangeDic as tableChangeDic
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic
from models.Data.AidanceCheck import intList
from models.Data.Item import Item
from models.Member.MemberBases import MemberBases
from models.Order.OrderService import OrderService
from models.Order.UserOrder import UserOrder
from models.Order.UserOrder import UserOrderChangeDic as tableChangeDic
from version.v3.bossConfig import app
from models.Data.SingleService import SingleService

# 订单分发接口 中间人专用
@app.route("/findSendOrderAidanceByConditionCheck", methods=["POST"])
@jwt_required
def findSendOrderAidanceByConditionCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["yyddff"]
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
    tableName = "view_aidance_order_task"
    # tableName = "view_aidance_check"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, view_aidance_order_task_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = view_aidance_order_task_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取 列表
@app.route("/findOrderAidanceByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_order_aidance')
def findOrderAidanceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
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
    # tablename = OrderAidance.__tablename__
    tablename = "view_order_aidance_info"
    intColumnClinetNameList = intList + ["isDone"]
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, viewChangeDict, intColumnClinetNameList, tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = viewTableSortDict(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getOrderAidanceDetail", methods=["POST"])
@jwt_required
@queryLog('boss_order_aidance')
def getOrderAidanceDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(OrderAidance, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteOrderAidance", methods=["POST"])
@jwt_required
@deleteLog('boss_order_aidance')
def deleteOrderAidance():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(OrderAidance, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addOrderAidance", methods=["POST"])
@jwt_required
@addLog('boss_order_aidance')
def addOrderAidance():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskId = dataDict.get("taskId", None)
    serviceNo = dataDict.get("serviceNo", None)
    preOrderNo = dataDict.get("preOrderNo", None)
    createPerson = dataDict.get("createPerson", None)
    createTime = dataDict.get("createTime", None)
    executePerson = dataDict.get("executePerson", None)
    executeTime = dataDict.get("executeTime", None)
    isDone = dataDict.get("isDone", None)
    columsStr = (id, taskId, serviceNo, preOrderNo, createPerson, createTime, executePerson, executeTime, isDone)
    table = insertToSQL(OrderAidance, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataOrderAidance", methods=["POST"])
@jwt_required
@updateLog('boss_order_aidance')
def updataOrderAidance():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(OrderAidance, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 商务经理送审 单项
@app.route("/updataUpOrderAidanceCheckStatus", methods=["POST"])
@jwt_required
def updataUpOrderAidanceCheckStatus():
    """
    taskType 服务类型 1 战略方案（总体） 2 单项方案  3 单项合同 4 战略合同
    :return:
    """
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")  # 单项服务id
    roleId = dataDict.get("roleId", "")
    customerName = dataDict.get("customerName", "")
    createReason = dataDict.get("createReason", "")
    choicePerson = dataDict.get("choicePerson", "")
    if not (idList and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    now = getTimeStrfTimeStampNow()
    dbOperation = OperationOfDB()
    for id in idList:
        table = findById(OrderAidance, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        # 创建任务表
        flowId = 4  # 单项 流程
        executePerson = None
        checkId = 0
        fromId = 0
        serviceId = table.id
        acceptStatus = 0
        isDone = 0
        setpFlow = 1
        createRealName = current_user.admin_real_name
        createPerson = current_user.admin_name
        createTime = now
        remark = None
        taskType = 2  # 单项
        aidanceStr = (customerName, createReason, createRealName, str(createTime), flowId, remark, executePerson,
                      createPerson, None, checkId, fromId, serviceId, setpFlow, acceptStatus, isDone, taskType)
        dbOperation = OperationOfDB()
        AidanceTable = dbOperation.insertToSQL(Aidance, *aidanceStr)
        if not AidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["insert_fail"])
            return jsonify(resultDict)
        aidanceId = AidanceTable.id
        # 获取上一级管理人
        # flowId = table.flow_id
        # flowId = table.flow_id
        if choicePerson:
            checkPerson = choicePerson
        else:
            checkPerson = getRolePersonFlow(flowId, dbOperation)
        if checkPerson is None:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        # 添加 新的审核表 # 跟着步骤查询
        flowStep = 1
        aidanceStr = (aidanceId, now, current_user.admin_name, 1, None, checkPerson, None, flowStep)
        tableCheck = dbOperation.insertToSQL(AidanceCheck, *aidanceStr)
        if not tableCheck:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        # 更新 task
        AidanceTable.check_id = tableCheck.id
        AidanceTable = dbOperation.addTokenToSql(AidanceTable)
        if not AidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        table.is_done = 1
        table.task_id = AidanceTable.id
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


# 商务经理  接收  任务 | 沟通
@app.route("/acceptTaskBusiness", methods=["POST"])
@jwt_required
def acceptTaskBusiness():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    checkStatus = dataDict.get("checkStatus", "")
    if not (checkStatus and idList):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.has_key("checkStatus"):
        dataDict.pop("checkStatus")
    dbOperation = OperationOfDB()
    for id in idList:
        # 查询 是否有 Aidance
        table = findById(Aidance, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        orderAidacneInfo = findById(OrderAidance, "id", table.service_id)
        if not orderAidacneInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        orderNo = orderAidacneInfo.pre_order_no
        # 通过
        if checkStatus == Res.AuditCode["pass"]:
            # 查询
            sqlStr = "select t2.service_name,t2.direction_name,t3.item_title,t4.member_name from zzh_user_order as t1 join  zzh_order_service as t2 join data_item as t3 join zzh_member_bases as t4 on t1.order_no='{}' and t2.order_no = t1.order_no and t3.item_id =t2.item_id and t4.user_id = t1.user_id".format(
                orderNo)
            resultList = executeSqlFirst(sqlStr)
            productName = None
            require = None
            customerName = None
            if resultList:
                productName = resultList[0]
                require = resultList[1] + resultList[2]
                customerName = resultList[3]
            # else:
            #     dbOperation.commitRollback()
            #     resultDict = returnErrorMsg(errorCode["query_fail"])
            #     return jsonify(resultDict)
            # 创建 沟通表
            projectPath = None
            projectType = 3
            createPerson = current_user.admin_name
            createTime = getTimeStrfTimeStampNow()
            executePerson = current_user.admin_name
            executeTime = getTimeStrfTimeStampNow()
            isDone = 0
            remark = None
            is_send = 0
            source_type = 5
            CommunicateStr = (None, orderAidacneInfo.pre_order_no, orderAidacneInfo.service_no,
                              productName, require, projectPath, projectType, customerName, executePerson, executeTime, createPerson,
                              createTime, is_send, isDone, remark, 0, source_type)
            communicateTable = dbOperation.insertToSQL(Communicate, *CommunicateStr)
            if not communicateTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["param_error"])
                return jsonify(resultDict)
            # 创建单项任务协助表
            taskId = None
            serviceId = None
            customerName = customerName
            serviceAgency = dataDict.get("serviceAgency", Res.serviceAgency)
            servicePerson = dataDict.get("servicePerson", Res.servicePerson)
            serviceContent = None
            declareDirection = None
            manageDept = None
            applyAmount = None
            subsidyMethod = None
            serviceDeadline = None
            declareConditions = None
            declareData = None
            otherRemark = None
            aidanceType = 1
            remark = None
            pdfPath = None
            createPerson = current_user.admin_name
            createTime = getTimeStrfTimeStampNow()
            executePerson = None
            executeTime = None
            isDone = 0
            columsStr = (
                taskId, serviceId, customerName, serviceAgency, servicePerson, serviceContent, declareDirection,
                manageDept,
                applyAmount, subsidyMethod, serviceDeadline, declareConditions, declareData, otherRemark, aidanceType,
                remark,
                pdfPath, createPerson, createTime, executePerson, executeTime, isDone)
            singleTable = insertToSQL(SingleService, *columsStr)
            # createReason = ""  #
            # flowId = 1  # 流程id 1 单项 2 总体
            # taskType = 2  # 服务类型 1 总体 2 单项 3 政策协助 4 签约协助 5 技术协助
            # remark = ""  # 备注
            # customerName = customerName  # 顾客姓名
            # createTime = getTimeStrfTimeStampNow()
            # createRealName = current_user.admin_real_name
            # createPerson = current_user.admin_name
            # executePerson = None
            # checkId = 0
            # fromId = None
            # serviceId = None
            # acceptStatus = 0
            # isDone = 0
            # setpFlow = 1
            # aidanceStr = (customerName, createReason, createRealName, str(createTime), flowId, remark, executePerson,
            #               createPerson, None, checkId, fromId, serviceId, setpFlow, acceptStatus, isDone, taskType)
            # aidanceTable = dbOperation.insertToSQL(Aidance, *aidanceStr)
            if not singleTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["insert_fail"])
                return jsonify(resultDict)
        elif checkStatus == Res.AuditCode["fail"]:
            dbOperation.commitRollback()
            resultList = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultList)
        else:
            dbOperation.commitRollback()
            resultList = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultList)
        # 更新审核表
        checkId = table.check_id
        intColumnClinetNameList = intList
        newDict = {"checkStatus": 2}
        orderAidanceTable = dbOperation.updateThis(AidanceCheck, AidanceCheck.id, checkId, newDict,
                                                   AidanceCheckChangeDic,
                                                   intColumnClinetNameList=intColumnClinetNameList)
        if not orderAidanceTable:
            dbOperation.commitRollback()
            resultList = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultList)
        # 更新任务表
        table.flow_step += 1
        table.is_done = 2
        table.accept_status = 1
        table.execute_person = current_user.admin_name
        table.complete_time = getTimeStrfTimeStampNow()
        orderAidanceTable = dbOperation.addTokenToSql(table)
        if not orderAidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        # 更新明细表
        orderAidacneInfo.execute_person = current_user.admin_name
        orderAidacneInfo.execute_time = getTimeStrfTimeStampNow()
        orderAidacneInfo.is_done = 2
        orderAidacneInfo = dbOperation.addTokenToSql(orderAidacneInfo)
        if not orderAidacneInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)

    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 查看详情
@app.route("/getOrderAidanceInfo", methods=["POST"])
@jwt_required
def getOrderAidanceInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonData(resultDict)
    itemInfo = None
    userInfo = None
    table = findById(Aidance, "id", id)
    orderAidanceInfo = findById(OrderAidance, "id", table.service_id)
    if orderAidanceInfo:
        orderNo = orderAidanceInfo.pre_order_no
        # orderInfo = findById(UserOrder, "order_no", orderNo, isStrcheck=True)
        orderInfo = UserOrder.query.filter(UserOrder.order_no==orderNo).first()
        serviceInfo = findById(OrderService, "order_no", orderNo, isStrcheck=True)
        if orderInfo:
            userInfo = findById(MemberBases, "user_id", orderInfo.user_id)
        if serviceInfo:
            itemInfo = findById(Item, 'item_id', serviceInfo.item_id)
    else:
        resultDict = returnErrorMsg(errorCode["query_fail"])
        return jsonData(resultDict)
    _memberInfo = {
        "id": "",
        "userId": "",
        "isCheck": "",
        "memberName": "",
        "memberType": "",
        "memberCode": "",
        "invitedCode": "",
        "memberFavoriteCount": "",
        "memberPoints": "",
        "memberBalance": "",
        "isVip": "",
        "memberExpired": "",
        "memberContactEmail": "",
        "memberContactPerson": "",
        "memberContactPhone": "",
        "enterpriseId": "",
        "figureId": "",
        "areaCode": "",
        "memberCreditCode": "", }
    _orderDict = {
        "orderId": "",
        "orderNo": "",
        "orderType": "",
        "orderFrom": "",
        "orderStatus": "",
        "declareStatus": "",
        "orderAddIp": "",
        "orderAddTime": "",
        "serviceId": "",
        "contactPerson": "",
        "contactPhone": "",
        "contactEmail": "",
        "orderMessage": "",
        "orderAmount": "",
        "payableAmount": "",
        "realAmount": "",
        "orderPoint": "",
        "isCoupon": "",
        "isInvoice": "",
        "isComment": "",
        "userId": "",

    }
    _serviceDict = {
        "id": "",
        "orderNo": "",
        "itemId": "",
        "serviceName": "",
        "policySource": "",
        "servicePrice": "",
        "serviceStarttime": "",
        "serviceDeadline": "",
        "directionName": "",
        "serviceContent": "",
        "sheetContent": "",
        "materialList": "",
        "forecastPath": "",
        "serviceContactPerson": "",
        "serviceContactPhone": "",
        "isSecular": "",
        "isEvaluate": "",
        "declareList": "",
        "createTime": "",
        "categoryType": "",
        "servciceProcess": "",

    }
    _itemDict = {
        "itemId": "",
        "deptName": "",
        "levelCode": "",
        "categoryName": "",
        "areaCode": "",
        "itemUrl": "",
        "itemTitle": "",
        "itemImgurl": "",
        "itemPulishdate": "",
        "itemType": "",
        "itemSort": "",
        "isTop": "",
        "isLock": "",
        "isService": "",
        "isContentJson": "",
        "createTime": "",
        "isClose": "",
        "itemDeadline": "",
        "isSecular": "",
        "mediaType": "",
        "mediaUrl": "", }
    if itemInfo:
        _itemDict = {
            "itemId": itemInfo.item_id,
            "deptName": itemInfo.dept_name,
            "levelCode": itemInfo.level_code,
            "categoryName": itemInfo.category_name,
            "areaCode": itemInfo.area_code,
            "itemUrl": itemInfo.item_url,
            "itemTitle": itemInfo.item_title,
            "itemImgurl": itemInfo.item_imgurl,
            "itemPulishdate": itemInfo.item_pulishdate,
            "itemType": itemInfo.item_type,
            "itemSort": itemInfo.item_sort,
            "isTop": itemInfo.is_top,
            "isLock": itemInfo.is_lock,
            "isService": itemInfo.is_service,
            "isContentJson": itemInfo.is_content_json,
            # "createTime": itemInfo.create_time,
            "isClose": itemInfo.is_close,
            "itemDeadline": itemInfo.item_deadline,
            "isSecular": itemInfo.is_secular,
            "mediaType": itemInfo.media_type,
            "mediaUrl": itemInfo.media_url
        }
    if serviceInfo:
        _serviceDict = {
            "id": serviceInfo.id,
            # "orderNo": serviceInfo.order_no,
            # "itemId": serviceInfo.item_id,
            "serviceName": serviceInfo.service_name,
            "policySource": serviceInfo.policy_source,
            "servicePrice": str(serviceInfo.service_price),
            "serviceStarttime": serviceInfo.service_starttime,
            "serviceDeadline": serviceInfo.service_deadline,
            "directionName": serviceInfo.direction_name,
            "serviceContent": serviceInfo.service_content,
            "sheetContent": serviceInfo.sheet_content,
            "materialList": serviceInfo.material_list,
            "forecastPath": serviceInfo.forecast_path,
            "serviceContactPerson": serviceInfo.service_contact_person,
            "serviceContactPhone": serviceInfo.service_contact_phone,
            # "isSecular": serviceInfo.is_secular,
            "isEvaluate": serviceInfo.is_evaluate,
            "declareList": serviceInfo.declare_list,
            "createTime": serviceInfo.create_time,
            "categoryType": serviceInfo.category_type,
            "servciceProcess": serviceInfo.servcice_process,
        }
    if orderInfo:
        _orderDict = {
            "orderId": orderInfo.order_id,
            "orderNo": orderInfo.order_no,
            "orderType": orderInfo.order_type,
            "orderFrom": orderInfo.order_from,
            "orderStatus": orderInfo.order_status,
            "declareStatus": orderInfo.declare_status,
            "orderAddIp": orderInfo.order_add_ip,
            "orderAddTime": orderInfo.order_add_time,
            "serviceId": orderInfo.service_id,
            "contactPerson": orderInfo.contact_person,
            "contactPhone": orderInfo.contact_phone,
            "contactEmail": orderInfo.contact_email,
            "orderMessage": orderInfo.order_message,
            "orderAmount": str(orderInfo.order_amount),
            "payableAmount": str(orderInfo.payable_amount),
            "realAmount": str(orderInfo.real_amount),
            "orderPoint": orderInfo.order_point,
            "isCoupon": orderInfo.is_coupon,
            "isInvoice": orderInfo.is_invoice,
            "isComment": orderInfo.is_comment,
            "userId": orderInfo.user_id,
        }
    if userInfo:
        _memberInfo = {
            "userId": userInfo.user_id,
            "memberName": userInfo.member_name,
            "memberType": userInfo.member_type,
            "memberContactEmail": userInfo.member_contact_email,
            "memberContactPerson": userInfo.member_contact_person,
            "memberContactPhone": userInfo.member_contact_phone,
            "areaCode": userInfo.area_code,
            "memberCreditCode": userInfo.member_credit_code,
        }
    infoDict = dict(dict(dict(_orderDict, **_memberInfo), **_itemDict), **_serviceDict)
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


def tableSort(table):
    _infoDict = {"id": table.id,
                 "taskId": table.task_id,
                 "serviceNo": table.service_no,
                 "preOrderNo": table.pre_order_no,
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
                 "serviceNo": tableData[2],
                 "preOrderNo": tableData[3],
                 "createPerson": tableData[4],
                 "createTime": tableData[5],
                 "executePerson": tableData[6],
                 "executeTime": tableData[7],
                 "isDone": tableData[8], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def viewTableSortDict(tableData):
    _infoDict = {
        "id": tableData[0],
        "taskId": tableData[1],
        "serviceNo": tableData[2],
        "preOrderNo": tableData[3],
        "createPerson": tableData[4],
        "createTime": tableData[5],
        "executePerson": tableData[6],
        "executeTime": tableData[7],
        "isDone": tableData[8],
        "contactPerson": tableData[9],
        "contactPhone": tableData[10],
        "contactEmail": tableData[11],
        "itemTitle": tableData[12],
        "memberName": tableData[13],
        "memberContactEmail": tableData[14],
        "memberContactPerson": tableData[15],
        "memberContactPhone": tableData[16],
    }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


viewChangeDict = {
    "id": "id",
    "taskId": "task_id",
    "serviceNo": "service_no",
    "preOrderNo": "pre_order_no",
    "createPerson": "create_person",
    "createTime": "create_time",
    "executePerson": "execute_person",
    "executeTime": "execute_time",
    "isDone": "is_done",
    "contactPerson": "contact_person",
    "contactPhone": "contact_phone",
    "contactEmail": "contact_email",
    "itemTitle": "item_title",
    "memberName": "member_name",
    "memberContactEmail": "member_contact_email",
    "memberContactPerson": "member_contact_person",
    "memberContactPhone": "member_contact_phone",
}




view_aidance_order_task_change = {
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
    "serviceNo": "service_no",
    "preOrderNo": "pre_order_no",
    "name": "name",
    "desc": "desc",
    "num": "num",
    "orderType": "order_type",
    "orderFrom": "order_from",
    "orderStatus": "order_status",
    "declareStatus": "declare_status",
    "dataServiceId": "data_service_id",
    "contactPerson": "contact_person",
    "contactPhone": "contact_phone",
    "contactEmail": "contact_email",
    "orderMessage": "order_message",
    "orderAmount": "order_amount",
    "payableAmount": "payable_amount",
    "realAmount": "real_amount",
    "orderPoint": "order_point",
    "isCoupon": "is_coupon",
    "isInvoice": "is_invoice",
    "isComment": "is_comment",
    "userId": "user_id",
    "orderAddTime": "order_add_time",
    "submitTime": "submit_time",
    "submitPerson": "submit_person",
    "checkStatus": "check_status",
    "checkTime": "check_time",
    "checkPerson": "check_person",
    "checkRemark": "check_remark",
    "sort": "sort",
}

def view_aidance_order_task_fun(tableData):
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
        "serviceNo": tableData[17],
        "preOrderNo": tableData[18],
        "name": tableData[19],
        "desc": tableData[20],
        "num": tableData[21],
        "orderType": tableData[22],
        "orderFrom": tableData[23],
        "orderStatus": tableData[24],
        "declareStatus": tableData[25],
        "dataServiceId": tableData[26],
        "contactPerson": tableData[27],
        "contactPhone": tableData[28],
        "contactEmail": tableData[29],
        "orderMessage": tableData[30],
        "orderAmount": str(tableData[31]),
        "payableAmount": str(tableData[32]),
        "realAmount": str(tableData[33]),
        "orderPoint": tableData[34],
        "isCoupon": tableData[35],
        "isInvoice": tableData[36],
        "isComment": tableData[37],
        "userId": tableData[38],
        "orderAddTime": tableData[39],
        "submitTime": tableData[40],
        "submitPerson": tableData[41],
        "checkStatus": tableData[42],
        "checkTime": tableData[43],
        "checkPerson": tableData[44],
        "checkRemark": tableData[45],
        "sort": tableData[46],
        "orderNo": tableData[18],
    }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict