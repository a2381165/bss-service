# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Order.UserOrderContract import UserOrderContract, UserOrderContractChangeDic as tableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取 列表
@app.route("/findUserOrderContractByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_contract')
def findUserOrderContractBycondition():
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
    for index, newDict in enumerate(newList):
        condition.append(newDict)
    # tablename = UserOrderContract.__tablename__
    tablename = "view_contract_order_item"
    intColumnClinetNameList = [u'id', u'contractStatus', u'auditStatus', u'counselorId', u'manageCounselorId',
                               u'contractType', u'projectRate', u'counselorProjectRate', u'isGenerate',
                               u'itemType', u'deptId', u'itemId']
    tableList, count = conditionDataListFind(dataDict, view_contract_order_item, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {
                "id": tableData[0],
                "orderNo": tableData[1],
                "serviceNo": tableData[2],
                "itemTitle": tableData[3],
                "contractNo": tableData[4],
                "contractStatus": tableData[5],
                "contractAnnex": tableData[6],
                "contractRemark": tableData[7],
                "auditPerson": tableData[8],
                "auditTime": tableData[9],
                "auditStatus": tableData[10],
                "auditRemark": tableData[11],
                "counselorId": tableData[12],
                "manageCounselorId": tableData[13],
                "contractType": tableData[14],
                "contractPrice": str(tableData[15]),
                "startFee": str(tableData[16]),
                "projectFee": str(tableData[17]),
                "projectRate": str(tableData[18]),
                "counselorStartFee": str(tableData[19]),
                "counselorAcceptFee": str(tableData[20]),
                "counselorProjectFee": str(tableData[21]),
                "counselorProjectRate": str(tableData[22]),
                "isGenerate": tableData[23],
                "itemUrl": tableData[24],
                "itemImgurl": tableData[25],
                "itemPricerange": tableData[26],
                "itemPulishdate": tableData[27],
                "itemDeadline": tableData[28],
                "itemContact": tableData[29],
                "itemSubmitAddress": tableData[30],
                "itemType": tableData[31],
                "itemContent": tableData[32],
                "deptId": tableData[33],
                "itemId": tableData[34], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取 列表
@app.route("/findFBUserOrderContractByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_contract')
def findFBUserOrderContractByCondition():
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
    tablename = UserOrderContract.__tablename__
    intColumnClinetNameList = [u'id', u'contractStatus', u'auditStatus', u'counselorId', u'manageCounselorId',
                               u'contractType', u'projectRate', u'counselorProjectRate', u'isGenerate']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "contractNo": tableData[4],
                        "contractStatus": tableData[5],
                        "contractAnnex": tableData[6],
                        "contractRemark": tableData[7],
                        "auditPerson": tableData[8],
                        "auditTime": tableData[9],
                        "auditStatus": tableData[10],
                        "auditRemark": tableData[11],
                        "counselorId": tableData[12],
                        "manageCounselorId": tableData[13],
                        "contractType": tableData[14],
                        "contractPrice": tableData[15],
                        "startFee": tableData[16],
                        "projectFee": tableData[17],
                        "projectRate": tableData[18],
                        "counselorStartFee": tableData[19],
                        "counselorAcceptFee": tableData[20],
                        "counselorProjectFee": tableData[21],
                        "counselorProjectRate": tableData[22],
                        "isGenerate": tableData[23], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情
@app.route("/getUserOrderContractDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_contract')
def getUserOrderContractDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserOrderContract, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "orderNo": table.order_no,
                "serviceNo": table.service_no,
                "itemTitle": table.item_title,
                "contractNo": table.contract_no,
                "contractStatus": table.contract_status,
                "contractAnnex": table.contract_annex,
                "contractRemark": table.contract_remark,
                "auditPerson": table.audit_person,
                "auditTime": table.audit_time,
                "auditStatus": table.audit_status,
                "auditRemark": table.audit_remark,
                "counselorId": table.counselor_id,
                "manageCounselorId": table.manage_counselor_id,
                "contractType": table.contract_type,
                "contractPrice": table.contract_price,
                "startFee": table.start_fee,
                "projectFee": table.project_fee,
                "projectRate": table.project_rate,
                "counselorStartFee": table.counselor_start_fee,
                "counselorAcceptFee": table.counselor_accept_fee,
                "counselorProjectFee": table.counselor_project_fee,
                "counselorProjectRate": table.counselor_project_rate,
                "isGenerate": table.is_generate, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserOrderContract", methods=["POST"])
@jwt_required
@deleteLog('zzh_user_order_contract')
def deleteUserOrderContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserOrderContract, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserOrderContract", methods=["POST"])
@jwt_required
@addLog('zzh_user_order_contract')
def addUserOrderContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("orderNo", None), dataDict.get("serviceNo", None), dataDict.get("itemTitle", None),
                 dataDict.get("contractNo", None), dataDict.get("contractStatus", None),
                 dataDict.get("contractAnnex", None), dataDict.get("contractRemark", None),
                 dataDict.get("auditPerson", None), dataDict.get("auditTime", None), dataDict.get("auditStatus", None),
                 dataDict.get("auditRemark", None), dataDict.get("counselorId", None),
                 dataDict.get("manageCounselorId", None), dataDict.get("contractType", None),
                 dataDict.get("contractPrice", None), dataDict.get("startFee", None), dataDict.get("projectFee", None),
                 dataDict.get("projectRate", None), dataDict.get("counselorStartFee", None),
                 dataDict.get("counselorAcceptFee", None), dataDict.get("counselorProjectFee", None),
                 dataDict.get("counselorProjectRate", None), dataDict.get("isGenerate", None))
    table = insertToSQL(UserOrderContract, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataUserOrderContract", methods=["POST"])
@jwt_required
@updateLog('zzh_user_order_contract')
def updataUserOrderContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'contractStatus', u'auditStatus', u'counselorId', u'manageCounselorId',
                               u'contractType', u'projectRate', u'counselorProjectRate', u'isGenerate']
    table = updataById(UserOrderContract, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 更新合同签订记录表
@app.route("/updateUserOrderContract", methods=["POST"])
@jwt_required
def updateUserOrderContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg("not find ids!")
        return jsonify(resultDict)
    auditStatus = dataDict.get("auditStatus", 0)
    if auditStatus != 0:
        dataDict.pop("auditStatus")

    resultDict = update(idList, dataDict, infoList)
    return jsonify(resultDict)


# 送审 保存并送审
@app.route("/checkUserOrderContract", methods=["POST"])
@jwt_required
def checkUserOrderContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    idList = dataDict.get("ids", [])
    # auditStatus = dataDict.get("auditStatus", None)
    if not (idList):
        resultDict = returnErrorMsg("not find ids !")
        return jsonify(resultDict)
    dataDict.pop("ids")
    dataDict["auditStatus"] = 1
    resultDict = update(idList, dataDict, infoList)
    return jsonify(resultDict)


def update(idList, dataDict, infoList):
    if not idList:
        resultDict = returnErrorMsg("not find ids!")
        return resultDict
    columnId = "id"
    intColumnClinetNameList = (
        "id", "contractStatus", "auditStatus", "counselorId", "manageCounselorId", "contractType", "isGenerate",
        "counselorProjectRate", "projectRate")
    for id in idList:
        menuUp = updataById(UserOrderContract, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if menuUp == None:
            resultDict = returnErrorMsg()
            return resultDict
        elif menuUp == 0:
            resultDict = returnErrorMsg("the id not exit!")
            return resultDict
        else:
            # infoDict = tableDictSort(menuUp)
            infoList.append({})
    resultDict = returnMsg(infoList)
    return resultDict


view_contract_order_item = {
    "id": "id",
    "orderNo": "order_no",
    "serviceNo": "service_no",
    "itemTitle": "item_title",
    "contractNo": "contract_no",
    "contractStatus": "contract_status",
    "contractAnnex": "contract_annex",
    "contractRemark": "contract_remark",
    "auditPerson": "audit_person",
    "auditTime": "audit_time",
    "auditStatus": "audit_status",
    "auditRemark": "audit_remark",
    "counselorId": "counselor_id",
    "manageCounselorId": "manage_counselor_id",
    "contractType": "contract_type",
    "contractPrice": "contract_price",
    "startFee": "start_fee",
    "projectFee": "project_fee",
    "projectRate": "project_rate",
    "counselorStartFee": "counselor_start_fee",
    "counselorAcceptFee": "counselor_accept_fee",
    "counselorProjectFee": "counselor_project_fee",
    "counselorProjectRate": "counselor_project_rate",
    "isGenerate": "is_generate",
    "itemUrl": "item_url",
    "itemImgurl": "item_imgurl",
    "itemPricerange": "item_pricerange",
    "itemPulishdate": "item_pulishdate",
    "itemDeadline": "item_deadline",
    "itemContact": "item_contact",
    "itemSubmitAddress": "item_submit_address",
    "itemType": "item_type",
    "itemContent": "item_content",
    "deptId": "dept_id",
    "itemId": "item_id",
}
