# coding:utf-8

import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required,get_jwt_identity

from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnErrorMsg, returnMsg, returnErrorMsg,errorCode
from models.Boss.Role import Role
from models.Boss.User import User
from models.Boss.UserRole import UserRole, tableChangeDic
from version.v3.bossConfig import app
from models.Boss.UserRoleCheck import UserRoleCheck


# 查询角色名单
@app.route("/roleFilter", methods=["POST"])
@jwt_required
@queryLog("boss_role")
def roleFilter():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = 1
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    for condition in dataDict["condition"]:
        field = condition.get("field")
        value = condition.get("value")
        if field == "roleId":
            roleId = value
            dataDict["condition"].remove(condition)
    sqlStr = "select admin_real_name,admin_telephone,admin_email,admin_name from view_role_admin where (role_id = %s or role_id = 1) and    " % roleId
    intColumnClinetNameList = ("Id", "roleId", "adminId", "rolePid", "IsSys")
    groupBy = "group by admin_id"
    adminRoleTableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, None, sqlStr,
                                                      groupBy)
    infoList = []
    for adminRoleTable in adminRoleTableList:
        infoDict = {
            "adminRealName": adminRoleTable[0],
            "adminTelephone": adminRoleTable[1],
            "adminEmail": adminRoleTable[2],
            "adminName": adminRoleTable[3]
        }
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    resultDict["total"] = count
    return jsonify(resultDict)


# 保存信息
@app.route("/preserveRoleAdmin", methods=["POST"])
@jwt_required
@updateLog("boss_role")
def preserveRoleAdmin():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = []
    adminIdList = dataDict.get("adminId", [])
    roleId = dataDict.get("roleId", None)
    if roleId == None:
        resultDict = returnErrorMsg("not find roleId or adminId!")
        return jsonify(resultDict)
    roleTable = findById(Role, "role_id", roleId)
    if roleTable:
        dbOperation = OperationOfDB()
        idList.append(roleId)
        resualtList = []
        resualtDictInfo = dbOperation.deleteByColumn(UserRole, idList, "role_id")
        if not resualtDictInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("not find role_id")
            return jsonify(resultDict)
        for adminId in adminIdList:
            adminTable = findById(User, "admin_id", adminId)
            if adminTable:
                columnsStr = (roleId, adminId)
                adminRoleTable = dbOperation.insertToSQL(UserRole, *columnsStr)
                if adminRoleTable:
                    resultDict = returnMsg({})
                    resualtList.append(resultDict)
                else:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("insert fail")
                    return jsonify(resultDict)
        if dbOperation.commitToSQL():
            resualtInfo = returnMsg(resualtList)
        else:
            dbOperation.commitRollback()
            resualtInfo = returnErrorMsg("inset fail")
    else:
        resualtInfo = returnErrorMsg("the roleId not exit!")
    return jsonify(resualtInfo)


# 条件查询
@app.route("/findAdminRoleByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_role")
def findAdminRoleByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    intColumnClinetNameList = ("Id", "roleId", "adminId", "rolePid", "IsSys")
    className = "view_role_user"
    adminsList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, className)
    if adminsList:
        InfoList = []
        for tableData in adminsList:
            infoDict = {
                "id": tableData[0],
                "adminId": tableData[1],
                "adminName": tableData[2],
                "adminDesc": tableData[7],
                "adminRealName": tableData[8],
                "adminTelephone": tableData[9],
                "adminEmail": tableData[10],
                "adminAddTime": tableData[11],
                "isLock": tableData[12],
                "ozId": tableData[13],
                "roleId": tableData[14],
                "rolePid": tableData[15],
                "roleName": tableData[16],
                "roleDesc": tableData[17],
                "isSys": tableData[18],
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

# 条件查询 # 登录页 获取自己的角色
@app.route("/findOwnRoleByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_role")
def findOwnRoleByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    userId = get_jwt_identity()
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    condition = dataDict.get("condition",[])
    newDict = {
        "field":"adminId",
        "op":"equal",
        "value":userId
    }
    condition.append(newDict)
    intColumnClinetNameList = ("Id", "roleId", "adminId", "rolePid", "IsSys",)
    className = "view_role_user"
    otherChangeDic = {"adminId":"admin_id"}
    allChagneDic = dict(tableChangeDic,**otherChangeDic)
    adminsList, count = conditionDataListFind(dataDict, allChagneDic, intColumnClinetNameList, className)
    if adminsList:
        InfoList = []
        for tableData in adminsList:
            # UserRoleCheck.query.filter(UserRoleCheck.role_id==tableData[14],UserRoleCheck.user_id==tableData[1]).first()
            infoDict = {
                "id": tableData[0],
                'adminId': tableData[1],
                'adminName': tableData[2],
                # 'adminToken': tableData[3],
                # 'adminRefreshToken': tableData[4],
                # 'adminSalt': tableData[5],
                # 'adminPassword': tableData[6],
                'adminDesc': tableData[7],
                'adminRealName': tableData[8],
                'adminTelephone': tableData[9],
                'adminEmail': tableData[10],
                'adminAddTime': str(tableData[11]),
                'roleId': tableData[14],
                'rolePid': tableData[15],
                'roleName': tableData[16],
                'roleDesc': tableData[17],
                'IsSys': tableData[18]
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

# 删除信息
@app.route("/deleteAdmin", methods=["POST"])
@jwt_required
@deleteLog("boss_role")
def deleteAdminRole():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    adminId = dataDict.get("adminId", None)
    roleId = dataDict.get("roleId", None)
    otherConditons = ""
    if roleId != None:
        otherConditons = otherConditons + " and role_id = %s" % roleId
    if adminId != None:
        otherConditons = otherConditons + " and admin_id = %s" % adminId
    if otherConditons == "":
        otherConditons = None

    resultDict = deleteById(UserRole, idList, "id", otherConditons)
    return jsonify(resultDict)


# 查看详情
@app.route("/findAdminRoleById", methods=["POST"])
@jwt_required
@queryLog("boss_role")
def findAdminRoleById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('Id', None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminRoleTable = findById(UserRole, "id", id)
    if adminRoleTable:
        infoDict = tableDictSort(adminRoleTable)
        resultDict = returnMsg(infoDict)
    elif adminRoleTable == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 添加
@app.route("/addAdminRole", methods=["POST"])
@jwt_required
@addLog("boss_role")
def addAdminRole():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnsStr = (dataDict.get('roleId', None), dataDict.get('adminId', None))

    table = insertToSQL(UserRole, *columnsStr)
    if table:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def tableDictSort(table):
    tableDict = {
        "Id": table.id,
        "adminId": table.admin.admin_id,
        'adminName': table.admin.admin_name,
        'adminToken': table.admin.admin_token,
        'adminRefreshToken': table.admin.admin_refresh_token,
        'adminSalt': table.admin.admin_salt,
        'adminPassword': table.admin.admin_password,
        'adminDesc': table.admin.admin_desc,
        'adminRealName': table.admin.admin_real_name,
        'adminTelephone': table.admin.admin_telephone,
        'adminEmail': table.admin.admin_email,
        'adminAddTime': str(table.admin.admin_add_time),
        'roleId': table.role.role_id,
        'rolePid': table.role.role_pid,
        'roleName': table.role.role_name,
        'roleDesc': table.role.role_desc,
        'isSys': table.role.is_sys
    }
    tableDict = dictRemoveNone(tableDict)
    return tableDict
