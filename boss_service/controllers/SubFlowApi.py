# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Data.SubFlow import SubFlow, SubFlowChangeDic as tableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog
from models.Boss.Role import Role
from models.Boss.User import User
from models.Boss.UserRole import UserRole


# 获取 列表
@app.route("/findSubFlowByCondition", methods=["POST"])
@jwt_required
@queryLog('data_sub_flow')
def findSubFlowBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SubFlow.__tablename__
    intColumnClinetNameList = [u'id', u'flowId', u'roleId', u'sort']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            roleId = tableData[2]
            roleInfo = findById(Role, "role_id", roleId)
            if roleInfo:
                roleName = roleInfo.role_name
            else:
                roleName = ""
            persons = tableData[4]
            personName = []
            try:
                for person in persons.split("/"):
                    userInfo = User.query.filter(User.admin_name == person).first()
                    if userInfo:
                        person_name = userInfo.admin_real_name
                    else:
                        person_name = ""
                    personName.append(person_name)
            except:
                personName = []
            if len(personName) == 1:
                personNames = "{}".format(personName[0])
            elif len(personName) > 1:
                personNames = "/".join(personName)[:-1]
            else:
                personNames = ""

            infoDict = {"id": tableData[0],
                        "flowId": tableData[1],
                        "roleId": tableData[2],
                        "sort": tableData[3],
                        "persons": tableData[4],
                        "remark": tableData[5],
                        "createTime": tableData[6],
                        "roleName": roleName,
                        "personNames": personNames,
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getSubFlowDetail", methods=["POST"])
@jwt_required
@queryLog('data_sub_flow')
def getSubFlowDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(SubFlow, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "flowId": table.flow_id,
                "roleId": table.role_id,
                "sort": table.sort,
                "persons": table.persons,
                "remark": table.remark,
                "createTime": table.create_time, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteSubFlow", methods=["POST"])
@jwt_required
@deleteLog('data_sub_flow')
def deleteSubFlow():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("ids", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(SubFlow, ids, "id")
    if len(ids) == count:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addSubFlow", methods=["POST"])
@jwt_required
@addLog('data_sub_flow')
def addSubFlow():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    now = getTimeStrfTimeStampNow()
    columsStr = (dataDict.get("flowId", None), dataDict.get("roleId", None), dataDict.get("sort", None),
                 dataDict.get("persons", None), dataDict.get("remark", None), now)
    table = insertToSQL(SubFlow, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataSubFlow", methods=["POST"])
@jwt_required
@updateLog('data_sub_flow')
def updataSubFlow():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'flowId', u'roleId', u'sort']
    table = updataById(SubFlow, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 获取本角色
@app.route("/getSubRole", methods=["POST"])
def getSubRole():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", "")
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    userList = UserRole.query.filter(UserRole.role_id == roleId).all()
    userIds = [user.user_id for user in userList]
    userInfoList = User.query.filter(User.admin_id.in_(userIds)).all()
    infoList = []
    for userInfo in userInfoList:
        infoDict = {
            "adminRealName": userInfo.admin_real_name,
            "adminName": userInfo.admin_name,
            "adminTelephone": userInfo.admin_telephone,
            "adminEmail": userInfo.admin_email,
        }
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)
