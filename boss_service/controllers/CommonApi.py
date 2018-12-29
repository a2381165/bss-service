#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/10  11:27
# @Site    : 
# @File    : CommonApi.py
# @Software: PyCharm
from flask import json, jsonify, request, render_template
from flask_jwt_extended import jwt_required

from common.OperationOfDB import conditionDataListFind, findById
from common.OperationOfDB import executeSql
from common.ReturnMessage import returnErrorMsg, returnMsg, errorCode
# from config import cache
from models.Boss.User import User
from models.Data.Aidance import Aidance
from models.Data.SubFlow import SubFlow
from version.v3.bossConfig import app


# 根据角色 选择人员 roleId
@app.route("/choocePerson", methods=["POST"])
@jwt_required
def choocePerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    sql = "select * from boss_user_role as t1 join boss_role as t2 join boss_user as t3 on t1.role_id = t2.role_id and t1.user_id = t3.admin_id and t1.role_id = {}".format(
        roleId)
    resultList = executeSql(sql)
    if resultList:
        infoList = []
        for result in resultList:
            infoDict = {
                "adminId": result.admin_id,
                "adminName": result.admin_name,
                "adminRealName": result.admin_real_name,
                "adminTelephone": result.admin_telephone,
                "adminEmail": result.admin_email,
            }
            infoList.append(infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = len(infoList)
    else:
        resultDict = returnErrorMsg(errorCode["query_fail"])
    return jsonify(resultDict)


# # 根据角色 选择人员 roleId view
@app.route("/choosePersonByCondition", methods=["POST"])
@jwt_required
def choosePersonByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    intColumnClinetNameList = ("Id", "roleId", "adminId", "rolePid", "IsSys")
    className = "view_role_user"
    adminsList, count = conditionDataListFind(dataDict, viewRoleUserChangeDic, intColumnClinetNameList, className)
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


# 订单
# 选择 - 角色人员 flowId 下一级
@app.route("/choiceOrderAidancePerson", methods=["POST"])
@jwt_required
def choiceOrderAidancePerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    flowId = dataDict.get("flowId","")
    if not (flowId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    flow_setp = 2
    tableINfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.sort == flow_setp).first()
    persons = tableINfo.persons
    personName = []
    try:
        for person in persons.split("/"):
            userInfo = User.query.filter(User.admin_name == person).first()
            if userInfo:
                infoDict = {
                    "adminName": userInfo.admin_name,
                    "adminRealName": userInfo.admin_real_name,
                    "adminTelephone": userInfo.admin_telephone,
                    "adminEmail": userInfo.admin_email,
                }
                personName.append(infoDict)
    except:
        pass
    resultDict = returnMsg(personName)
    resultDict["total"] = len(resultDict)
    return jsonify(resultDict)


#  选择同级 人员  flowId 同级
@app.route("/chooseOtherPerson", methods=["POST"])
@jwt_required
def chooseOtherPerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    flowId = dataDict.get("flowId")
    if not (flowId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    flow_setp = 1
    tableINfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.sort == flow_setp).first()
    persons = tableINfo.persons
    personName = []
    try:
        for person in persons.split("/"):
            userInfo = User.query.filter(User.admin_name == person).first()
            if userInfo:
                infoDict = {
                    "adminName": userInfo.admin_name,
                    "adminRealName": userInfo.admin_real_name,
                    "adminTelephone": userInfo.admin_telephone,
                    "adminEmail": userInfo.admin_email,
                }
                personName.append(infoDict)
    except:
        pass
    resultDict = returnMsg(personName)
    resultDict["total"] = len(resultDict)
    return jsonify(resultDict)


# 选择 - 角色人员 - aidaceId
@app.route("/choiceAidanceOrderAidancePerson", methods=["POST"])
@jwt_required
def choiceAidanceOrderAidancePerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not (id):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(Aidance, "id", id)
    flow_setp = table.flow_step + 2
    flowId = table.flow_id
    tableINfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.sort == flow_setp).first()
    persons = tableINfo.persons
    personName = []
    try:
        for person in persons.split("/"):
            userInfo = User.query.filter(User.admin_name == person).first()
            if userInfo:
                infoDict = {
                    "adminName": userInfo.admin_name,
                    "adminRealName": userInfo.admin_real_name,
                    "adminTelephone": userInfo.admin_telephone,
                    "adminEmail": userInfo.admin_email,
                }
                personName.append(infoDict)
    except:
        pass
    resultDict = returnMsg(personName)
    resultDict["total"] = len(resultDict)
    return jsonify(resultDict)


# 咨询师
# 选择 - 角色人员 下一级 aidanceId
@app.route("/choicePerson", methods=["POST"])
@jwt_required
def choicePerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id")
    if not (id):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(Aidance, "id", id)
    flow_setp = table.flow_step + 2
    flowId = table.flow_id
    tableINfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.sort == flow_setp).first()
    persons = tableINfo.persons
    personName = []
    try:
        for person in persons.split("/"):
            userInfo = User.query.filter(User.admin_name == person).first()
            if userInfo:
                infoDict = {
                    "adminName": userInfo.admin_name,
                    "adminRealName": userInfo.admin_real_name,
                    "adminTelephone": userInfo.admin_telephone,
                    "adminEmail": userInfo.admin_email,
                }
                personName.append(infoDict)
    except:
        pass
    resultDict = returnMsg(personName)
    resultDict["total"] = len(resultDict)
    return jsonify(resultDict)


# 选择 - 角色人员 同级 aidanceId
@app.route("/choicePersonCounselor", methods=["POST"])
@jwt_required
def choicePersonCounselor():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id")
    if not (id):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(Aidance, "id", id)
    flow_setp = table.flow_step + 1
    flowId = table.flow_id
    tableINfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.sort == flow_setp).first()
    persons = tableINfo.persons
    personName = []
    try:
        for person in persons.split("/"):
            userInfo = User.query.filter(User.admin_name == person).first()
            if userInfo:
                infoDict = {
                    "adminName": userInfo.admin_name,
                    "adminRealName": userInfo.admin_real_name,
                    "adminTelephone": userInfo.admin_telephone,
                    "adminEmail": userInfo.admin_email,
                }
                personName.append(infoDict)
    except:
        pass
    resultDict = returnMsg(personName)
    resultDict["total"] = len(resultDict)
    return jsonify(resultDict)


viewRoleUserChangeDic = {
    "id": "id",
    "adminId": "admin_id",
    "adminName": "admin_name",
    "adminToken": "admin_token",
    "adminRefreshToken": "admin_refresh_token",
    "adminSalt": "admin_salt",
    "adminPassword": "admin_password",
    "adminDesc": "admin_desc",
    "adminRealName": "admin_real_name",
    "adminTelephone": "admin_telephone",
    "adminEmail": "admin_email",
    "adminAddTime": "admin_add_time",
    "isLock": "is_lock",
    "ozId": "oz_id",
    "roleId": "role_id",
    "rolePid": "role_pid",
    "roleName": "role_name",
    "roleDesc": "role_desc",
    "isSys": "is_sys",
}
