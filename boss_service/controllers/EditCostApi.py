# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Boss.EditCost import EditCost, EditCostChangeDic as tableChangeDic, intList
from models.Boss.ServiceFee import ServiceFee, ServiceFeeChangeDic
from models.Boss.MonthlyWages import MonthlyWages
from common.Log import queryLog, addLog, deleteLog, updateLog


# 商务副部长
@app.route("/findBsEditCostByCondition", methods=["POST"])
@jwt_required
def findBsEditCostByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    isSettled = dataDict.get("isSettled", None)
    if dataDict.get('condition', None) == None and not isSettled:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    if isSettled == 1:
        newList = [{
            "field": "isDone",
            "op": "equal",
            "value": 0
        }]
        for newDict in newList:
            condition.append(newDict)
        deptIdConditonStr = " and  ( development_fee_status in (0,1) or sign_fee_status in (0,1) or bs_commission_fee_status in (0,1) )"
    elif isSettled == 2:
        newList = [{
            "field": "isDone",
            "op": "in",
            "value": "(0,1)"
        }]
        for newDict in newList:
            condition.append(newDict)
        deptIdConditonStr = " and  ( development_fee_status  in (2,3,4,5) or sign_fee_status not in (2,3,4,5) or bs_commission_fee_status not in (2,3,4,5) )"
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = "view_edit_cost_member_contract_service_fee_admin_name"
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_edit_cost_member_contract_change, intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr, deptIdConditonStr=deptIdConditonStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = bs_view_edit_cost_member_contract_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 咨询副部长
@app.route("/findCoEditCostByCondition", methods=["POST"])
@jwt_required
def findCoEditCostByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    isSettled = dataDict.get("isSettled", None)
    if dataDict.get('condition', None) == None and not isSettled:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    if isSettled == 1:
        newList = [{
            "field": "isDone",
            "op": "equal",
            "value": 0
        }]
        for newDict in newList:
            condition.append(newDict)
        deptIdConditonStr = " and  ( edit_fee_status in (0,1) or accept_fee_status in (0,1) or co_commission_fee_status in (0,1) )"
    elif isSettled == 2:
        newList = [{
            "field": "isDone",
            "op": "in",
            "value": "(0,1)"
        }]
        for newDict in newList:
            condition.append(newDict)
        deptIdConditonStr = " and  ( edit_fee_status not in (0,1) or accept_fee_status not in (0,1) or co_commission_fee_status not in (0,1) )"
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = "view_edit_cost_member_contract_service_fee_admin_name"
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_edit_cost_member_contract_change, intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr, deptIdConditonStr=deptIdConditonStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = co_view_edit_cost_member_contract_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

# 获取 列表
@app.route("/findEditCostByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_edit_cost')
def findEditCostByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    isSettled = dataDict.get("isSettled", None)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")

    if isSettled == 1:
        newList = [{
            "field": "isDone",
            "op": "equal",
            "value": 0
        }]
        for newDict in newList:
            condition.append(newDict)
        deptIdConditonStr = " and    ( edit_fee_status in (2,3) or accept_fee_status in (2,3) or co_commission_fee_status in (2,3) or development_fee_status in (2,3) or sign_fee_status in (2,3) or bs_commission_fee_status in (2,3) )"
    elif isSettled == 2:
        newList = [{
            "field": "isDone",
            "op": "in",
            "value": "(0,1)"
        }]
        for newDict in newList:
            condition.append(newDict)
        deptIdConditonStr = " and  ( edit_fee_status in (4,5) or accept_fee_status in (4,5) or co_commission_fee_status in (4,5) or development_fee_status in (4,5) or sign_fee_status in (4,5) or bs_commission_fee_status in (4,5) )"
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = "view_edit_cost_member_contract_service_fee_admin_name"
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_edit_cost_member_contract_change, intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr,deptIdConditonStr=deptIdConditonStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = view_edit_cost_member_contract_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 更新
@app.route("/updataEditCost", methods=["POST"])
@jwt_required
@updateLog('boss_edit_cost')
def updataEditCost():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(EditCost, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 咨询副部长 上报
@app.route("/sendUpCoEditCost", methods=["POST"])
@jwt_required
def sendUpCoEditCost():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(EditCost, "id", id)
    editCheckId = table.edit_check_id
    acceptCheckId = table.accept_check_id
    projectCheckId = table.project_check_id
    # developmentCheckId = table.development_check_id
    # signCheckId = table.sign_check_id
    # commissionCheckId = table.commission_check_id
    dbOperatiopn = OperationOfDB()
    editInfo = findById(ServiceFee, "id", editCheckId)
    acceptInfo = findById(ServiceFee, "id", acceptCheckId)
    projectInfo = findById(ServiceFee, "id", projectCheckId)
    if editInfo.service_fee > 0 and editInfo.fee_status in (0,1):
        editInfo.fee_status = 2
        editInfo = dbOperatiopn.addTokenToSql(editInfo)
        if not editInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if acceptInfo.service_fee > 0 and acceptInfo.fee_status in (0,1):
        acceptInfo.fee_status = 2
        acceptInfo = dbOperatiopn.addTokenToSql(acceptInfo)
        if not acceptInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if projectInfo.service_rate > 0 and projectInfo.fee_status in (0,1):
        projectInfo.fee_status = 2
        projectInfo = dbOperatiopn.addTokenToSql(projectInfo)
        if not projectInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperatiopn.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperatiopn.commitRollback()
        resultDict = returnMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 商务副部长 上报
@app.route("/sendUpBsEditCost", methods=["POST"])
@jwt_required
def sendUpBsEditCost():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(EditCost, "id", id)
    # editCheckId = table.edit_check_id
    # acceptCheckId = table.accept_check_id
    # projectCheckId = table.project_check_id
    developmentCheckId = table.development_check_id
    signCheckId = table.sign_check_id
    commissionCheckId = table.commission_check_id
    dbOperatiopn = OperationOfDB()
    developmentInfo = findById(ServiceFee, "id", developmentCheckId)
    signInfo = findById(ServiceFee, "id", signCheckId)
    commissionInfo = findById(ServiceFee, "id", commissionCheckId)
    if developmentInfo.service_fee > 0 and developmentInfo.fee_status in (0,1):
        developmentInfo.fee_status = 2
        editInfo = dbOperatiopn.addTokenToSql(developmentInfo)
        if not editInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if signInfo.service_fee > 0 and signInfo.fee_status in (0,1):
        signInfo.fee_status = 2
        acceptInfo = dbOperatiopn.addTokenToSql(signInfo)
        if not acceptInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if commissionInfo.service_rate > 0 and commissionInfo.fee_status in (0,1):
        commissionInfo.fee_status = 2
        projectInfo = dbOperatiopn.addTokenToSql(commissionInfo)
        if not projectInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperatiopn.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperatiopn.commitRollback()
        resultDict = returnMsg(errorCode["commit_fail"])
    return jsonify(resultDict)

# 部长上报
@app.route("/sendUpEditCost",methods=["POST"])
@jwt_required
def sendUpEditCost():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(EditCost, "id", id)
    editCheckId = table.edit_check_id
    acceptCheckId = table.accept_check_id
    projectCheckId = table.project_check_id
    developmentCheckId = table.development_check_id
    signCheckId = table.sign_check_id
    commissionCheckId = table.commission_check_id
    dbOperatiopn = OperationOfDB()
    editInfo = findById(ServiceFee, "id", editCheckId)
    acceptInfo = findById(ServiceFee, "id", acceptCheckId)
    projectInfo = findById(ServiceFee, "id", projectCheckId)
    developmentInfo = findById(ServiceFee, "id", developmentCheckId)
    signInfo = findById(ServiceFee, "id", signCheckId)
    commissionInfo = findById(ServiceFee, "id", commissionCheckId)
    editFee = 0
    accpetFee = 0
    prejectRate = 0
    if editInfo.service_fee > 0 and editInfo.fee_status in (2,3):
        editInfo.fee_status = 4
        editFee = editInfo.service_fee
        editInfo = dbOperatiopn.addTokenToSql(editInfo)
        if not editInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if acceptInfo.service_fee > 0 and acceptInfo.fee_status in (2,3):
        acceptInfo.fee_status = 4
        accpetFee= editInfo.service_fee
        acceptInfo = dbOperatiopn.addTokenToSql(acceptInfo)
        if not acceptInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if projectInfo.service_rate > 0 and projectInfo.fee_status in (2,3):
        projectInfo.fee_status = 4
        prejectRate = projectInfo.service_rate
        projectInfo = dbOperatiopn.addTokenToSql(projectInfo)
        if not projectInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if developmentInfo.service_fee > 0 and developmentInfo.fee_status in (2,3):
        developmentInfo.fee_status = 4
        developmentFee= developmentInfo.service_fee
        editInfo = dbOperatiopn.addTokenToSql(developmentInfo)
        if not editInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if signInfo.service_fee > 0 and signInfo.fee_status in (2,3):
        signInfo.fee_status = 4
        signFee= signInfo.service_fee
        acceptInfo = dbOperatiopn.addTokenToSql(signInfo)
        if not acceptInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if commissionInfo.service_rate > 0 and commissionInfo.fee_status in (2,3):
        commissionInfo.fee_status = 4
        commissionRate = commissionInfo.service_fee
        projectInfo = dbOperatiopn.addTokenToSql(commissionInfo)
        if not projectInfo:
            dbOperatiopn.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    now = getTimeStrfTimeStampNow()
    year = now.year
    month = now.month
    co_admin_id = 1
    bs_admin_id = 1
    admin_id = 1
    # 咨询副部长
    co_monthlyWagesTable = MonthlyWages.query.filer_by(month=month,year=year,admin_id=co_admin_id).first()
    bs_monthlyWagesTable = MonthlyWages.query.filer_by(month=month,year=year,admin_id=bs_admin_id).first()
    monthlyWagesTable = MonthlyWages.query.filer_by(month=month,year=year,admin_id=admin_id).first()
    if co_monthlyWagesTable:
        monthlyWagesTable.start_fee += editFee + accpetFee
        monthlyWagesTable.manage_fee = (monthlyWagesTable.start_fee + editFee + accpetFee) * monthlyWagesTable.rate
    if bs_monthlyWagesTable:
        monthlyWagesTable.start_fee += editFee + accpetFee
        monthlyWagesTable.manage_fee = (monthlyWagesTable.start_fee + editFee + accpetFee) * monthlyWagesTable.rate

        # monthlyWagesTable.project_fee += prejectRate

    if dbOperatiopn.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperatiopn.commitRollback()
        resultDict = returnMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


def tableSort(table):
    _infoDict = {"id": table.id,
                 "internalOrderNo": table.internal_order_no,
                 "contractNo": table.contract_no,
                 "orderNo": table.order_no,
                 "internalOrderType": table.internal_order_type,
                 "editCheckId": table.edit_check_id,
                 "acceptCheckId": table.accept_check_id,
                 "projectCheckId": table.project_check_id,
                 "developmentCheckId": table.development_check_id,
                 "signCheckId": table.sign_check_id,
                 "commissionCheckId": table.commission_check_id,
                 "createPerson": table.create_person,
                 "createTime": table.create_time,
                 "isDone": table.is_done, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "internalOrderNo": tableData[1],
                 "contractNo": tableData[2],
                 "orderNo": tableData[3],
                 "internalOrderType": tableData[4],
                 "editCheckId": tableData[5],
                 "acceptCheckId": tableData[6],
                 "projectCheckId": tableData[7],
                 "developmentCheckId": tableData[8],
                 "signCheckId": tableData[9],
                 "commissionCheckId": tableData[10],
                 "createPerson": tableData[11],
                 "createTime": tableData[12],
                 "isDone": tableData[13], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def co_view_edit_cost_member_contract_fun(tableData):
    _infoDict = {"id": tableData[0],
                 "internalOrderNo": tableData[1],
                 "contractNo": tableData[2],
                 "orderNo": tableData[3],
                 "internalOrderType": tableData[4],
                 "editCheckId": tableData[5],
                 "acceptCheckId": tableData[6],
                 "projectCheckId": tableData[7],
                 # "developmentCheckId": tableData[8],
                 # "signCheckId": tableData[9],
                 # "commissionCheckId": tableData[10],
                 "createPerson": tableData[11],
                 "createTime": tableData[12],
                 "isDone": tableData[13],
                 "serviceNo": tableData[14],
                 "itemTitle": tableData[15],
                 "contractAnnex": tableData[16],
                 "contractRemark": tableData[17],
                 "contractType": tableData[18],
                 "contractPrice": tableData[19],
                 "startFee": tableData[20],
                 "projectFee": tableData[21],
                 "projectRate": tableData[22],
                 "isGenerate": tableData[23],
                 "startTime": tableData[24],
                 "endTime": tableData[25],
                 "signingPerson": tableData[26],
                 "orderType": tableData[27],
                 "serviceId": tableData[28],
                 "contactPerson": tableData[29],
                 "contactPhone": tableData[30],
                 "contactEmail": tableData[31],
                 "userId": tableData[32],
                 "memberName": tableData[33],
                 "memberContactEmail": tableData[34],
                 "memberContactPerson": tableData[35],
                 "memberContactPhone": tableData[36],
                 "editAdminId": tableData[37],
                 "editFee": tableData[38],
                 "editFeeStatus": tableData[39],
                 "accpetAdminId": tableData[40],
                 "acceptFee": tableData[41],
                 "acceptFeeStatus": tableData[42],
                 "coCommissionAdminId": tableData[43],
                 "coCommissionFee": tableData[44],
                 "coCommissionRate": tableData[45],
                 "coCommissionFeeStatus": tableData[46],
                 "editName": tableData[57],
                 "acppetName": tableData[58],
                 "coCommissionName": tableData[59],
                 }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def bs_view_edit_cost_member_contract_fun(tableData):
    _infoDict = {"id": tableData[0],
                 "internalOrderNo": tableData[1],
                 "contractNo": tableData[2],
                 "orderNo": tableData[3],
                 "internalOrderType": tableData[4],
                 # "editCheckId": tableData[5],
                 # "acceptCheckId": tableData[6],
                 # "projectCheckId": tableData[7],
                 "developmentCheckId": tableData[8],
                 "signCheckId": tableData[9],
                 "commissionCheckId": tableData[10],
                 "createPerson": tableData[11],
                 "createTime": tableData[12],
                 "isDone": tableData[13],
                 "serviceNo": tableData[14],
                 "itemTitle": tableData[15],
                 "contractAnnex": tableData[16],
                 "contractRemark": tableData[17],
                 "contractType": tableData[18],
                 "contractPrice": tableData[19],
                 "startFee": tableData[20],
                 "projectFee": tableData[21],
                 "projectRate": tableData[22],
                 "isGenerate": tableData[23],
                 "startTime": tableData[24],
                 "endTime": tableData[25],
                 "signingPerson": tableData[26],
                 "orderType": tableData[27],
                 "serviceId": tableData[28],
                 "contactPerson": tableData[29],
                 "contactPhone": tableData[30],
                 "contactEmail": tableData[31],
                 "userId": tableData[32],
                 "memberName": tableData[33],
                 "memberContactEmail": tableData[34],
                 "memberContactPerson": tableData[35],
                 "memberContactPhone": tableData[36],
                 "developmentAdminId": tableData[47],
                 "developmentFee": tableData[48],
                 "developmentFeeStatus": tableData[49],
                 "signAdminId": tableData[50],
                 "signFee": tableData[51],
                 "signFeeStatus": tableData[52],
                 "bsCommissionAdminId": tableData[53],
                 "bsCommissionFee": tableData[54],
                 "bsCommissionRate": tableData[55],
                 "bsCommissionFeeStatus": tableData[56],
                 "developmentName": tableData[60],
                 "signName": tableData[61],
                 "bsCommissionName": tableData[62], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def view_edit_cost_member_contract_fun(tableData):
    _infoDict = {"id": tableData[0],
                 "internalOrderNo": tableData[1],
                 "contractNo": tableData[2],
                 "orderNo": tableData[3],
                 "internalOrderType": tableData[4],
                 "editCheckId": tableData[5],
                 "acceptCheckId": tableData[6],
                 "projectCheckId": tableData[7],
                 "developmentCheckId": tableData[8],
                 "signCheckId": tableData[9],
                 "commissionCheckId": tableData[10],
                 "createPerson": tableData[11],
                 "createTime": tableData[12],
                 "isDone": tableData[13],
                 "serviceNo": tableData[14],
                 "itemTitle": tableData[15],
                 "contractAnnex": tableData[16],
                 "contractRemark": tableData[17],
                 "contractType": tableData[18],
                 "contractPrice": tableData[19],
                 "startFee": tableData[20],
                 "projectFee": tableData[21],
                 "projectRate": tableData[22],
                 "isGenerate": tableData[23],
                 "startTime": tableData[24],
                 "endTime": tableData[25],
                 "signingPerson": tableData[26],
                 "orderType": tableData[27],
                 "serviceId": tableData[28],
                 "contactPerson": tableData[29],
                 "contactPhone": tableData[30],
                 "contactEmail": tableData[31],
                 "userId": tableData[32],
                 "memberName": tableData[33],
                 "memberContactEmail": tableData[34],
                 "memberContactPerson": tableData[35],
                 "memberContactPhone": tableData[36],
                 "editAdminId": tableData[37],
                 "editFee": tableData[38],
                 "editFeeStatus": tableData[39],
                 "accpetAdminId": tableData[40],
                 "acceptFee": tableData[41],
                 "acceptFeeStatus": tableData[42],
                 "coCommissionAdminId": tableData[43],
                 "coCommissionFee": tableData[44],
                 "coCommissionRate": tableData[45],
                 "coCommissionFeeStatus": tableData[46],
                 "developmentAdminId": tableData[47],
                 "developmentFee": tableData[48],
                 "developmentFeeStatus": tableData[49],
                 "signAdminId": tableData[50],
                 "signFee": tableData[51],
                 "signFeeStatus": tableData[52],
                 "bsCommissionAdminId": tableData[53],
                 "bsCommissionFee": tableData[54],
                 "bsCommissionRate": tableData[55],
                 "bsCommissionFeeStatus": tableData[56],
                 "editName": tableData[57],
                 "acppetName": tableData[58],
                 "coCommissionName": tableData[59],
                 "developmentName": tableData[60],
                 "signName": tableData[61],
                 "bsCommissionName": tableData[62], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_edit_cost_member_contract_change = {
    "id": "id",
    "internalOrderNo": "internal_order_no",
    "contractNo": "contract_no",
    "orderNo": "order_no",
    "internalOrderType": "internal_order_type",
    "editCheckId": "edit_check_id",
    "acceptCheckId": "accept_check_id",
    "projectCheckId": "project_check_id",
    "developmentCheckId": "development_check_id",
    "signCheckId": "sign_check_id",
    "commissionCheckId": "commission_check_id",
    "createPerson": "create_person",
    "createTime": "create_time",
    "isDone": "is_done",
    "serviceNo": "service_no",
    "itemTitle": "item_title",
    "contractAnnex": "contract_annex",
    "contractRemark": "contract_remark",
    "contractType": "contract_type",
    "contractPrice": "contract_price",
    "startFee": "start_fee",
    "projectFee": "project_fee",
    "projectRate": "project_rate",
    "isGenerate": "is_generate",
    "startTime": "start_time",
    "endTime": "end_time",
    "signingPerson": "signing_person",
    "orderType": "order_type",
    "serviceId": "service_id",
    "contactPerson": "contact_person",
    "contactPhone": "contact_phone",
    "contactEmail": "contact_email",
    "userId": "user_id",
    "memberName": "member_name",
    "memberContactEmail": "member_contact_email",
    "memberContactPerson": "member_contact_person",
    "memberContactPhone": "member_contact_phone",
    "editAdminId": "edit_admin_id",
    "editFee": "edit_fee",
    "editFeeStatus": "edit_fee_status",
    "accpetAdminId": "accpet_admin_id",
    "acceptFee": "accept_fee",
    "acceptFeeStatus": "accept_fee_status",
    "coCommissionAdminId": "co_commission_admin_id",
    "coCommissionFee": "co_commission_fee",
    "coCommissionRate": "co_commission_rate",
    "coCommissionFeeStatus": "co_commission_fee_status",
    "developmentAdminId": "development_admin_id",
    "developmentFee": "development_fee",
    "developmentFeeStatus": "development_fee_status",
    "signAdminId": "sign_admin_id",
    "signFee": "sign_fee",
    "signFeeStatus": "sign_fee_status",
    "bsCommissionAdminId": "bs_commission_admin_id",
    "bsCommissionFee": "bs_commission_fee",
    "bsCommissionRate": "bs_commission_rate",
    "bsCommissionFeeStatus": "bs_commission_fee_status",
    "editName": "edit_name",
    "acppetName": "acppet_name",
    "coCommissionName": "co_commission_name",
    "developmentName": "development_name",
    "signName": "sign_name",
    "bsCommissionName": "bs_commission_name",
}
