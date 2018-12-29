#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 0018 14:33
# @Site    : 
# @File    : FlowCommon.py
# @Software: PyCharm
from flask_jwt_extended import current_user

from common.DatatimeNow import getTimeStrfTimeStampNow
from common.listMysql import getRolePersonFlow
from models.Data.Aidance import Aidance
from models.Data.AidanceCheck import AidanceCheck
from common.OperationOfDB import findById
from models.Data.SubFlow import SubFlow


# first
def sendUp(table, choicePerson, dbOperation, flowId, taskType, **kwargs):
    now = getTimeStrfTimeStampNow()
    if kwargs:
        isDone = kwargs.get("isDone",1)
    else:
        isDone = 1
    # 创建任务表
    flowId = flowId  # 单项 流程
    executePerson = None
    checkId = 0
    fromId = 0
    serviceId = table.id
    acceptStatus = 0
    setpFlow = 1
    createRealName = current_user.admin_real_name
    createPerson = current_user.admin_name
    createTime = now
    remark = None
    taskType = taskType  # 单项
    try:
        customerName = table.customer_name
    except:
        customerName = kwargs.get("customerName",None)
    createReason = None
    aidanceStr = (customerName, createReason, createRealName, str(createTime), flowId, remark, executePerson,
                  createPerson, None, checkId, fromId, serviceId, setpFlow, acceptStatus, isDone, taskType)
    AidanceTable = dbOperation.insertToSQL(Aidance, *aidanceStr)
    if not AidanceTable:
        return None
    aidanceId = AidanceTable.id
    # 获取上一级管理人
    if choicePerson:
        checkPerson = choicePerson
    else:
        checkPerson = getRolePersonFlow(flowId, dbOperation)
    if checkPerson is None:
        return None
    # 添加 新的审核表 # 跟着步骤查询
    flowStep = 1
    aidanceStr = (aidanceId, now, current_user.admin_name, 1, None, checkPerson, None, flowStep)
    tableCheck = dbOperation.insertToSQL(AidanceCheck, *aidanceStr)
    if not tableCheck:
        return None
    # 更新 task
    AidanceTable.check_id = tableCheck.id
    AidanceTable = dbOperation.addTokenToSql(AidanceTable)
    if not AidanceTable:
        return None
    # 更新明细表
    table.is_done = 1
    table.task_id = AidanceTable.id
    table = dbOperation.addTokenToSql(table)
    if not table:
        return None
    return True


# 退回上报
def returnUp(aidanceTable, table, dbOperation, choicePerson):
    now = getTimeStrfTimeStampNow()
    aidanceId = table.task_id
    # aidanceTable = findById(Aidance, "id", aidanceId)
    flowId = aidanceTable.flow_id
    # 获取上一级管理人
    if choicePerson:
        checkPerson = choicePerson
    else:
        checkPerson = getRolePersonFlow(flowId, dbOperation)
    if checkPerson is None:
        return None
    # 添加 新的审核表 # 跟着步骤查询
    flowStep = 1
    aidanceStr = (aidanceId, now, current_user.admin_name, 1, None, checkPerson, None, flowStep)
    tableCheck = dbOperation.insertToSQL(AidanceCheck, *aidanceStr)
    if not tableCheck:
        return None
    # 更新checkId
    aidanceTable.check_id = tableCheck.id
    aidanceTable = dbOperation.addTokenToSql(aidanceTable)
    if not aidanceTable:
        return None
    return True


# 中间人
def getFlowSort(flowId, roleId, adminName=None):
    if not adminName:
        adminName = current_user.admin_name
    if "(" in str(flowId):
        subInfo = SubFlow.query.filter(SubFlow.flow_id.in_(flowId), SubFlow.role_id == roleId).first()
        if subInfo:
            if adminName in subInfo.persons:
                sort = subInfo.sort - 1
            else:
                return None
        else:
            return None
    else:
        subInfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.role_id == roleId).first()
        if subInfo:
            if adminName in subInfo.persons:
                sort = subInfo.sort - 1
            else:
                return None
        else:
            return None
    return sort


def getFlowUnderSort(flowId, roleId, adminName=None):
    if not adminName:
        adminName = current_user.admin_name
    if "(" in str(flowId):
        subInfo = SubFlow.query.filter(SubFlow.flow_id.in_(flowId), SubFlow.role_id == roleId).first()
        if subInfo:
            if adminName in subInfo.persons:
                sort = subInfo.sort
            else:
                return None
        else:
            return None
    else:
        subInfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.role_id == roleId).first()
        if subInfo:
            if adminName in subInfo.persons:
                sort = subInfo.sort
            else:
                return None
        else:
            return None
    return sort
