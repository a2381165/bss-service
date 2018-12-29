# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, current_user

import Res
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.OrderCommon import addDeclareStatus
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Counselor.CounselorAccountCertification import CounselorAccountCertification
from models.Counselor.CounselorOrderAmountCheck import CounselorOrderAmountCheck
from models.Order.DeclareProgress import DeclareProgress
from models.Order.UserOrderAccept import UserOrderAccept, UserOrderAcceptChangeDic as tableChangeDic
from models.Order.UserOrderAssign import UserOrderAssign, UserOrderAssignChangeDic
from models.Order.UserOrderCancel import UserOrderCancel
from models.Order.UserOrderContract import UserOrderContract
from models.Order.UserOrderProject import UserOrderProject
from version.v3.bossConfig import app


# 获取 列表
@app.route("/findUserOrderAcceptByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_accept')
def findUserOrderAcceptBycondition():
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
    tablename = UserOrderAccept.__tablename__
    intColumnClinetNameList = [u'id', u'specificFund', u'isSystem', u'isPaper', u'acceptStatus', u'auditStatus',
                               u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"

            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "specificFund": tableData[4],
                        "isSystem": tableData[5],
                        "isPaper": tableData[6],
                        "declareName": tableData[7],
                        "preProjectTime": tableData[8],
                        "acceptStatus": tableData[9],
                        "acceptRemark": tableData[10],
                        "auditPerson": tableData[11],
                        "auditTime": tableData[12],
                        "auditStatus": tableData[13],
                        "auditRemark": tableData[14],
                        "counselorId": tableData[15],
                        "manageCounselorId": tableData[16],
                        "imageUrl": tableData[17],
                        "requireList": tableData[18],
                        "acceptTime": tableData[19],
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
@app.route("/findFBUserOrderAcceptByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_accept')
def findFBUserOrderAcceptByCondition():
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
    tablename = UserOrderAccept.__tablename__
    intColumnClinetNameList = [u'id', u'specificFund', u'isSystem', u'isPaper', u'acceptStatus', u'auditStatus',
                               u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"

            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "specificFund": tableData[4],
                        "isSystem": tableData[5],
                        "isPaper": tableData[6],
                        "declareName": tableData[7],
                        "preProjectTime": tableData[8],
                        "acceptStatus": tableData[9],
                        "acceptRemark": tableData[10],
                        "auditPerson": tableData[11],
                        "auditTime": tableData[12],
                        "auditStatus": tableData[13],
                        "auditRemark": tableData[14],
                        "counselorId": tableData[15],
                        "manageCounselorId": tableData[16],
                        "imageUrl": tableData[17],
                        "requireList": tableData[18],
                        "acceptTime": tableData[19],
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
@app.route("/getUserOrderAcceptDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_accept')
def getUserOrderAcceptDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserOrderAccept, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "orderNo": table.order_no,
                "serviceNo": table.service_no,
                "itemTitle": table.item_title,
                "specificFund": table.specific_fund,
                "isSystem": table.is_system,
                "isPaper": table.is_paper,
                "declareName": table.declare_name,
                "preProjectTime": table.pre_project_time,
                "acceptStatus": table.accept_status,
                "acceptRemark": table.accept_remark,
                "auditPerson": table.audit_person,
                "auditTime": table.audit_time,
                "auditStatus": table.audit_status,
                "auditRemark": table.audit_remark,
                "counselorId": table.counselor_id,
                "manageCounselorId": table.manage_counselor_id,
                "imageUrl": table.image_url,
                "requireList": table.require_list,
                "acceptTime": table.accept_time, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserOrderAccept", methods=["POST"])
@jwt_required
@deleteLog('zzh_user_order_accept')
def deleteUserOrderAccept():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserOrderAccept, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserOrderAccept", methods=["POST"])
@jwt_required
@addLog('zzh_user_order_accept')
def addUserOrderAccept():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("orderNo", None), dataDict.get("serviceNo", None), dataDict.get("itemTitle", None),
                 dataDict.get("specificFund", None), dataDict.get("isSystem", None), dataDict.get("isPaper", None),
                 dataDict.get("declareName", None), dataDict.get("preProjectTime", None),
                 dataDict.get("acceptStatus", None), dataDict.get("acceptRemark", None),
                 dataDict.get("auditPerson", None), dataDict.get("auditTime", None), dataDict.get("auditStatus", None),
                 dataDict.get("auditRemark", None), dataDict.get("counselorId", None),
                 dataDict.get("manageCounselorId", None), dataDict.get("imageUrl", None),
                 dataDict.get("requireList", None), dataDict.get("acceptTime", None))
    table = insertToSQL(UserOrderAccept, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataUserOrderAccept", methods=["POST"])
@jwt_required
@updateLog('zzh_user_order_accept')
def updataUserOrderAccept():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "service_no"
    intColumnClinetNameList = (
        "id", "isSystem", "isPaper", "acceptStatus", "auditStatus", "counselorId", "manageCounselorId")
    serviceNo = dataDict.get("serviceNo", None)
    acceptStatus = dataDict.get("acceptStatus", None)
    isSystem = dataDict.get("isSystem", 0)
    isPaper = dataDict.get("isPaper", 0)
    preProjectTime = dataDict.get("preProjectTime", None)
    acceptRemark = dataDict.get("acceptRemark", None)

    if acceptStatus == 2:
        if not (serviceNo and acceptStatus):
            resultDict = returnErrorMsg("not find serviceNo or acceptStatus!")
            return jsonify(resultDict)
    else:
        if not (serviceNo and acceptStatus and isinstance(isSystem, int) and isinstance(isPaper, int)):
            resultDict = returnErrorMsg("not find serviceNo or acceptStatus!")
            return jsonify(resultDict)

    table = findById(UserOrderAccept, columnId, serviceNo, isStrcheck=True)
    if not table:
        resultDict = returnErrorMsg("not find this service_no")
        return jsonify(resultDict)
    if table.audit_status == 1:
        resultDict = returnMsg("checking")
        return jsonify(resultDict)

    dataDict["auditStatus"] = 1
    menuUp = updataById(UserOrderAccept, dataDict, columnId, serviceNo, tableChangeDic,
                        intColumnClinetNameList, isIsInt=False)
    if menuUp == None:
        resultDict = returnErrorMsg()
    elif menuUp == 0:
        resultDict = returnErrorMsg("the amountId not exit!")
    else:
        # infoDict = acceptTableDictSort(menuUp)
        resultDict = returnMsg({})
    return jsonify(resultDict)


# 审核
@app.route("/checkIsUserOrderAccept", methods=["POST"])
@jwt_required
def checkIsUserOrderAccept():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = UserOrderAccept.id
    intColumnClinetNameList = ("id", "isSystem", "isPaper", "acceptStatus", "counselorId", "manageCounselorId")
    infoList = []
    idList = dataDict.get("ids", None)
    auditStatus = dataDict.get("auditStatus", None)
    if not (idList and auditStatus):
        resultDict = returnErrorMsg("not find ids or auditStatus!")
        return jsonify(resultDict)

    datatimeNow = getTimeStrfTimeStampNow()
    dataDict["auditPerson"] = current_user.admin_name
    dataDict["auditTime"] = datatimeNow

    dbOperation = OperationOfDB()
    for id in idList:
        menuUp = findById(UserOrderAccept, "id", id)
        if menuUp == 0:
            resultDict = returnErrorMsg("not find this id")
            return jsonify(resultDict)
        elif menuUp == None:
            resultDict = returnErrorMsg
            return jsonify(resultDict)
        # menuUp = dbOperation.updateThis(UserOrderAccept, columnId, id, dataDict, tableChangeDic)
        # if not menuUp:
        #     dbOperation.commitRollback()
        #     resultDict = returnErrorMsg("not find table")
        #     return jsonify(resultDict)
        sendAuditStatus = menuUp.accept_status

        if sendAuditStatus == Res.StatusCode["pass"]:
            if auditStatus == Res.AuditCode["pass"]:
                # 添加立项表
                columnsStr = (
                    menuUp.order_no, menuUp.service_no, menuUp.item_title, menuUp.specific_fund, 0, None, 0,
                    None, None, None, None, 0, None, menuUp.counselor_id, menuUp.manage_counselor_id, None, None, None)
                auditTable = dbOperation.insertToSQL(UserOrderProject, *columnsStr)
                if not auditTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find table")
                    return jsonify(resultDict)
                # 添加受理费

                counselorTable = CounselorAccountCertification.query.filter(
                    CounselorAccountCertification.counselor_id == menuUp.counselor_id).first()
                if not counselorTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find this counselor")
                    return jsonify(resultDict)
                ContractTable = UserOrderContract.query.filter(
                    UserOrderContract.service_no == menuUp.service_no).first()
                payment_method = counselorTable.counselor_receipt_method
                payment_money = ContractTable.counselor_accept_fee
                amountColumnsStr = (menuUp.order_no, 2, payment_method, counselorTable.counselor_payee,
                                    counselorTable.counselor_receipt_bank, counselorTable.counselor_receipt_account,
                                    None, payment_money, None, None, 0, None, 1, None, None, None, menuUp.service_no)
                amountTable = dbOperation.insertToSQL(CounselorOrderAmountCheck, *amountColumnsStr)
                if not amountTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find table")
                    return jsonify(resultDict)
                declareTable = addDeclareStatus(menuUp.order_no, dbOperation, "0000011111")
                if not declareTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not update fail")
                    return jsonify(resultDict)
            elif auditStatus == Res.AuditCode["fail"]:
                dataDict["acceptStatus"] = 0
            else:
                dbOperation.commitRollback()
                resultDict = returnMsg("")
                return jsonify(resultDict)
        elif sendAuditStatus == Res.StatusCode["fail"]:
            if auditStatus == Res.AuditCode["pass"]:
                # 添加取消表
                cancelIp = request.remote_addr
                cancel_time = getTimeStrfTimeStampNow()
                columnsStr = (
                    menuUp.order_no, 1, dataDict.get("auditRemark", None), cancel_time, cancelIp, 0, None, None, None)
                UserOrderCancelTable = dbOperation.insertToSQL(UserOrderCancel, *columnsStr)
                if not UserOrderCancelTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find table")
                    return jsonify(resultDict)
                # 更新派单记录
                newDataDict = {"assignStatus": 3}
                columnId = UserOrderAssign.service_no
                serviceNo = menuUp.service_no
                # intColumnClinetNameList = ("id", "counselorId", "manageCounselorId", "assignStatus")
                UserOrderAssignTable = dbOperation.updateThis(UserOrderAssign, columnId, serviceNo, newDataDict,
                                                              UserOrderAssignChangeDic, isInt=False)
                if not UserOrderAssignTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find table")
                    return jsonify(resultDict)
                declareTable = addDeclareStatus(menuUp.order_no, dbOperation, "0000021111")
                if not declareTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not update fail")
                    return jsonify(resultDict)
            elif auditStatus == Res.AuditCode["fail"]:
                dataDict["acceptStatus"] = 0
            else:
                dbOperation.commitRollback()
                resultDict = returnMsg("")
                return jsonify(resultDict)
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("not find contract_status")
            return jsonify(resultDict)
        # 添加审核阶段表
        datatimeNow = getTimeStrfTimeStampNow()
        shColumnsStr = (menuUp.order_no, '项目受理阶段', current_user.admin_name, dataDict.get("stageTime", datatimeNow),
                        dataDict.get("stageRemark"))
        shTable = dbOperation.insertToSQL(DeclareProgress, *shColumnsStr)
        if not shTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("not find table")
            return jsonify(resultDict)
        menuUp = dbOperation.updateThis(UserOrderAccept, columnId, id, dataDict, tableChangeDic)
        if not menuUp:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("not find table")
            return jsonify(resultDict)
    isOk = dbOperation.commitToSQL()
    if isOk:
        # infoDict = tableDictSort(menuUp)
        # infoList.append(infoDict)
        resultDict = returnMsg(infoList)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("not find table")
        return jsonify(resultDict)
    return jsonify(resultDict)
