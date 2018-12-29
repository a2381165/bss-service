# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

import Res
from Res import IsSend
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, addTokenToSql
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Counselor.CounselorGroup import CounselorGroup
from models.Order.UserOrder import UserOrder
from models.Order.UserOrderAssess import UserOrderAssess
from models.Order.UserOrderAssign import UserOrderAssign, UserOrderAssignChangeDic as tableChangeDic
from models.Order.UserOrderCancel import UserOrderCancel
from models.Order.UserOrderItem import UserOrderItem
from version.v3.bossConfig import app


# 获取 列表
@app.route("/findUserOrderAssignByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_assign')
def findUserOrderAssignBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # tablename = UserOrderAssign.__tablename__
    condition = dataDict.get("condition")
    newList = [{
        "field": "counselorId",
        "op": "equal",
        "value": current_user.admin_id
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = "view_user_order_assign2"
    intColumnClinetNameList = [u'id', u'counselorId', u'manageCounselorId', u'assignStatus', u'isSend', u'acceptStatus']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            levelCode = 1
            deptName = "海冰部"
            categoryName = "还比u"
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "counselorId": tableData[3],
                        "manageCounselorId": tableData[4],
                        "assignStatus": tableData[5],
                        "assignPerson": tableData[6],
                        "assignTime": tableData[7],
                        "remark": tableData[8],
                        "isSend": tableData[9],
                        "acceptStatus": tableData[10],
                        "returnRemark": tableData[11],
                        "adminName": tableData[12],
                        "adminDesc": tableData[13],
                        "adminRealName": tableData[14],
                        "adminTelephone": tableData[15],
                        "adminEmail": tableData[16],
                        "adminAddTime": tableData[17],
                        "isLock": tableData[18],
                        "ozId": tableData[19],
                        "orderType": tableData[20],
                        "orderStatus": tableData[21],
                        "declareStatus": tableData[22],
                        "orderAddIp": tableData[23],
                        "orderAddTime": tableData[24],
                        "orderItemId": tableData[25],
                        "orderServiceId": tableData[26],
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
                        "isCheck": tableData[39],
                        "memberName": tableData[40],
                        "memberType": tableData[41],
                        "memberCode": tableData[42],
                        "invitedCode": tableData[43],
                        "memberFavoriteCount": tableData[44],
                        "memberPoints": tableData[45],
                        "memberBalance": tableData[46],
                        "isVip": tableData[47],
                        "memberExpired": tableData[48],
                        "memberContactEmail": tableData[49],
                        "memberContactPerson": tableData[50],
                        "memberContactPhone": tableData[51],
                        "enterpriseId": tableData[52],
                        "figureId": tableData[53],
                        "areaCode": tableData[54],
                        "memberCreditCode": tableData[55],
                        "itemUrl": tableData[56],
                        "itemTitle": tableData[57],
                        "itemImgurl": tableData[58],
                        "itemPricerange": tableData[59],
                        "itemPulishdate": tableData[60],
                        "itemDeadline": tableData[61],
                        "itemContact": tableData[62],
                        "itemSubmitAddress": tableData[63],
                        "itemType": tableData[64],
                        "itemContent": tableData[65],
                        "deptId": tableData[66],
                        "itemId": tableData[67],
                        "levelCode": levelCode,
                        "deptName": deptName,
                        "categoryName": categoryName,
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getUserOrderAssignDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_assign')
def getUserOrderAssignDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserOrderAssign, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "orderNo": table.order_no,
                "serviceNo": table.service_no,
                "counselorId": table.counselor_id,
                "manageCounselorId": table.manage_counselor_id,
                "assignStatus": table.assign_status,
                "assignPerson": table.assign_person,
                "assignTime": table.assign_time,
                "remark": table.remark,
                "isSend": table.is_send,
                "acceptStatus": table.accept_status,
                "returnRemark": table.return_remark, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserOrderAssign", methods=["POST"])
@jwt_required
@deleteLog('zzh_user_order_assign')
def deleteUserOrderAssign():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserOrderAssign, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserOrderAssign", methods=["POST"])
@jwt_required
@addLog('zzh_user_order_assign')
def addUserOrderAssign():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("orderNo", None), dataDict.get("serviceNo", None), dataDict.get("counselorId", None),
                 dataDict.get("manageCounselorId", None), dataDict.get("assignStatus", None),
                 dataDict.get("assignPerson", None), dataDict.get("assignTime", None), dataDict.get("remark", None),
                 dataDict.get("isSend", None), dataDict.get("acceptStatus", None), dataDict.get("returnRemark", None))
    table = insertToSQL(UserOrderAssign, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataUserOrderAssign", methods=["POST"])
@jwt_required
@updateLog('zzh_user_order_assign')
def updataUserOrderAssign():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'counselorId', u'manageCounselorId', u'assignStatus', u'isSend', u'acceptStatus']
    table = updataById(UserOrderAssign, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 接收订单 拒绝订单
@app.route("/acceptUserOrderAssign", methods=["POST"])
@jwt_required
def updateUserOrderAssign():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    # orderNo = dataDict.get("orderNo", None)
    serviceNo = dataDict.get("serviceNo", None)
    acceptStatus = dataDict.get("acceptStatus", None)
    returnRemark = dataDict.get("returnRemark", "")
    if not (serviceNo and acceptStatus):
        resultDict = returnErrorMsg("not find serviceNo or acceptStatus !")
        return jsonify(resultDict)

    assignStatus = dataDict.get("assignStatus", 0)
    if assignStatus != 0:
        dataDict.pop("assignStatus")

    columnId = "id"
    intColumnClinetNameList = ("id", "counselorId", "manageCounselorId", "assignStatus")
    # for id in idList:
    #     menuUp = updataById(UserOrderAssign, dataDict, columnId, id, UserOrderAssignChangeDic, intColumnClinetNameList)
    #     if menuUp == None:
    #         resultDict = returnErrorMsg()
    #         return jsonify(resultDict)
    #     elif menuUp == 0:
    #         resultDict = returnErrorMsg("the id not exit!")
    #         return jsonify(resultDict)
    #     else:
    #         infoDict = tableDictSort(menuUp)
    #         infoList.append(infoDict)
    # resultDict = returnMsg(infoList)
    # return jsonify(resultDict)
    dbOperation = OperationOfDB()
    menuUp = dbOperation.updateThis(UserOrderAssign, UserOrderAssign.service_no, serviceNo, dataDict,
                                    tableChangeDic, isInt=False)
    if not menuUp:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("update failed")
        return jsonify(resultDict)
    else:
        # 1 派单成功

        if acceptStatus == Res.AcceptCode["pass"]:
            userOrderItemTable = UserOrderItem.query.filter(UserOrderItem.order_no == menuUp.order_no).first()
            if userOrderItemTable:
                columnsStr = (
                    menuUp.order_no, menuUp.service_no, userOrderItemTable.item_title, userOrderItemTable.item_url,
                    0, None, None, None, menuUp.counselor_id, menuUp.manage_counselor_id, 0)
                userOrderAssessTable = dbOperation.insertToSQL(UserOrderAssess, *columnsStr)
                if userOrderAssessTable:
                    infoDict = tableDictSort(menuUp)
                    infoList.append(infoDict)
                else:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("insert userOrderAssess failed please check userOrderAssess info!")
                    return jsonify(resultDict)
            else:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("please check UserOrderItem info!")
                return jsonify(resultDict)
        elif acceptStatus == Res.AcceptCode["fail"]:
            cancelIp = request.remote_addr
            cancel_time = getTimeStrfTimeStampNow()

            columnsStr = (
                menuUp.order_no, 1, returnRemark, cancel_time, cancelIp, 0, None, None, None)
            userOrderCancelTable = dbOperation.insertToSQL(UserOrderCancel, *columnsStr)
            if not userOrderCancelTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("not find table")
                return resultDict
            orderTable = UserOrder.query.filter(UserOrder.order_no == menuUp.order_no).first()
            orderTable.declare_status = "0000000002"
            orderTable = addTokenToSql(orderTable)
            if not orderTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["update_fail"])
                return jsonify(resultDict)
            infoDict = tableDictSort(menuUp)
            infoList.append(infoDict)
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("please check UserOrderItem info!")
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(infoList)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("commit failed")
    return jsonify(resultDict)


# 选择咨询师
# 通过条件筛选
@app.route("/findCounselorManageByCondition", methods=["POST"])
@jwt_required
def findCounselorManageByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    orderNo = dataDict.get("orderNo")
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    manageId = get_jwt_identity()

    counselorGroupTable = CounselorGroup.query.filter(CounselorGroup.admin_id == manageId).first()
    if counselorGroupTable:
        groupId = counselorGroupTable.group_id
        addDict = {}
        addDict["field"] = "groupId"
        addDict["op"] = "equal"
        addDict["value"] = groupId
        dataDict.get("condition").append(addDict)
    # roleInfo = AdminRole.query.filter(AdminRole.admin_id == manageId).first()
    # if roleInfo:
    #     if roleInfo.role_id != 1:
    #         addDict = {}
    #         addDict["field"] = "manageCounselorId"
    #         addDict["op"] = "equal"
    #         addDict["value"] = manageId
    #         dataDict.get("condition").append(addDict)
    intColumnClinetNameList = ("id", "groupId", "counselorId")

    # tableName = CounselorManage.__tablename__
    tableName = "view_counselor_manager_bases_robing"
    tableList, count = conditionDataListFind(dataDict, viewManageChange, intColumnClinetNameList, tableName)
    if tableList:
        InfoList = []
        for tableData in tableList:
            isRobbing = 0
            if tableData[18]:
                isRobbing = 1
            infoDict = {
                "id": tableData[0],
                "groupId": tableData[1],
                "counselorId": tableData[2],
                "counselorType": tableData[3],
                "invitedCode": tableData[4],
                "counselorCode": tableData[5],
                "counselorPoints": tableData[6],
                "counselorBalance": str(tableData[7]),
                "isPaymentAccount": tableData[8],
                "isCheck": tableData[9],
                "counselorContactEmail": tableData[10],
                "counselorContactPerson": tableData[11],
                "counselorContactPhone": tableData[12],
                "areaCode": tableData[13],
                "counselorPersonId": tableData[14],
                "counselorEnterpriseId": tableData[15],
                "counselorName": tableData[16],
                "counselorRank": tableData[17],
                "orderNo": tableData[18],
                "robbingTime": tableData[19],
                "isRobbing": isRobbing,
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 派单给咨询师
@app.route("/assignUserOrderAssign", methods=["POST"])
@jwt_required
def assignUserOrderAssign():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    isSend = dataDict.get("isSend", None)
    counselorId = dataDict.get("counselorId", None)
    manageId = get_jwt_identity()
    columnId = "id"
    intColumnClinetNameList = ("id", "counselorId", "manageCounselorId", "assignStatus", "isSend", "acceptStatus")
    infoList = []
    idList = dataDict.get("ids", None)
    if not (idList):
        resultDict = returnErrorMsg("not find ids or assignStatus!")
        return jsonify(resultDict)
    adminId = get_jwt_identity()
    if not counselorId and isSend == IsSend["fail"]:
        # 分发不通过 返回上一层
        for id in idList:
            table = UserOrderAssign.query.filter(UserOrderAssign.id == id).first()
            if not table:
                resultDict = returnErrorMsg("not find assignTable")
                return jsonify(resultDict)
            table.is_send = 0
            hasTable = addTokenToSql(table)
            if hasTable:
                resultDict = returnMsg({})
            else:
                resultDict = returnErrorMsg("update fail")
            return jsonify(resultDict)

    infoList = []
    dateTimeNow = getTimeStrfTimeStampNow()
    if isSend == IsSend["pass"]:
        adminTable = current_user
        adminName = adminTable.admin_name
        dataDict["assignTime"] = dateTimeNow
        dataDict["assignPerson"] = adminName
    dataDict["manageCounselorId"] = manageId
    dataDict["acceptStatus"] = 1
    resultDict = update(idList, dataDict, infoList)
    return jsonify(resultDict)


def update(idList, dataDict, infoList):
    columnId = "id"
    intColumnClinetNameList = ("id", "counselorId", "manageCounselorId", "assignStatus", "isSend", "acceptStatus")
    for id in idList:
        menuUp = updataById(UserOrderAssign, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if menuUp == None:
            resultDict = returnErrorMsg()
            return resultDict
        elif menuUp == 0:
            resultDict = returnErrorMsg("the id not exit!")
            return resultDict
        else:
            dbOperation = OperationOfDB()
            if dataDict.get("assignStatus", None) == 3:
                cancelIp = request.remote_addr
                cancel_time = getTimeStrfTimeStampNow()
                columnsStr = (
                    menuUp.order_no, 1, dataDict.get("auditRemark", None), cancel_time, cancelIp, 0, None, None, None)
                userOrderCancelTable = dbOperation.insertToSQL(UserOrderCancel, *columnsStr)
                if not userOrderCancelTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find table")
                    return resultDict
                orderTable = UserOrder.query.filter(UserOrder.order_no == menuUp.order_no).first()
                orderTable.declare_status = "0000000002"
                addTokenToSql(orderTable)
                infoDict = tableDictSort(menuUp)
                infoList.append(infoDict)
            else:
                orderTable = UserOrder.query.filter(UserOrder.order_no == menuUp.order_no).first()
                orderTable.declare_status = "0000000001"
                addTokenToSql(orderTable)
                infoDict = tableDictSort(menuUp)
                infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return resultDict


# # 接收订单 拒绝订单
# @app.route("/resetAcceptUserOrderAssign", methods=["POST"])
# @jwt_required
# def resetAcceptUserOrderAssign():
#     counselorId = get_jwt_identity()
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     infoList = []
#     orderNo = dataDict.get("orderNo", None)
#     serviceNo = dataDict.get("serviceNo", None)
#     acceptStatus = dataDict.get("acceptStatus", None)
#     if not (serviceNo and acceptStatus):
#         resultDict = returnErrorMsg("not find ids or acceptStatus !")
#         return jsonify(resultDict)
#
#     assignStatus = dataDict.get("assignStatus", 0)
#     if assignStatus != 0:
#         dataDict.pop("assignStatus")
#
#     columnId = "id"
#     intColumnClinetNameList = ("id", "counselorId", "manageCounselorId", "assignStatus")
#     # for id in idList:
#     #     menuUp = updataById(UserOrderAssign, dataDict, columnId, id, UserOrderAssignChangeDic, intColumnClinetNameList)
#     #     if menuUp == None:
#     #         resultDict = returnErrorMsg()
#     #         return jsonify(resultDict)
#     #     elif menuUp == 0:
#     #         resultDict = returnErrorMsg("the id not exit!")
#     #         return jsonify(resultDict)
#     #     else:
#     #         infoDict = tableDictSort(menuUp)
#     #         infoList.append(infoDict)
#     # resultDict = returnMsg(infoList)
#     # return jsonify(resultDict)
#     dbOperation = OperationOfDB()
#     menuUp = dbOperation.updateThis(UserOrderAssign, UserOrderAssign.service_no, serviceNo, dataDict,
#                                     tableChangeDic, isInt=False)
#
#     # UserOrderEdit
#     if not menuUp:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg("update failed")
#         return jsonify(resultDict)
#     else:
#         # 1 派单成功
#         if acceptStatus == Res.AcceptCode["pass"]:
#             orderNo = menuUp.order_no
#             userOrderItemTable = UserOrderItem.query.filter(UserOrderItem.order_no == menuUp.order_no).first()
#             if userOrderItemTable:
#                 assesTable = UserOrderAssess.query.filter(UserOrderAssess.order_no == orderNo,
#                                                           UserOrderAssess.service_no != serviceNo).order_by(
#                     UserOrderAssess.assess_time.desc()).first()
#                 contractTable = UserOrderContract.query.filter(UserOrderContract.order_no == orderNo,
#                                                                UserOrderContract.service_no != serviceNo).order_by(
#                     UserOrderContract.audit_time.desc()).first()
#                 counselorContractTable = CounselorContract.query.filter(CounselorContract.order_no == orderNo,
#                                                                         CounselorContract.service_no != serviceNo,
#                                                                         CounselorContract.contract_status != -1).first()
#                 amountCheckTable = CounselorOrderAmountCheck.query.filter(
#                     CounselorOrderAmountCheck.service_no == serviceNo).first()
#                 if counselorContractTable:
#                     counselorContractTable.contract_status = -1
#                     counselorContractTable = dbOperation.addTokenToSql(counselorContractTable)
#                 if assesTable and contractTable and amountCheckTable:
#                     declareTable = addDeclareStatus(menuUp.order_no, dbOperation, "0000000111")
#                     if not declareTable:
#                         dbOperation.commitRollback()
#                         resultDict = returnErrorMsg("not update fail")
#                         return jsonify(resultDict)
#
#                     # 新评估表
#                     assessColumnsStr = (
#                         orderNo, serviceNo, assesTable.item_title, assesTable.item_url, assesTable.assess_status,
#                         assesTable.assess_person, assesTable.assess_time, assesTable.assess_remark, counselorId,
#                         assesTable.manage_counselor_id, assesTable.require_list)
#                     newAssessTable = dbOperation.insertToSQL(UserOrderAssess, *assessColumnsStr)
#                     # 新合同表
#                     contractColumnsStr = (
#                         orderNo, serviceNo, contractTable.item_title, contractTable.contract_no,
#                         contractTable.contract_status,
#                         contractTable.contract_annex, contractTable.contract_remark, contractTable.audit_person,
#                         contractTable.audit_time, contractTable.audit_status, contractTable.audit_remark, counselorId,
#                         contractTable.manage_counselor_id, contractTable.contract_type, contractTable.contract_price,
#                         contractTable.start_fee, contractTable.project_fee, contractTable.counselor_start_fee,
#                         contractTable.counselor_accept_fee, contractTable.counselor_project_fee,
#                         contractTable.project_rate,
#                         contractTable.counselor_project_rate, contractTable.is_generate)
#                     newContractTable = dbOperation.insertToSQL(UserOrderContract, *contractColumnsStr)
#                     # 新 收款表
#                     counselorTable = CounselorAccountCertification.query.filter(
#                         CounselorAccountCertification.counselor_id == counselorId).first()
#                     if not counselorTable:
#                         dbOperation.commitRollback()
#                         resultDict = returnErrorMsg("not find this counselor")
#                         return jsonify(resultDict)
#                     payment_method = counselorTable.counselor_receipt_method
#                     payment_money = contractTable.counselor_start_fee
#                     amountColumnsStr = (
#                         orderNo, 1, payment_method, counselorTable.counselor_payee,
#                         counselorTable.counselor_receipt_bank,
#                         counselorTable.counselor_receipt_account, None, payment_money, None, None, 0, None, 1, None,
#                         None, None, serviceNo)
#                     amountTable = dbOperation.insertToSQL(CounselorOrderAmountCheck, *amountColumnsStr)
#
#                     # 新 编写表
#                     columnsStr = (
#                         orderNo, serviceNo, assesTable.item_title, None, 0, None, None, None, 0, None,
#                         counselorId, menuUp.manage_counselor_id, None, None, None, None, None)
#                     OrderEditTable = dbOperation.insertToSQL(UserOrderEdit, *columnsStr)
#
#                     if not (newAssessTable and newContractTable and OrderEditTable and amountTable):
#                         dbOperation.commitRollback()
#                         resultDict = returnErrorMsg("insert fail")
#                         return jsonify(resultDict)
#                         # columnsStr = (
#                         #     menuUp.order_no, menuUp.service_no, userOrderItemTable.item_title, userOrderItemTable.item_url,
#                         #     0, None, None, None, menuUp.counselor_id, menuUp.manage_counselor_id, None)
#                         # userOrderAssessTable = dbOperation.insertToSQL(UserOrderAssess, *columnsStr)
#                         # if userOrderAssessTable:
#                         #     infoDict = tableDictSort(menuUp)
#                         #     infoList.append(infoDict)
#                         # else:
#                         #     dbOperation.commitRollback()
#                         #     resultDict = returnErrorMsg("insert userOrderAssess failed please check userOrderAssess info!")
#                         #     return jsonify(resultDict)
#             else:
#                 resultDict = returnErrorMsg("please check UserOrderItem info!")
#                 return jsonify(resultDict)
#         else:
#             resultDict = returnErrorMsg("please check UserOrderItem info!")
#             return jsonify(resultDict)
#     if dbOperation.commitToSQL():
#         resultDict = returnMsg(infoList)
#     else:
#         dbOperation.commitRollback()
#         resultDict = returnErrorMsg("commit failed")
#     return jsonify(resultDict)

# 副部长 查询 派单列表
@app.route("/findFBUserOrderAssignByCondition", methods=["POST"])
def findFBUserOrderAssignByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # tablename = UserOrderAssign.__tablename__
    condition = dataDict.get("condition")
    newList = [{
        "field": "manageCounselorId",
        "op": "equal",
        "value": current_user.admin_id
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = "view_user_order_assign2"
    intColumnClinetNameList = [u'id', u'counselorId', u'manageCounselorId', u'assignStatus', u'isSend',
                               u'acceptStatus']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            levelCode = 1
            deptName = "海冰部"
            categoryName = "还比u"
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "counselorId": tableData[3],
                        "manageCounselorId": tableData[4],
                        "assignStatus": tableData[5],
                        "assignPerson": tableData[6],
                        "assignTime": tableData[7],
                        "remark": tableData[8],
                        "isSend": tableData[9],
                        "acceptStatus": tableData[10],
                        "returnRemark": tableData[11],
                        "adminName": tableData[12],
                        "adminDesc": tableData[13],
                        "adminRealName": tableData[14],
                        "adminTelephone": tableData[15],
                        "adminEmail": tableData[16],
                        "adminAddTime": tableData[17],
                        "isLock": tableData[18],
                        "ozId": tableData[19],
                        "orderType": tableData[20],
                        "orderStatus": tableData[21],
                        "declareStatus": tableData[22],
                        "orderAddIp": tableData[23],
                        "orderAddTime": tableData[24],
                        "orderItemId": tableData[25],
                        "orderServiceId": tableData[26],
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
                        "isCheck": tableData[39],
                        "memberName": tableData[40],
                        "memberType": tableData[41],
                        "memberCode": tableData[42],
                        "invitedCode": tableData[43],
                        "memberFavoriteCount": tableData[44],
                        "memberPoints": tableData[45],
                        "memberBalance": tableData[46],
                        "isVip": tableData[47],
                        "memberExpired": tableData[48],
                        "memberContactEmail": tableData[49],
                        "memberContactPerson": tableData[50],
                        "memberContactPhone": tableData[51],
                        "enterpriseId": tableData[52],
                        "figureId": tableData[53],
                        "areaCode": tableData[54],
                        "memberCreditCode": tableData[55],
                        "itemUrl": tableData[56],
                        "itemTitle": tableData[57],
                        "itemImgurl": tableData[58],
                        "itemPricerange": tableData[59],
                        "itemPulishdate": tableData[60],
                        "itemDeadline": tableData[61],
                        "itemContact": tableData[62],
                        "itemSubmitAddress": tableData[63],
                        "itemType": tableData[64],
                        "itemContent": tableData[65],
                        "deptId": tableData[66],
                        "itemId": tableData[67],
                        "levelCode": levelCode,
                        "deptName": deptName,
                        "categoryName": categoryName,
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def tableDictSort(table):
    infoDict = {
        "id": table.id,
        "orderNo": table.order_no,
        "serviceNo": table.service_no,
        "counselorId": table.counselor_id,
        "manageCounselorId": table.manage_counselor_id,
        "assignStatus": table.assign_status,
        "assignPerson": table.assign_person,
        "assignTime": table.assign_time,
        "remark": table.remark
    }
    return infoDict


viewManageChange = {
    "id": "id",
    "groupId": "group_id",
    "counselorId": "counselor_id",
    "counselorType": "counselor_type",
    "invitedCode": "invited_code",
    "counselorCode": "counselor_code",
    "counselorPoints": "counselor_points",
    "counselorBalance": "counselor_balance",
    "isPaymentAccount": "is_payment_account",
    "isCheck": "is_check",
    "counselorContactEmail": "counselor_contact_email",
    "counselorContactPerson": "counselor_contact_person",
    "counselorContactPhone": "counselor_contact_phone",
    "areaCode": "area_code",
    "counselorPersonId": "counselor_person_id",
    "counselorEnterpriseId": "counselor_enterprise_id",
    "counselorName": "counselor_name",
    "counselorRank": "counselor_rank",
    "orderNo": "order_no",
    "robbingTime": "robbing_time",
}
