# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, current_user

from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, insertToSQL, updataById, deleteByIdBoss
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.ServiceAttach import ServiceAttach, ServiceAttachChangeDic as tableChangeDic
from version.v3.bossConfig import app


# 获取 列表
@app.route("/findServiceAttachByCondition", methods=["POST"])
@jwt_required
@queryLog('data_service_attach')
def findServiceAttachBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = ServiceAttach.__tablename__
    intColumnClinetNameList = [u'id', u'type']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "attachExtensionName": tableData[1],
                        "attachSize": tableData[2],
                        "attachTitle": tableData[3],
                        "attachPath": tableData[4],
                        "createTime": tableData[5],
                        "type": tableData[6],
                        "createPerson": tableData[7], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getServiceAttachDetail", methods=["POST"])
@jwt_required
@queryLog('data_service_attach')
def getServiceAttachDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(ServiceAttach, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "attachExtensionName": table.attach_extension_name,
                "attachSize": table.attach_size,
                "attachTitle": table.attach_title,
                "attachPath": table.attach_path,
                "createTime": table.create_time,
                "type": table.type,
                "createPerson": table.create_person, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteServiceAttach", methods=["POST"])
@jwt_required
@deleteLog('data_service_attach')
def deleteServiceAttach():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("ids", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminName = current_user.admin_name
    otherCondition = " and create_person='{}'".format(adminName)
    count = deleteByIdBoss(ServiceAttach, ids, "id", otherCondition=otherCondition)
    if len(ids) == count:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["serviceAttach_delete"])
        return jsonify(resultDict)


# 添加 
@app.route("/addServiceAttach", methods=["POST"])
@jwt_required
@addLog('data_service_attach')
def addServiceAttach():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (
        dataDict.get("attachExtensionName", None), dataDict.get("attachSize", None), dataDict.get("attachTitle", None),
        dataDict.get("attachPath", None), dataDict.get("createTime", None), dataDict.get("type", None),
        dataDict.get("createPerson", None))
    table = insertToSQL(ServiceAttach, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataServiceAttach", methods=["POST"])
@jwt_required
@updateLog('data_service_attach')
def updataServiceAttach():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'type']
    adminName = current_user.admin_name
    otherCondition = " and create_person='{}'".format(adminName)
    table = updataById(ServiceAttach, dataDict, "id", id, tableChangeDic,
                       intColumnClinetNameList=intColumnClinetNameList, otherCondition=otherCondition)
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
