# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Data.MemberTempContract import MemberTempContract, MemberTempContractChangeDic as tableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取 列表
@app.route("/findMemberTempContractByCondition", methods=["POST"])
@jwt_required
@queryLog('data_member_temp_contract')
def findMemberTempContractByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = MemberTempContract.__tablename__
    orderByStr = " order by create_time desc "
    intColumnClinetNameList = [u'id', u'productName', u'projectRate', u'contractType', u'isDone']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename,orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "contractNo": tableData[3],
                        "contractName": tableData[4],
                        "contractRemark": tableData[5],
                        "productName": tableData[6],
                        "contractPrice": tableData[7],
                        "startFee": tableData[8],
                        "projectFee": tableData[9],
                        "projectRate": tableData[10],
                        "contractType": tableData[11],
                        "startTime": tableData[12],
                        "endTime": tableData[13],
                        "createPerson": tableData[14],
                        "createTime": tableData[15],
                        "executePerson": tableData[16],
                        "executeTime": tableData[17],
                        "isDone": tableData[18], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getMemberTempContractDetail", methods=["POST"])
@jwt_required
@queryLog('data_member_temp_contract')
def getMemberTempContractDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(MemberTempContract, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "orderNo": table.order_no,
                "serviceNo": table.service_no,
                "contractNo": table.contract_no,
                "contractName": table.contract_name,
                "contractRemark": table.contract_remark,
                "productName": table.product_name,
                "contractPrice": table.contract_price,
                "startFee": table.start_fee,
                "projectFee": table.project_fee,
                "projectRate": table.project_rate,
                "contractType": table.contract_type,
                "startTime": table.start_time,
                "endTime": table.end_time,
                "createPerson": table.create_person,
                "createTime": table.create_time,
                "executePerson": table.execute_person,
                "executeTime": table.execute_time,
                "isDone": table.is_done, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteMemberTempContract", methods=["POST"])
@jwt_required
@deleteLog('data_member_temp_contract')
def deleteMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(MemberTempContract, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addMemberTempContract", methods=["POST"])
@jwt_required
@addLog('data_member_temp_contract')
def addMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("orderNo", None), dataDict.get("serviceNo", None), dataDict.get("contractNo", None),
                 dataDict.get("contractName", None), dataDict.get("contractRemark", None),
                 dataDict.get("productName", None), dataDict.get("contractPrice", None), dataDict.get("startFee", None),
                 dataDict.get("projectFee", None), dataDict.get("projectRate", None),
                 dataDict.get("contractType", None), dataDict.get("startTime", None), dataDict.get("endTime", None),
                 dataDict.get("createPerson", None), dataDict.get("createTime", None),
                 dataDict.get("executePerson", None), dataDict.get("executeTime", None), dataDict.get("isDone", None))
    table = insertToSQL(MemberTempContract, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataMemberTempContract", methods=["POST"])
@jwt_required
@updateLog('data_member_temp_contract')
def updataMemberTempContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'productName', u'projectRate', u'contractType', u'isDone']
    table = updataById(MemberTempContract, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
