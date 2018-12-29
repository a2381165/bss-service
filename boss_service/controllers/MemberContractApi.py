# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Member.MemberContract import MemberContract, MemberContractChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取 列表 已签约
@app.route("/findMemberContractByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_member_contract')
def findMemberContractByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = MemberContract.__tablename__
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


# 获取 列表 已立项
@app.route("/findViewMemberContractByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_member_contract')
def findViewMemberContractByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = "view_contract_file_member"
    intColumnClinetNameList = intList + ["fileStatus"]
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, view_contract_file_member_change, intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = view_contract_file_member_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getMemberContractDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_member_contract')
def getMemberContractDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(MemberContract, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteMemberContract", methods=["POST"])
@jwt_required
@deleteLog('zzh_member_contract')
def deleteMemberContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(MemberContract, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 添加
@app.route("/addMemberContract", methods=["POST"])
@jwt_required
@addLog('zzh_member_contract')
def addMemberContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    orderNo = dataDict.get("orderNo", None)
    serviceNo = dataDict.get("serviceNo", None)
    itemTitle = dataDict.get("itemTitle", None)
    contractNo = dataDict.get("contractNo", None)
    contractAnnex = dataDict.get("contractAnnex", None)
    contractRemark = dataDict.get("contractRemark", None)
    contractType = dataDict.get("contractType", None)
    contractPrice = dataDict.get("contractPrice", None)
    startFee = dataDict.get("startFee", None)
    projectFee = dataDict.get("projectFee", None)
    projectRate = dataDict.get("projectRate", None)
    isGenerate = dataDict.get("isGenerate", None)
    startTime = dataDict.get("startTime", None)
    endTime = dataDict.get("endTime", None)
    signingPerson = dataDict.get("signingPerson", None)
    createPerson = dataDict.get("createPerson", None)
    createTime = dataDict.get("createTime", None)
    columsStr = (
        id, orderNo, serviceNo, itemTitle, contractNo, contractAnnex, contractRemark, contractType, contractPrice,
        startFee,
        projectFee, projectRate, isGenerate, startTime, endTime, signingPerson, createPerson, createTime)
    table = insertToSQL(MemberContract, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataMemberContract", methods=["POST"])
@jwt_required
@updateLog('zzh_member_contract')
def updataMemberContract():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(MemberContract, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


def tableSort(table):
    _infoDict = {"id": table.id,
                 "orderNo": table.order_no,
                 "serviceNo": table.service_no,
                 "itemTitle": table.item_title,
                 "contractNo": table.contract_no,
                 "contractAnnex": table.contract_annex,
                 "contractRemark": table.contract_remark,
                 "contractType": table.contract_type,
                 "contractPrice": table.contract_price,
                 "startFee": table.start_fee,
                 "projectFee": table.project_fee,
                 "projectRate": table.project_rate,
                 "isGenerate": table.is_generate,
                 "startTime": table.start_time,
                 "endTime": table.end_time,
                 "signingPerson": table.signing_person,
                 "createPerson": table.create_person,
                 "createTime": table.create_time, }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id": tableData[0],
                 "orderNo": tableData[1],
                 "serviceNo": tableData[2],
                 "itemTitle": tableData[3],
                 "contractNo": tableData[4],
                 "contractAnnex": tableData[5],
                 "contractRemark": tableData[6],
                 "contractType": tableData[7],
                 "contractPrice": tableData[8],
                 "startFee": tableData[9],
                 "projectFee": tableData[10],
                 "projectRate": tableData[11],
                 "isGenerate": tableData[12],
                 "startTime": tableData[13],
                 "endTime": tableData[14],
                 "signingPerson": tableData[15],
                 "createPerson": tableData[16],
                 "createTime": tableData[17], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def view_contract_file_member_fun(tableData):
    _infoDict = {"id": tableData[0],
                 "contractNo": tableData[1],
                 "fileStatus": tableData[2],
                 "fileNum": tableData[3],
                 "transferPerson": tableData[4],
                 "transferTime": tableData[5],
                 "filePerson": tableData[6],
                 "fileTime": tableData[7],
                 "remark": tableData[8],
                 "createTime": tableData[9],
                 "orderNo": tableData[10],
                 "serviceNo": tableData[11],
                 "itemTitle": tableData[12],
                 "contractAnnex": tableData[13],
                 "contractRemark": tableData[14],
                 "contractType": tableData[15],
                 "contractPrice": tableData[16],
                 "startFee": tableData[17],
                 "projectFee": tableData[18],
                 "projectRate": tableData[19],
                 "isGenerate": tableData[20],
                 "startTime": tableData[21],
                 "endTime": tableData[22],
                 "signingPerson": tableData[23], }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_contract_file_member_change = {
    "id": "id",
    "contractNo": "contract_no",
    "fileStatus": "file_status",
    "fileNum": "file_num",
    "transferPerson": "transfer_person",
    "transferTime": "transfer_time",
    "filePerson": "file_person",
    "fileTime": "file_time",
    "remark": "remark",
    "createTime": "create_time",
    "orderNo": "order_no",
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
}
