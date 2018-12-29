# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Order.UserOrderEdit import UserOrderEdit, UserOrderEditChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog
from Res import StatusCode, IsSend, IsClose, AcceptCode, AssignCode, AuditCode
from models.Order.UserOrder import UserOrder
from common.DatatimeNow import getTimeStrfTimeStampNow, getTimeStampNow, getTimeToStrfdate
import random
from models.Order.UserOrderAccept import UserOrderAccept
from models.Order.UserOrderCancel import UserOrderCancel
from models.Order.UserOrderAssign import UserOrderAssign, UserOrderAssignChangeDic as AssignChangeDic
from models.Order.DeclareProgress import DeclareProgress
from common.OrderCommon import addDeclareStatus,createServiceNo,getRandomIntCode

# 获取 列表
@app.route("/findUserOrderEditByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_edit')
def findUserOrderEditBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [{
        "field": "counselorId",
        "op": "equal",
        "value": current_user.admin_id
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = UserOrderEdit.__tablename__
    intColumnClinetNameList = [u'id', u'editStatus', u'auditStatus', u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, UserOrderEditChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "specificFund": str(tableData[4]),
                        "editStatus": tableData[5],
                        "editRemark": tableData[6],
                        "auditPerson": tableData[7],
                        "auditTime": tableData[8],
                        "auditStatus": tableData[9],
                        "auditRemark": tableData[10],
                        "counselorId": tableData[11],
                        "manageCounselorId": tableData[12],
                        "requireList": tableData[13],
                        "manuscriptTime": tableData[14],
                        "declareName": tableData[15],
                        "editTime": tableData[16],
                        "editAnnex": tableData[17],
                        "itemContent": itemContent,
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

# 获取 列表
@app.route("/findFBUserOrderEditByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_edit')
def findFBUserOrderEditByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [{
        "field": "manageCounselorId",
        "op": "equal",
        "value": current_user.admin_id
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = UserOrderEdit.__tablename__
    intColumnClinetNameList = [u'id', u'editStatus', u'auditStatus', u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, UserOrderEditChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "specificFund": str(tableData[4]),
                        "editStatus": tableData[5],
                        "editRemark": tableData[6],
                        "auditPerson": tableData[7],
                        "auditTime": tableData[8],
                        "auditStatus": tableData[9],
                        "auditRemark": tableData[10],
                        "counselorId": tableData[11],
                        "manageCounselorId": tableData[12],
                        "requireList": tableData[13],
                        "manuscriptTime": tableData[14],
                        "declareName": tableData[15],
                        "editTime": tableData[16],
                        "editAnnex": tableData[17],
                        "itemContent": itemContent,
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

# 获取详情 
@app.route("/getUserOrderEditDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_edit')
def getUserOrderEditDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserOrderEdit, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "orderNo": table.order_no,
                "serviceNo": table.service_no,
                "itemTitle": table.item_title,
                "specificFund": table.specific_fund,
                "editStatus": table.edit_status,
                "editRemark": table.edit_remark,
                "auditPerson": table.audit_person,
                "auditTime": table.audit_time,
                "auditStatus": table.audit_status,
                "auditRemark": table.audit_remark,
                "counselorId": table.counselor_id,
                "manageCounselorId": table.manage_counselor_id,
                "requireList": table.require_list,
                "manuscriptTime": table.manuscript_time,
                "declareName": table.declare_name,
                "editTime": table.edit_time,
                "editAnnex": table.edit_annex, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserOrderEdit", methods=["POST"])
@jwt_required
@deleteLog('zzh_user_order_edit')
def deleteUserOrderEdit():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserOrderEdit, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserOrderEdit", methods=["POST"])
@jwt_required
@addLog('zzh_user_order_edit')
def addUserOrderEdit():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("orderNo", None), dataDict.get("serviceNo", None), dataDict.get("itemTitle", None),
                 dataDict.get("specificFund", None), dataDict.get("editStatus", None), dataDict.get("editRemark", None),
                 dataDict.get("auditPerson", None), dataDict.get("auditTime", None), dataDict.get("auditStatus", None),
                 dataDict.get("auditRemark", None), dataDict.get("counselorId", None),
                 dataDict.get("manageCounselorId", None), dataDict.get("requireList", None),
                 dataDict.get("manuscriptTime", None), dataDict.get("declareName", None),
                 dataDict.get("editTime", None), dataDict.get("editAnnex", None))
    table = insertToSQL(UserOrderEdit, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataUserOrderEdit", methods=["POST"])
@jwt_required
@updateLog('zzh_user_order_edit')
def updataUserOrderEdit():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    serviceNo = dataDict.get("serviceNo", None)
    editStatus = dataDict.get("editStatus", None)
    specificFund = dataDict.get("specificFund", None)
    manuscriptTime = dataDict.get("manuscriptTime", None)
    declareName = dataDict.get("declareName", None)

    if editStatus == 2:
        if not (serviceNo and editStatus):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
    else:
        if not (serviceNo and editStatus and manuscriptTime and declareName):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)

    table = findById(UserOrderEdit, "service_no", serviceNo, isStrcheck=True)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if table.audit_status == 1:
        resultDict = returnMsg("审核中")
        return jsonify(resultDict)

    columnId = "service_no"
    intColumnClinetNameList = ("id", "editStatus", "auditStatus", "counselorId", "manageCounselorId", "specificFund")
    dataDict["auditStatus"] = 1
    dataDict["editTime"] = getTimeStrfTimeStampNow()
    menuUp = updataById(UserOrderEdit, dataDict, columnId, serviceNo, UserOrderEditChangeDic, intColumnClinetNameList,
                        isIsInt=False)
    if menuUp == None:
        resultDict = returnErrorMsg()
    elif menuUp == 0:
        resultDict = returnErrorMsg(errorCode["param_error"])
    else:
        # infoDict =
        resultDict = returnMsg({})
    return jsonify(resultDict)


# 审核
@app.route("/checkIsUserOrderEdit", methods=["POST"])
@jwt_required
def checkIsUserOrderEdit():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    idList = dataDict.get("ids", [])
    auditStatus = dataDict.get("auditStatus", None)
    isClose = dataDict.get("isClose", None)
    if isClose:
        dataDict.pop("isClose")
    failList = []
    if not (idList and auditStatus):
        resultDict = returnErrorMsg("not find ids and auditStatus!")
        return jsonify(resultDict)
    dataDict.pop("ids")
    columnId = "id"
    intColumnClinetNameList = ("id", "editStatus", "auditStatus")

    adminTable = current_user
    adminName = adminTable.admin_name
    dateTimeNow = getTimeStrfTimeStampNow()
    if auditStatus != None:
        dataDict["auditTime"] = str(dateTimeNow)
        dataDict["auditPerson"] = adminName

    dbOperation = OperationOfDB()
    for id in idList:
        menuUp = findById(UserOrderEdit, "id", id)
        if menuUp == 0:
            resultDict = returnErrorMsg("not find this id")
            return jsonify(resultDict)
        elif menuUp == None:
            resultDict = returnErrorMsg
            return jsonify(resultDict)

        # 材料成功审核
        if menuUp.edit_status == StatusCode["pass"]:
            # 审核通过 创建下一级表
            if auditStatus == AuditCode["pass"]:
                columnsStr = (
                    menuUp.order_no, menuUp.service_no, menuUp.item_title, menuUp.specific_fund, 0, 0,
                    menuUp.declare_name, None, 0, None, None, None, 0, None, menuUp.counselor_id,
                    menuUp.manage_counselor_id, None, menuUp.require_list, None)
                auditTable = dbOperation.insertToSQL(UserOrderAccept, *columnsStr)
                if not auditTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("insert UserOrderAccept failed")
                    return jsonify(resultDict)
                declareTable = addDeclareStatus(menuUp.order_no, dbOperation, "0000001111")
                if not declareTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not update fail")
                    return jsonify(resultDict)
            elif auditStatus == AuditCode["fail"]:
                dataDict["editStatus"] = 0
            else:
                resultDict = returnMsg("")
                return jsonify(resultDict)
        # 合同失败审核
        elif menuUp.edit_status == StatusCode["fail"]:
            # 审核通过 关闭订单
            if auditStatus == AuditCode["pass"]:
                # 关闭订单
                if isClose == IsClose["close"]:
                    # 订单关闭表
                    cancelIp = request.remote_addr
                    cancel_time = getTimeStrfTimeStampNow()
                    columnsStr = (
                        menuUp.order_no, 1, dataDict.get("auditRemark", None), cancel_time, cancelIp, 0, None, None,
                        None)
                    userOrderContractTable = dbOperation.insertToSQL(UserOrderCancel, *columnsStr)
                    if not userOrderContractTable:
                        dbOperation.commitRollback()
                        resultDict = returnErrorMsg("insert UserOrderEdit failed")
                        return jsonify(resultDict)
                    # 更新派单表 为关闭订单
                    newDataDict = {"assignStatus": 3}
                    # intColumnClinetNameList = ("id", "counselorId", "manageCounselorId", "assignStatus")
                    service_No = menuUp.service_no
                    UserOrderAssignTable = dbOperation.updateThis(UserOrderAssign, UserOrderAssign.service_no,
                                                                  service_No,
                                                                  newDataDict, AssignChangeDic, isInt=False)
                    if not UserOrderAssignTable:
                        dbOperation.commitRollback()
                        resultDict = returnErrorMsg("updata UserOrderAssign failed")
                        return jsonify(resultDict)
                    declareTable = addDeclareStatus(menuUp.order_no, dbOperation, "0000002111")
                    if not declareTable:
                        dbOperation.commitRollback()
                        resultDict = returnErrorMsg("not update fail")
                        return jsonify(resultDict)
                elif isClose == IsClose["reset"]:
                    # 重新派单
                    newDataDict = {"assignStatus": 3}
                    serviceNo = menuUp.service_no
                    UserOrderAssignTable = dbOperation.updateThis(UserOrderAssign, UserOrderAssign.service_no,
                                                                  serviceNo,
                                                                  newDataDict, AssignChangeDic, isInt=False)
                    if not UserOrderAssignTable:
                        dbOperation.commitRollback()
                        resultDict = returnErrorMsg("updata UserOrderAssign failed")
                        return jsonify(resultDict)
                    # 重新派单 生成新的 订单
                    service_no = createServiceNo(UserOrderAssignTable.order_no)
                    newColumsStr = (
                        UserOrderAssignTable.order_no, service_no, None, UserOrderAssignTable.manage_counselor_id, 2,
                        None,
                        None, None, 1, 0, None)
                    newUserOrderAssignTable = dbOperation.insertToSQL(UserOrderAssign, *newColumsStr)
                    if not newUserOrderAssignTable:
                        dbOperation.commitRollback()
                        resultDict = returnErrorMsg("insert UserOrderAssign failed")
                        return jsonify(resultDict)

                else:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find isClose")
                    return jsonify(resultDict)
            elif auditStatus == AuditCode["fail"]:
                dataDict["editStatus"] = 0
            else:
                dbOperation.commitRollback()
                resultDict = returnMsg("")
                return jsonify(resultDict)
        # 无效
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("not find contract_status")
            return jsonify(resultDict)
        datatimeNow = getTimeStrfTimeStampNow()
        shColumnsStr = (menuUp.order_no, '材料编写阶段', current_user.admin_name, dataDict.get("stageTime", datatimeNow),
                        dataDict.get("stageRemark"))
        shTable = dbOperation.insertToSQL(DeclareProgress, *shColumnsStr)
        if not shTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("insert DeclareProgress failed")
            return jsonify(resultDict)
        # 更新
        menuUp = dbOperation.updateThis(UserOrderEdit, UserOrderEdit.id, id, dataDict, UserOrderEditChangeDic)
        if not menuUp:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("update failed")
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(infoList)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("commit failed")
    return jsonify(resultDict)

