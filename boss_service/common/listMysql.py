#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/14 0014 11:41
# @Site    : 
# @File    : listMysql.py
# @Software: PyCharm
from models.Data.SubFlow import SubFlow
from models.Boss.Role import Role
from common.OperationOfDB import findById


# 获取角色 人名  通用
def getRolePerson(aidanceInfo, flowId, dbOperation,isNum=1):
    nextStep = aidanceInfo.flow_step
    # if nextStep == 1:
    #     nextStep += 2
    # else:
    nextStep += isNum
    subInfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.sort == nextStep).first()
    # 如果有下一步
    if not subInfo:
        dbOperation.commitRollback()
        return None
    roleId = subInfo.role_id
    # 角色管理人
    try:
        checkPerson = subInfo.persons.split("/")[0]
    except:
        roleInfo = findById(Role, "role_id", roleId)
        if roleInfo:
            checkPerson = roleInfo.manager_name
        else:
            checkPerson = None

    return checkPerson


# 获取角色 人名  通用
def getRolePersonFlow(flowId, dbOperation):
    nextStep = 2
    subInfo = SubFlow.query.filter(SubFlow.flow_id == flowId, SubFlow.sort == nextStep).first()
    # 如果有下一步
    if not subInfo:
        dbOperation.commitRollback()
        return None
    roleId = subInfo.role_id
    # 角色管理人
    try:
        checkPerson = subInfo.persons.split("/")[0]
    except:
        roleInfo = findById(Role, "role_id", roleId)
        if roleInfo:
            checkPerson = roleInfo.manager_name
        else:
            checkPerson = None

    return checkPerson
