# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById,addTokenToSql
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.Boss.UserRoleCheck import UserRoleCheck, tableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog
from models.Boss.UserRole import UserRole
from models.Boss.Role import Role
from models.Boss.User import User,tableChangeDic as userChangeDic

# 获取 列表
@app.route("/findUserRoleCheckByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_user_role_check')
def findUserRoleCheckBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = "view_role_check_user"
    intColumnClinetNameList = [u'id', u'userId', u'roleId', u'checkStatus',"roleType"]
    newChange= {"roleName":"role_name"}
    newChange = dict(dict(tableChangeDic,**userChangeDic),**newChange)
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, newChange, intColumnClinetNameList, tablename,orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "userId": tableData[1],
                        "roleId": tableData[2],
                        "checkStatus": tableData[3],
                        "checkPerson": tableData[4],
                        "checkRemark": tableData[5],
                        "checkTime": tableData[6],
                        "createTime": tableData[7],
                        "adminName":  tableData[8],
                        "adminRealName":  tableData[9],
                        "adminTelephone":  tableData[10],
                        "adminEmail":  tableData[11],
                        "roleName":  tableData[12],
                        "roleType":  tableData[13]}
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getUserRoleCheckDetail", methods=["POST"])
@jwt_required
@queryLog('boss_user_role_check')
def getUserRoleCheckDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserRoleCheck, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "userId": table.user_id,
                "roleId": table.role_id,
                "checkStatus": table.check_status,
                "checkPerson": table.check_person,
                "checkRemark": table.check_remark,
                "checkTime": table.check_time,
                "createTime": table.create_time, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserRoleCheck", methods=["POST"])
@jwt_required
@deleteLog('boss_user_role_check')
def deleteUserRoleCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("ids", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserRoleCheck, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserRoleCheck", methods=["POST"])
@jwt_required
@addLog('boss_user_role_check')
def addUserRoleCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    userId = get_jwt_identity()
    roleId = dataDict.get("roleId", None)
    roleType = dataDict.get("roleType",None)
    if not (roleId and roleType):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    checkStatus = 1
    now = getTimeStrfTimeStampNow()
    userRole = UserRole.query.filter(UserRole.user_id == userId, UserRole.role_id == roleId).first()
    tableInfo = UserRoleCheck.query.filter(UserRoleCheck.user_id == userId, UserRoleCheck.role_id == roleId,
                                           UserRoleCheck.check_status == 1).first()
    if roleType == 1:
        if userRole:
            resultDict = returnErrorMsg("you also has this role")
            return jsonify(resultDict)

        if tableInfo:
            resultDict = returnErrorMsg(errorCode["role_check_delete_add"])
            return jsonify(resultDict)
    elif roleType == 2:
        if not userRole:
            resultDict = returnErrorMsg("you  has not this role")
            return jsonify(resultDict)
        if tableInfo:
            resultDict = returnErrorMsg(errorCode["role_check_delete_add"])
            return jsonify(resultDict)

    columsStr = (userId, roleId, checkStatus, None, None, None, now,roleType)
    table = insertToSQL(UserRoleCheck, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新
@app.route("/updataUserRoleCheck", methods=["POST"])
@jwt_required
@updateLog('boss_user_role_check')
def updataUserRoleCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'userId', u'roleId', u'checkStatus']
    table = updataById(UserRoleCheck, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)


# 审核
@app.route("/checkUserRoleCheck", methods=["POST"])
@jwt_required
@updateLog('boss_user_role_check')
def checkUserRoleCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStauts = dataDict.get("checkStatus", None)
    if not (id and checkStauts):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminTable = current_user
    checkPerson = adminTable.admin_name
    checkTime = getTimeStrfTimeStampNow()
    newDict = {
        "checkStatus": checkStauts,
        "checkPerson": checkPerson,
        "checkTime": checkTime,
        "checkRemark": dataDict.get("remark", None),
    }
    dbOperation = OperationOfDB()
    # 审核成功
    if checkStauts == 2:
        # 获取审核表
        checkInfo = findById(UserRoleCheck, "id", id)
        if not checkInfo:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        userId = checkInfo.user_id
        roleId = checkInfo.role_id
        roleType= checkInfo.role_type
        # 是否有重复
        roleTable = UserRole.query.filter(UserRole.user_id == userId, UserRole.role_id == roleId).first()
        if roleType == 1:
            if roleTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("user also has this role")
                return jsonify(resultDict)
            # 创建新的 用户角色表
            columnsStr = (roleId, userId)
            infoTable = dbOperation.insertToSQL(UserRole, *columnsStr)
        elif roleType ==2:
            if not roleTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["param_error"])
                return jsonify(resultDict)
            infoTable= dbOperation.deleteByIdBoss(UserRole,roleTable.id,"id")
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        if not infoTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["system_error"])
            return jsonify(resultDict)
    else:
        pass

    table = dbOperation.updateThis(UserRoleCheck, UserRoleCheck.id, id, newDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnMsg({})
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
