# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate,getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById,deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.Zzh.MemberEnterpriseContactInfo import MemberEnterpriseContactInfo, tableChangeDic,intList
from common.Log import queryLog,addLog,deleteLog,updateLog



# 获取 列表 
@app.route("/findMemberEnterpriseContactInfoByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_member_enterprise_contact_info')
def findMemberEnterpriseContactInfoByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = MemberEnterpriseContactInfo.__tablename__
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc " 
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename,orderByStr=orderByStr)
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


# 获取详情 
@app.route("/getMemberEnterpriseContactInfoDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_member_enterprise_contact_info')
def getMemberEnterpriseContactInfoDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(MemberEnterpriseContactInfo, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteMemberEnterpriseContactInfo", methods=["POST"])
@jwt_required
@deleteLog('zzh_member_enterprise_contact_info')
def deleteMemberEnterpriseContactInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(MemberEnterpriseContactInfo, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)



# 添加 
@app.route("/addMemberEnterpriseContactInfo", methods=["POST"])
@jwt_required
@addLog('zzh_member_enterprise_contact_info')
def addMemberEnterpriseContactInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    enterpriseId = dataDict.get("enterpriseId", None)
    contractPerson = dataDict.get("contractPerson", None)
    contractPhone = dataDict.get("contractPhone", None)
    contractDuty = dataDict.get("contractDuty", None)
    contractEmail = dataDict.get("contractEmail", None)
    contractWeixin = dataDict.get("contractWeixin", None)
    columsStr = (enterpriseId,contractPerson,contractPhone,contractDuty,contractEmail,contractWeixin)
    table = insertToSQL(MemberEnterpriseContactInfo, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataMemberEnterpriseContactInfo", methods=["POST"])
@jwt_required
@updateLog('zzh_member_enterprise_contact_info')
def updataMemberEnterpriseContactInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById(MemberEnterpriseContactInfo, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

def tableSort(table):
    _infoDict = {"id":table.id,
                "enterpriseId":table.enterprise_id,
                "contractPerson":table.contract_person,
                "contractPhone":table.contract_phone,
                "contractDuty":table.contract_duty,
                "contractEmail":table.contract_email,
                "contractWeixin":table.contract_weixin,}
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = {"id":tableData[0],
                "enterpriseId":tableData[1],
                "contractPerson":tableData[2],
                "contractPhone":tableData[3],
                "contractDuty":tableData[4],
                "contractEmail":tableData[5],
                "contractWeixin":tableData[6],}
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict

