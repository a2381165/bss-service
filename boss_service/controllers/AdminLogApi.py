# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required

from common.Log import queryLog, deleteLog
from common.OperationOfDB import deleteById, findById, conditionDataListFind
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Boss.UserLog import UserLog as AdminLog, tableChangeDic
from version.v3.bossConfig import app


# 删除管理员操作日志
@app.route("/deleteAdminLog", methods=["POST"])
@jwt_required
@deleteLog("boss_user_log")
def deleteAdminLog():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    adminId = dataDict.get("adminId", None)
    if adminId != None:
        otherCondition = " and user_id = %s" % adminId
    else:
        otherCondition = None
    resultDict = deleteById(AdminLog, idList, "id", otherCondition)
    return jsonify(resultDict)


# 通过条件 筛选管理员操作日志
@app.route("/findAdminLogByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_user_log")
def findAdminLogByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("userId")
    tableName = AdminLog.__tablename__
    orderByStr = " order by log_add_time desc "
    adminsList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName,orderByStr=orderByStr)
    if adminsList:
        adminInfoList = []
        for adminData in adminsList:
            admin = {
                "id": adminData[0],
                'userId': adminData[1],
                "adminName": adminData[2],
                "logIp": adminData[4],
                'logAction': adminData[5],
                'logRemark': adminData[6],
                'logAddTime': str(adminData[7])
            }
            adminInfoList.append(admin)
        resultDict = returnMsg(adminInfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 查看管理员日志详情
@app.route("/findAdminLogById", methods=["POST"])
@jwt_required
@queryLog("boss_user_log")
def findAdminLogById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('Id', None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    else:
        table = findById(AdminLog, "Id", id)
        if table:
            dictInfo = tableDictSort(table)
            resultDict = returnMsg(dictInfo)
        elif table == 0:
            dictInfo = {}
            resultDict = returnMsg(dictInfo)
        else:
            resultDict = returnErrorMsg()
        return jsonify(resultDict)


def tableDictSort(table):
    tableDict = {
        "Id": table.id,
        'adminId': table.admin_id,
        'adminName': table.admin_name,
        'logIp': table.log_ip,
        'logaction': table.log_action,
        'logRemark': table.log_remark,
        'logAddTime': str(table.log_add_time)
    }
    return tableDict
