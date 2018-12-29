# coding:utf-8
import datetime

from flask import request, jsonify, json
from flask_jwt_extended import jwt_required, create_refresh_token, create_access_token, get_jti, current_user

from common.Log import addLog, updateLog
from common.OperationOfDB import addTokenToSql, insertToSQL
from common.OperationOfDB import findById
from common.ReturnMessage import returnErrorMsg, returnMsg, returnErrorMsg, errorCode
from common.UserPasswordEncrypt import PasswordSort
from models.Boss.User import User
from models.Boss.UserLog import UserLog
from models.Boss.UserRole import UserRole
from version.v3.bossConfig import app


# 管理员登录
@app.route("/adminLogin", methods=["POST"])
def adminLogin():
    if not request.json:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    adminName = dataDict.get("adminName", None)
    adminPassword = dataDict.get("adminPassword", None)
    if adminName and adminPassword:
        passwordSort = PasswordSort()
        encryptPassword = passwordSort.passwordEncrypt(adminPassword)
        adminTable = User.query.filter(User.admin_name == adminName, User.admin_password == encryptPassword).first()
        # admins = findByNameAndPassword(User, "admin_name", adminName, "admin_password", encryptPassword)
        if not adminTable:
            dictInfo = "Bad adminName or adminPassword"
            resultDict = returnErrorMsg(dictInfo)
        else:
            if adminTable.is_lock != 1:
                resultDict = returnErrorMsg("User Disable")
                return jsonify(resultDict)
            adminId = adminTable.admin_id
            accessToken = create_access_token(identity=adminId)
            refreshToken = create_refresh_token(identity=adminId)
            accessTokenJti = get_jti(accessToken)
            refreshTokenJti = get_jti(refreshToken)
            adminTable.admin_token = accessTokenJti
            adminTable.admin_refresh_token = refreshTokenJti
            adminTable = addTokenToSql(adminTable)
            try:
                # roleId = adminTable.adminRole.first().role.role_id
                table = findById(UserRole, "user_id", adminTable.admin_id)
                if table:
                    roleId = table.role_id
                else:
                    resultDict = returnErrorMsg("the User user not have a role relationship!")
                    return jsonify(resultDict)
                    # roleId = adminTable.adminRole.first().role_id
            except:
                resultDict = returnErrorMsg("the User user not have a role relationship!")
                return jsonify(resultDict)
            userIp = request.remote_addr
            datetimeNow = datetime.datetime.now()
            columnStr = (adminId, adminName, None, userIp, "login", "", datetimeNow)
            logTable = insertToSQL(UserLog, *columnStr)
            if not logTable:
                resultDict = returnErrorMsg(errorCode["system_error"])
                return jsonify(resultDict)
            dictInfo = {
                "adminId": adminTable.admin_id,
                "roleId": roleId,
                'adminName': adminTable.admin_name,
                'adminRealName': adminTable.admin_real_name,
                "adminToken": accessToken,
                "adminRefreshToken": refreshToken,
            }
            resultDict = returnMsg(dictInfo)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 管理员退出
@app.route("/adminLogout", methods=["POST"])
@jwt_required
@addLog("boss_user")
def adminLogout():
    current_user.admin_token = None
    current_user.admin_refresh_token = None
    addTokenToSql(current_user)
    resultDict = returnMsg("logout success")
    return jsonify(resultDict)


# 管理员重置密码
@app.route('/resetAdminPassword', methods=["POST"])
@jwt_required
@updateLog("boss_user")
def resetAdminPassword():
    if not request.json:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    oldAdminPassword = dataDict.get("oldAdminPassword", None)
    newAdminPassword = dataDict.get("newAdminPassword", None)
    if not (oldAdminPassword and newAdminPassword):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    passwordSort = PasswordSort()
    encryptOldPassword = passwordSort.passwordEncrypt(oldAdminPassword)
    encrypeNewPassword = passwordSort.passwordEncrypt(newAdminPassword)
    if current_user:
        if encryptOldPassword == current_user.admin_password:
            current_user.admin_password = encrypeNewPassword
            # token 设置为空 需要重新登录
            current_user.admin_token = None
            current_user.admin_refresh_token = None
            adminFinTable = addTokenToSql(current_user)
            if adminFinTable:
                infoDict = {}
                resultDict = returnMsg(infoDict)
            else:
                resultDict = returnErrorMsg("change info failed")
        else:
            resultDict = returnErrorMsg("the oldPassword incorrect!")
    elif current_user == 0:
        resultDict = returnErrorMsg(errorCode["param_error"])
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)
