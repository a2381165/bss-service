# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, current_user

from Res import StatusCode, AuditCode
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.OrderCommon import addDeclareStatus
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Counselor.CounselorAccountCertification import CounselorAccountCertification
from models.Counselor.CounselorOrderAmountCheck import CounselorOrderAmountCheck
from models.Member.MemberContract import MemberContract
from models.Order.DeclareProgress import DeclareProgress
from models.Order.UserOrderContract import UserOrderContract
from models.Order.UserOrderFile import UserOrderFile
from models.Order.UserOrderItem import UserOrderItem
from models.Order.UserOrderProject import UserOrderProject, UserOrderProjectChangeDic as tableChangeDic
from version.v3.bossConfig import app


# 获取 列表
@app.route("/findUserOrderProjectByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_project')
def findUserOrderProjectBycondition():
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
    tablename = UserOrderProject.__tablename__
    intColumnClinetNameList = [u'id', u'projectStatus', u'auditStatus', u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "specificFund": str(tableData[4]),
                        "projectStatus": tableData[5],
                        "projectCode": tableData[6],
                        "projectFund": str(tableData[7]),
                        "projectDate": tableData[8],
                        "projectRemark": tableData[9],
                        "auditPerson": tableData[10],
                        "auditTime": tableData[11],
                        "auditStatus": tableData[12],
                        "auditRemark": tableData[13],
                        "counselorId": tableData[14],
                        "manageCounselorId": tableData[15],
                        "projectStartTime": tableData[16],
                        "projectEndTime": tableData[17],
                        "projectName": tableData[18],
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
@app.route("/findFBUserOrderProjectByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_project')
def findFBUserOrderProjectByCondition():
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
    tablename = UserOrderProject.__tablename__
    intColumnClinetNameList = [u'id', u'projectStatus', u'auditStatus', u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "specificFund": str(tableData[4]),
                        "projectStatus": tableData[5],
                        "projectCode": tableData[6],
                        "projectFund": str(tableData[7]),
                        "projectDate": tableData[8],
                        "projectRemark": tableData[9],
                        "auditPerson": tableData[10],
                        "auditTime": tableData[11],
                        "auditStatus": tableData[12],
                        "auditRemark": tableData[13],
                        "counselorId": tableData[14],
                        "manageCounselorId": tableData[15],
                        "projectStartTime": tableData[16],
                        "projectEndTime": tableData[17],
                        "projectName": tableData[18],
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
@app.route("/getUserOrderProjectDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_project')
def getUserOrderProjectDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserOrderProject, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "orderNo": table.order_no,
                "serviceNo": table.service_no,
                "itemTitle": table.item_title,
                "specificFund": table.specific_fund,
                "projectStatus": table.project_status,
                "projectCode": table.project_code,
                "projectFund": table.project_fund,
                "projectDate": table.project_date,
                "projectRemark": table.project_remark,
                "auditPerson": table.audit_person,
                "auditTime": table.audit_time,
                "auditStatus": table.audit_status,
                "auditRemark": table.audit_remark,
                "counselorId": table.counselor_id,
                "manageCounselorId": table.manage_counselor_id,
                "projectStartTime": table.project_start_time,
                "projectEndTime": table.project_end_time,
                "projectName": table.project_name, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserOrderProject", methods=["POST"])
@jwt_required
@deleteLog('zzh_user_order_project')
def deleteUserOrderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserOrderProject, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserOrderProject", methods=["POST"])
@jwt_required
@addLog('zzh_user_order_project')
def addUserOrderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("orderNo", None), dataDict.get("serviceNo", None), dataDict.get("itemTitle", None),
                 dataDict.get("specificFund", None), dataDict.get("projectStatus", None),
                 dataDict.get("projectCode", None), dataDict.get("projectFund", None),
                 dataDict.get("projectDate", None), dataDict.get("projectRemark", None),
                 dataDict.get("auditPerson", None), dataDict.get("auditTime", None), dataDict.get("auditStatus", None),
                 dataDict.get("auditRemark", None), dataDict.get("counselorId", None),
                 dataDict.get("manageCounselorId", None), dataDict.get("projectStartTime", None),
                 dataDict.get("projectEndTime", None), dataDict.get("projectName", None))
    table = insertToSQL(UserOrderProject, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updateUserOrderProject", methods=["POST"])
@jwt_required
@updateLog('zzh_user_order_project')
def updateUserOrderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    serviceNo = dataDict.get("serviceNo", None)
    projectStatus = dataDict.get("projectStatus", None)
    projectDate = dataDict.get("projectDate", None)
    projectStartTime = dataDict.get("projectStartTime", None)
    projectEndTime = dataDict.get("projectEndTime", None)
    projectName = dataDict.get("projectName", None)
    projectCode = dataDict.get("projectCode", None)
    projectFund = dataDict.get("projectFund", None)

    if projectStatus == 2:
        if not (serviceNo and projectStatus):
            resultDict = returnErrorMsg("not find serviceNo or projectStatus!")
            return jsonify(resultDict)
    else:
        if not (
                serviceNo and projectStatus and projectDate and projectStartTime and projectEndTime and projectName and projectCode and projectFund):
            resultDict = returnErrorMsg(
                "not find serviceNo or projectStatus or projectDate or projectStartTime or projectEndTime or projectName or projectFund!")
            return jsonify(resultDict)

    columnId = "service_no"
    table = findById(UserOrderProject, columnId, serviceNo, isStrcheck=True)
    if not table:
        resultDict = returnErrorMsg("not find this service_no")
        return jsonify(resultDict)
    if table.audit_status == 1:
        resultDict = returnMsg("checking")
        return jsonify(resultDict)

    dataDict["auditStatus"] = 1
    intColumnClinetNameList = ("id", "projectStatus", "auditStatus", "counselorId", "manageCounselorId")
    menuUp = updataById(UserOrderProject, dataDict, columnId, serviceNo, tableChangeDic,
                        intColumnClinetNameList, isIsInt=False)
    if menuUp == None:
        resultDict = returnErrorMsg()
    elif menuUp == 0:
        resultDict = returnErrorMsg("the Id not exit!")
    else:
        # infoDict = projectTableDictSort(menuUp)
        resultDict = returnMsg({})
    return jsonify(resultDict)


# 审核
@app.route("/checkIsUserOrderProject", methods=["POST"])
@jwt_required
def checkIsUserOrderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    idList = dataDict.get("ids", [])
    auditStatus = dataDict.get("auditStatus", None)
    failList = []
    if not (idList and auditStatus):
        resultDict = returnErrorMsg("not find ids and auditStatus!")
        return jsonify(resultDict)
    # adminId = get_jwt_identity()
    # # adminId = 60
    # if not adminUpdateDataLog(adminId, UserOrderProject.__tablename__, dataDict, 0):
    #     resultDict = returnErrorMsg("update log failed")
    #     return jsonify(resultDict)
    adminTable = current_user
    adminName = adminTable.admin_name
    dateTimeNow = getTimeStrfTimeStampNow()
    if auditStatus != None:
        dataDict["auditTime"] = dateTimeNow
        dataDict["auditPerson"] = adminName
    dbOperation = OperationOfDB()
    for id in idList:
        menuUp = findById(UserOrderProject, "id", id)
        if menuUp == 0:
            resultDict = returnErrorMsg("not find this id")
            return jsonify(resultDict)
        elif menuUp == None:
            resultDict = returnErrorMsg
            return jsonify(resultDict)


        # 合同成功审核
        if menuUp.project_status == StatusCode["pass"]:
            # 审核通过 创建下一级表
            if auditStatus == AuditCode["pass"]:
                # #添加受理费
                # amountColumnsStr=(menuUp.order_no,3,None,None,None,None,None,None,None,None,1,None)
                # amountTable = dbOperation.insertToSQL(CounselorOrderAmount,*amountColumnsStr)
                # if not amountTable:
                #     dbOperation.commitRollback()
                #     resultDict = returnErrorMsg("not find table")
                #     return jsonify(resultDict)
                columnsStr = (
                    menuUp.order_no, menuUp.service_no, menuUp.item_title, menuUp.specific_fund,0,None,
                    menuUp.project_status,menuUp.project_code, menuUp.project_fund, menuUp.project_date,
                    None, None, menuUp.counselor_id, menuUp.manage_counselor_id, None, )
                auditTable = dbOperation.insertToSQL(UserOrderFile, *columnsStr)
                if not auditTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("insert UserOrderFile failed")
                    return jsonify(resultDict)
                declareTable = addDeclareStatus(menuUp.order_no, dbOperation, "0000111111")
                if not declareTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not update fail")
                    return jsonify(resultDict)
                # 更新合同表的 合同经费
                ContractTable = UserOrderContract.query.filter(
                    UserOrderContract.service_no == menuUp.service_no).first()
                ContractTable.contract_price = menuUp.project_fund
                contractTable = dbOperation.addTokenToSql(ContractTable)

                # 更新 用户合同表
                memberContractTable = MemberContract.query.filter(
                    MemberContract.order_no == menuUp.order_no).first()
                memberContractTable.contract_price = menuUp.project_fund
                memberontractTable = dbOperation.addTokenToSql(memberContractTable)

                # 第三笔受理费用
                counselorTable = CounselorAccountCertification.query.filter(
                    CounselorAccountCertification.counselor_id == menuUp.counselor_id).first()
                if not counselorTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find this counselor")
                    return jsonify(resultDict)
                orderItemInfo = UserOrderItem.query.filter(UserOrderItem.order_no == menuUp.order_no).first()
                contractType = orderItemInfo.item_type
                payment_method = counselorTable.counselor_receipt_method
                if contractType == 1:
                    payment_money = ContractTable.counselor_project_rate
                    if payment_money == "":
                        payment_money = 0.00
                    else:
                        payment_money = int(payment_money) * int(menuUp.project_fund) * 0.01
                else:
                    payment_money = ContractTable.counselor_project_fee
                if payment_money == "":
                    payment_money = 0.00
                amountColumnsStr = (
                    menuUp.order_no, 3, payment_method, counselorTable.counselor_payee,
                    counselorTable.counselor_receipt_bank,
                    counselorTable.counselor_receipt_account, None, payment_money, None, None, 0, None, 1, None, None,
                    None, menuUp.service_no)
                amountTable = dbOperation.insertToSQL(CounselorOrderAmountCheck, *amountColumnsStr)
                if not (amountTable and contractTable and memberontractTable):
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not find table")
                    return jsonify(resultDict)
            elif auditStatus == AuditCode["fail"]:
                dataDict["projectStatus"] = 0
            else:
                dbOperation.commitRollback()
                resultDict = returnMsg("")
                return jsonify(resultDict)
        # 合同失败审核
        elif menuUp.project_status == StatusCode["fail"]:
            # 审核通过
            if auditStatus == AuditCode["pass"]:
                columnsStr = (
                    menuUp.order_no, menuUp.service_no, menuUp.item_title, menuUp.specific_fund, menuUp.project_status,
                    menuUp.project_code, menuUp.project_fund, menuUp.project_date,
                    None, None, menuUp.counselor_id, menuUp.manage_counselor_id, None, 0, None)
                auditTable = dbOperation.insertToSQL(UserOrderFile, *columnsStr)
                if not auditTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("insert UserOrderFile failed")
                    return jsonify(resultDict)
                # # 关闭订单
                # cancelIp = request.remote_addr
                # cancel_time = getTimeStrfTimeStampNow()
                # columnsStr = (
                #     menuUp.order_no, 1, dataDict.get("auditRemark", None), cancel_time, cancelIp, 0, None, None, None)
                # userOrderContractTable = dbOperation.insertToSQL(UserOrderCancel, *columnsStr)
                # if not userOrderContractTable:
                #     dbOperation.commitRollback()
                #     resultDict = returnErrorMsg("insert UserOrderCancel failed")
                #     return jsonify(resultDict)
                # # 重新派单 或者关闭订单
                # newDataDict = {"assignStatus": 3}
                # columnId = "order_no"
                # intColumnClinetNameList = ("id", "counselorId", "manageCounselorId", "assignStatus")
                #
                # serviceNo = menuUp.service_no
                # # intColumnClinetNameList = ("id", "counselorId", "manageCounselorId", "assignStatus")
                # UserOrderAssignTable = dbOperation.updateThis(UserOrderAssign, UserOrderAssign.service_no, serviceNo,
                #                                               newDataDict, AssignChangeDic, isInt=False)
                #
                # if not UserOrderAssignTable:
                #     dbOperation.commitRollback()
                #     resultDict = returnErrorMsg("updata UserOrderAssign failed")
                #     return jsonify(resultDict)
                declareTable = addDeclareStatus(menuUp.order_no, dbOperation, "0000211111")
                if not declareTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("not update fail")
                    return jsonify(resultDict)
            elif auditStatus == AuditCode["fail"]:
                dataDict["acceptStatus"] = 0
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
        shColumnsStr = (menuUp.order_no, '项目立项阶段', current_user.admin_name, dataDict.get("stageTime", datatimeNow),
                        dataDict.get("stageRemark"))
        shTable = dbOperation.insertToSQL(DeclareProgress, *shColumnsStr)
        if not shTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("insert DeclareProgress failed")
            return jsonify(resultDict)
        menuUp = dbOperation.updateThis(UserOrderProject, UserOrderProject.id, id, dataDict, tableChangeDic)
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
