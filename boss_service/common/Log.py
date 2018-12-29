# coding:utf-8
from flask import request, json, jsonify
from flask_jwt_extended import get_jwt_identity, current_user
from config import logger
from common.ReturnMessage import returnErrorMsg,errorCode
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.OperationOfDB import insertToSQL
from functools import wraps
from models.Boss.UserLog import UserLog


# 查询 日志
def queryLog(tableName):
    def _queryLog(fn):
        @wraps(fn)
        def _warp():
            resultDict = fn()
            if resultDict.status_code == 200:
                try:
                    jsonData = request.get_data()
                    dataDict = json.loads(jsonData)
                except ValueError:
                    dataDict = {}
                adminId = get_jwt_identity()
                try:
                    userIp = request.remote_addr
                    timeNow = getTimeStrfTimeStampNow()
                    adminTable = current_user
                    log_action = "query data " + tableName
                    log_remark = str(dataDict)
                    log_group = 0
                    addResualt = True
                    logger.info("adminId:{},adminName:{},logGroup:{},userIp:{},logAction:{},logRemark:{}".format( adminId, adminTable.admin_name, log_group, userIp, log_action, log_remark))
                    # if adminTable:
                    #     columnsStr = (
                    #         adminId, adminTable.admin_name, log_group, userIp, log_action, log_remark, timeNow)
                    # else:
                    #     resultDict = returnErrorMsg("insert log fail ")
                    #     return jsonify(resultDict)
                    # addResualt = insertToSQL(UserLog, *columnsStr)
                    if addResualt:
                        return resultDict
                    else:
                        resultDict = returnErrorMsg(errorCode["system_error"])
                        return jsonify(resultDict)
                except:
                    resultDict = returnErrorMsg(errorCode["system_error"])
                    return jsonify(resultDict)
            else:
                return resultDict

        return _warp

    return _queryLog


# 添加 日志
def addLog(tableName):
    def _addLog(fn):
        @wraps(fn)
        def _warp():
            resultDict = fn()
            if resultDict.status_code == 200:
                jsonData = request.get_data()
                dataDict = json.loads(jsonData)
                adminId = get_jwt_identity()
                try:
                    userIp = request.remote_addr
                    timeNow = getTimeStrfTimeStampNow()
                    adminTable = current_user
                    log_action = "add data " + tableName
                    log_remark = str(dataDict)
                    log_group = 0
                    addResualt = True
                    logger.info("adminId:{},adminName:{},logGroup:{},userIp:{},logAction:{},logRemark:{}".format( adminId, adminTable.admin_name, log_group, userIp, log_action, log_remark))
                    # if adminTable:
                    #     columnsStr = (
                    #         adminId, adminTable.admin_name, log_group, userIp, log_action, log_remark, timeNow)
                    # else:
                    #     resultDict = returnErrorMsg("insert log fail ")
                    #     return jsonify(resultDict)
                    # addResualt = insertToSQL(UserLog, *columnsStr)
                    if addResualt:
                        return resultDict
                    else:
                        resultDict = returnErrorMsg(errorCode["system_error"])
                        return jsonify(resultDict)
                except:
                    resultDict = returnErrorMsg(errorCode["system_error"])
                    return jsonify(resultDict)
            else:
                return resultDict

        return _warp

    return _addLog


# 删除 日志
def deleteLog(tableName):
    def _deleteLog(fn):
        @wraps(fn)
        def _warp():
            resultDict = fn()
            if resultDict.status_code == 200:
                jsonData = request.get_data()
                dataDict = json.loads(jsonData)
                adminId = get_jwt_identity()
                try:
                    userIp = request.remote_addr
                    timeNow = getTimeStrfTimeStampNow()
                    adminTable = current_user
                    log_action = "delete data " + tableName
                    log_remark = str(dataDict)
                    log_group = 0
                    addResualt = True
                    logger.info("adminId:{},adminName:{},logGroup:{},userIp:{},logAction:{},logRemark:{}".format( adminId, adminTable.admin_name, log_group, userIp, log_action, log_remark))
                    # if adminTable:
                    #     columnsStr = (
                    #         adminId, adminTable.admin_name, log_group, userIp, log_action, log_remark, timeNow)
                    # else:
                    #     resultDict = returnErrorMsg("insert log fail ")
                    #     return jsonify(resultDict)
                    # addResualt = insertToSQL(UserLog, *columnsStr)
                    if addResualt:
                        return resultDict
                    else:
                        resultDict = returnErrorMsg(errorCode["system_error"])
                        return jsonify(resultDict)
                except:
                    resultDict = returnErrorMsg(errorCode["system_error"])
                    return jsonify(resultDict)
            else:
                return resultDict

        return _warp

    return _deleteLog


# 修改 日志
def updateLog(tableName):
    def _updateLog(fn):
        @wraps(fn)
        def _warp():
            resultDict = fn()
            if resultDict.status_code == 200:
                jsonData = request.get_data()
                dataDict = json.loads(jsonData)
                adminId = get_jwt_identity()
                try:
                    userIp = request.remote_addr
                    timeNow = getTimeStrfTimeStampNow()
                    adminTable = current_user
                    log_action = "update data " + tableName
                    log_remark = str(dataDict)
                    log_group = 0
                    addResualt = True
                    logger.info("adminId:{},adminName:{},logGroup:{},userIp:{},logAction:{},logRemark:{}".format( adminId, adminTable.admin_name, log_group, userIp, log_action, log_remark))
                    # if adminTable:
                    #     columnsStr = (
                    #         adminId, adminTable.admin_name, log_group, userIp, log_action, log_remark, timeNow)
                    # else:
                    #     resultDict = returnErrorMsg("insert log fail ")
                    #     return jsonify(resultDict)
                    # addResualt = insertToSQL(UserLog, *columnsStr)
                    if addResualt:
                        return resultDict
                    else:
                        resultDict = returnErrorMsg(errorCode["system_error"])
                        return jsonify(resultDict)
                except:
                    resultDict = returnErrorMsg(errorCode["system_error"])
                    return jsonify(resultDict)
            else:
                return resultDict

        return _warp

    return _updateLog
