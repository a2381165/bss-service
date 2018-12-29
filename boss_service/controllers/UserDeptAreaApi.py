# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, executeSql
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.Boss.UserDeptArea import UserDeptArea, tableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog
from models.Boss.User import User
from models.Boss.UserRole import UserRole
from models.Boss.Organization import Organization
from models.Data.Department import Department


# 获取 列表
@app.route("/findUserDeptAreaByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_user_dept_area')
def findUserDeptAreaBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = UserDeptArea.__tablename__
    intColumnClinetNameList = [u'id', u'userId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "userId": tableData[1],
                        "areaCode": tableData[2],
                        "createTime": tableData[3], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getUserDeptAreaDetail", methods=["POST"])
@jwt_required
@queryLog('boss_user_dept_area')
def getUserDeptAreaDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserDeptArea, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "userId": table.user_id,
                "areaCode": table.area_code,
                "createTime": table.create_time, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserDeptArea", methods=["POST"])
@jwt_required
@deleteLog('boss_user_dept_area')
def deleteUserDeptArea():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserDeptArea, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserDeptArea", methods=["POST"])
@jwt_required
@addLog('boss_user_dept_area')
def addUserDeptArea():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("userId", None), dataDict.get("areaCode", None), dataDict.get("createTime", None))
    table = insertToSQL(UserDeptArea, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataUserDeptArea", methods=["POST"])
@jwt_required
@updateLog('boss_user_dept_area')
def updataUserDeptArea():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'userId']
    table = updataById(UserDeptArea, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
