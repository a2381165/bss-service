# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind, updataById
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Boss.Organization import Organization
from models.Boss.Role import Role, tableChangeDic
from models.Boss.User import User
from models.Boss.UserRole import UserRole
from models.Boss.UserRoleCheck import UserRoleCheck
from version.v3.bossConfig import app


# 修改角色信息
@app.route("/updateRole", methods=["POST"])
@jwt_required
@updateLog("boss_role")
def updateRole():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "role_id"
    intColumnClinetNameList = ("roleId", "rolePid", "isSys", "isLock", "ozId")
    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in idList:
        roleUp = updataById(Role, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if roleUp == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif roleUp == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        else:
            infoDic = tableDictSort(roleUp)
        infoList.append(infoDic)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 删除角色信息
@app.route("/deleteRole", methods=["POST"])
@jwt_required
@deleteLog("boss_role")
def deleteRole():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in ids:
        table = Role.query.filter(Role.role_pid == id).all()
        if table:
            resultDict = returnErrorMsg(errorCode["role_role"])
            return jsonify(resultDict)
        roleTable = Role.query.filter(Role.role_id == id).first()
        if roleTable.is_sys == 1:
            resultDict = returnErrorMsg(errorCode["role_sys"])
            return jsonify(resultDict)
        userRoleInfo = UserRole.query.filter(UserRole.role_id == id).first()
        if userRoleInfo:
            resultDict = returnErrorMsg(errorCode["role_people"])
            return jsonify(resultDict)
    resultDict = deleteById(Role, ids, "role_id")
    return jsonify(resultDict)


@app.route("/findRoleByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_role")
def findRoleByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("roleId", "rolePid", "isSys", "isLock", "ozId")
    tableName = Role.__tablename__
    adminsList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    if adminsList:
        adminInfoList = []
        for adminData in adminsList:
            ozName = ""
            ozPid = ""
            ozInfo = findById(Organization, "id", adminData[6])
            if ozInfo:
                ozName = ozInfo.oz_name
                ozPid = ozInfo.oz_pid
            admin = {
                "roleId": adminData[0],
                "rolePid": adminData[1],
                "roleName": adminData[2],
                "roleDesc": adminData[3],
                "isSys": adminData[4],
                "isLock": adminData[5],
                "ozId": adminData[6],
                "managerName": adminData[7],
                "managerRealName": adminData[8],
                'ozName': ozName,
                'ozPid': ozPid,

            }
            adminInfoList.append(admin)
        resultDict = returnMsg(adminInfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 条件查询
@app.route("/findNotOtherRoleByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_role")
def findNotOtherRoleByCondition():
    userId = get_jwt_identity()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition", [])
    uesrRoleList = UserRole.query.filter(UserRole.user_id == userId).all()
    userRoleIds = [userrole.role_id for userrole in uesrRoleList]
    roleList = Role.query.filter(Role.role_id.notin_(userRoleIds)).all()
    roleIds = [int(role.role_id) for role in roleList]
    newDict = [{
        "field": "roleId",
        "op": "in",
        "value": tuple(roleIds)
    }, {
        "field": "isLock",
        "op": "equal",
        "value": 1
    }]
    condition += newDict
    intColumnClinetNameList = ("roleId", "rolePid", "isSys", "isLock", "ozId")
    tableName = Role.__tablename__
    adminsList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    if adminsList:
        adminInfoList = []
        for adminData in adminsList:
            admin = {
                "roleId": adminData[0],
                "rolePid": adminData[1],
                "roleName": adminData[2],
                "roleDesc": adminData[3],
                "isSys": adminData[4],
                "isLock": adminData[5],
                "ozId": adminData[6],
                "managerName": adminData[7],
                "managerRealName": adminData[8],
            }
            adminInfoList.append(admin)
        resultDict = returnMsg(adminInfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 没有 申请 没有 的条件查询
@app.route("/findOtherRoleByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_role")
def findOtherRoleByCondition():
    userId = get_jwt_identity()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition", [])
    uesrRoleList = UserRole.query.filter(UserRole.user_id == userId).all()
    userRoleIds = [userrole.role_id for userrole in uesrRoleList]
    roleList = Role.query.filter(Role.role_id.notin_(userRoleIds)).all()
    # if role.role_id == 1 or role.role_pid != 0
    roleIds = [int(role.role_id) for role in roleList ]
    checkRoleList = UserRoleCheck.query.filter(UserRoleCheck.user_id == userId, UserRoleCheck.check_status == 1).all()
    checkRoleIds = [int(checkRole.role_id) for checkRole in checkRoleList if checkRole]
    newDict = [{
        "field": "roleId",
        "op": "in",
        "value": tuple(set(roleIds) ^ set(checkRoleIds))
    }, {
        "field": "isLock",
        "op": "equal",
        "value": 1
    }]
    condition += newDict
    intColumnClinetNameList = ("roleId", "rolePid", "isSys", "isLock", "ozId")
    tableName = Role.__tablename__
    adminsList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    if adminsList:
        adminInfoList = []
        for adminData in adminsList:
            admin = {
                "roleId": adminData[0],
                "rolePid": adminData[1],
                "roleName": adminData[2],
                "roleDesc": adminData[3],
                "isSys": adminData[4],
                "isLock": adminData[5],
                "ozId": adminData[6],
                "managerName": adminData[7],
                "managerRealName": adminData[8],
            }
            adminInfoList.append(admin)
        resultDict = returnMsg(adminInfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 根据ID查询信息
@app.route("/findRoleById", methods=["POST"])
@jwt_required
@queryLog("boss_role")
def findRoleById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('roleId', None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(Role, "role_id", id)
    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    elif table == 0:
        admin = {}
        resultDict = returnMsg(admin)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 增加角色信息
@app.route("/addRole", methods=["POST"])
@jwt_required
@addLog("boss_role")
def addRole():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ozId = dataDict.get("ozId", None)
    if not ozId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    columnsStr = (dataDict.get('rolePid', None), dataDict.get('roleName', None), dataDict.get('roleDesc', None),
                  dataDict.get('isSys', 1), dataDict.get('isLock', 0), ozId)
    table = insertToSQL(Role, *columnsStr)
    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 选择上一层角色
@app.route("/choiceRoleManger", methods=["POST"])
def choiceRoleManger():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    roleInfo = UserRole.query.filter(UserRole.role_id==roleId).all()
    infoList = []
    if roleInfo :
        for role in roleInfo:
            userInfo = findById(User, "admin_id", role.user_id)
            adminName = ""
            adminRealName = ""
            if userInfo:
                adminName = userInfo.admin_name
                adminRealName = userInfo.admin_real_name
            infoDict = {
                "roleId":roleId,
                "managerName": adminName,
                "managerRealName": adminRealName,
            }
            infoList.append(infoDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)

# 更新 管理人


def tableDictSort(table):
    infoDict = {
        "roleId": table.role_id,
        "rolePid": table.role_pid,
        "roleName": table.role_name,
        "roleDesc": table.role_desc,
        "isSys": table.is_sys,
        "isLock": table.is_lock,
        "ozId": table.oz_id,
        "managerName": table.manager_name,
        "managerRealName": table.manager_real_name,
    }
    return infoDict
