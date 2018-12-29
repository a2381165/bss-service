# coding:utf-8

import json

from flask import request, json, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from common.DatatimeNow import returnEmailCodeTime
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind, updataById, addTokenToSql
from common.ReturnMessage import returnErrorMsg, returnMsg, returnErrorMsg,errorCode
from common.UserPasswordEncrypt import PasswordSort
from models.Boss.Organization import tableChangeDic as ozChangeDic
from models.Boss.User import User, tableChangeDic
from version.v3.bossConfig import app


# 通过管理员名称 查找
@app.route("/findAdminByName", methods=["POST"])
@jwt_required
@queryLog('boss_user')
def findAdminByName():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    name = dataDict.get('adminName', None)
    if name == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(User, "admin_name", name, isStrcheck=True)
    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    elif table == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 通过管理员id 查找具体信息
@app.route("/findAdminById", methods=["POST"])
@jwt_required
@queryLog('boss_user')
def findAdminById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('adminId', None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    else:
        table = findById(User, "admin_id", id)
        if table:
            infoDict = tableDictSort(table)
            resultDict = returnMsg(infoDict)
        elif table == 0:
            infoDict = {}
            resultDict = returnMsg(infoDict)
        else:
            resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 通过 ids 删除管理员
@app.route("/deleteAdmin", methods=["POST"])
@jwt_required
@deleteLog('boss_user')
def deleteAdminByIds():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    table = deleteById(User, idList, "admin_id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 通过 条件 查询管理员
@app.route("/findAdminByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_user')
def findAdminByCondition():
    adminId = get_jwt_identity()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    else:
        intColumnClinetNameList = ("adminId", "isLock", 'ozId', 'ozPid', 'ozSort', 'isLock')
        # tableName = User.__tablename__
        tableName = "view_user_organization"
        newChangeDic = dict(tableChangeDic, **ozChangeDic)
        adminsList, count = conditionDataListFind(dataDict, newChangeDic, intColumnClinetNameList, tableName)
        if adminsList:
            adminInfoList = []
            for adminData in adminsList:
                if adminData[11] == -1:
                    continue
                adminDict = {
                    "adminId": adminData[0],
                    'adminName': adminData[1],
                    # "adminToken": adminData[2],
                    # "adminRefreshToken": adminData[3],
                    'adminSalt': adminData[4],
                    # 'adminPassword': adminData[5],
                    'adminDesc': adminData[6],
                    'adminRealName': adminData[7],
                    'adminTelephone': adminData[8],
                    'adminEmail': adminData[9],
                    "adminAddTime": str(adminData[10]),
                    'adminIsLock': adminData[11],
                    'ozId': adminData[12],
                    "ozName": adminData[13],
                    "ozPid": adminData[14],
                    "ozSort": adminData[15],
                    "ozCode": adminData[16],
                    "ozIsLock": adminData[17],
                    "remark": adminData[18],
                }
                adminDict = dictRemoveNone(adminDict)
                adminInfoList.append(adminDict)
            resultDict = returnMsg(adminInfoList)
            resultDict["total"] = count
        else:
            resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 添加管理员
@app.route("/addAdmin", methods=["POST"])
@jwt_required
@addLog('boss_user')
def addAdmin():
    adminId = get_jwt_identity()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    timeNow, expireTime = returnEmailCodeTime()
    adminTelephone = dataDict.get('adminTelephone')
    if adminTelephone == None or len(adminTelephone) < 11:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    adminPassword = dataDict.get('adminPassword', "123456")
    passwordSort = PasswordSort()
    # encryptPassword = passwordSort.passwordEncryptSlat(adminPassword)
    encryptPassword = passwordSort.passwordEncrypt(adminPassword)
    columnsStr = (dataDict.get('adminName', None), None, None,
                  dataDict.get('adminSalt', "zzh"), encryptPassword, dataDict.get('adminDesc', None),
                  dataDict.get('adminRealName', None), dataDict.get('adminTelephone', None),
                  dataDict.get('adminEmail', None),
                  timeNow, dataDict.get('isLock', 0), dataDict.get("ozId", 0))
    table = insertToSQL(User, *columnsStr)
    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 更新管理员资料
@app.route("/updateAdmin", methods=["POST"])
@jwt_required
@updateLog('boss_user')
def updateAdmin():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    # id = dataDict.get("adminId",None)
    columnId = "admin_id"
    intColumnClinetNameList = ['adminId', 'isLock', 'ozId']
    infoList = []
    idList = dataDict.get("ids", None)

    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in idList:
        if dataDict.get("adminPassword") != None:
            adminPassword = dataDict['adminPassword']
            passwordSort = PasswordSort()
            encryptPassword = passwordSort.passwordEncrypt(adminPassword)
            dataDict["adminPassword"] = encryptPassword
        # if dataDict.get("adminPassword") != None:
        #     oldAdminPassword = dataDict['oldAdminPassword']
        #     adminPassword = dataDict['adminPassword']
        #     passwordSort = PasswordSort()
        #     encryptPassword = passwordSort.passwordEncrypt(oldAdminPassword)
        #     adminTable = User.query.filter(User.admin_id == id).first()
        #     if encryptPassword == adminTable.admin_password:
        #         passwordSort = PasswordSort()
        #         encryptPassword = passwordSort.passwordEncrypt(adminPassword)
        #         dataDict["adminPassword"] = encryptPassword
        #     else:
        #         resultDict = returnErrorMsg(errorCode["param_error"])
        #         return jsonify(resultDict)
        adminUp = updataById(User, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if adminUp == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif adminUp == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        else:
            adminInfoDic = tableDictSort(adminUp)
        infoList.append(adminInfoDic)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 启动/禁止用管理员
@app.route("/controlAdmin", methods=["POST"])
@jwt_required
@updateLog('boss_user')
def controlAdmin():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("adminId", None)
    isLock = dataDict.get("isLock", None)
    # adminId = dataDict.get("adminId")
    if not (id and isLock):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(User, "admin_id", id)
    if table:
        table.is_lock = isLock
        hasTable = addTokenToSql(table)
        if hasTable:
            infoDict = tableDictSort(table)
            resultDict = returnMsg(infoDict)
        else:
            infoDict = {}
            resultDict = returnMsg(infoDict)
    elif table == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def tableDictSort(table):
    infoDict = {
        "adminId": table.admin_id,
        'adminName': table.admin_name,
        'adminPassword': table.admin_password,
        'adminSalt': table.admin_salt,
        'adminDesc': table.admin_desc,
        'adminRealName': table.admin_real_name,
        'adminTelephone': table.admin_telephone,
        'adminEmail': table.admin_email,
        'isLock': table.is_lock,
        "adminToken": table.admin_token,
        "adminRefreshToken": table.admin_refresh_token,
        "adminAddTime": str(table.admin_add_time),
        "ozId": table.oz_id,
    }
    return infoDict
