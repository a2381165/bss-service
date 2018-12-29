# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required

from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, \
    sqlFunctionCallBoss
from common.ReturnMessage import returnMsg, errorCode, returnErrorMsg
from models.Boss.Organization import Organization, tableChangeDic
from models.Boss.Role import Role
from models.Boss.User import User
from version.v3.bossConfig import app


# 获取 列表
@app.route("/findOrganizationByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_organization')
def findOrganizationBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = Organization.__tablename__
    # multiSort: {field: ["ozSort"], sort: ["asc"]}
    intColumnClinetNameList = [u'id', u'ozPid', u'ozSort', u'isLock']
    orderByStr = " order by oz_sort asc "
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "ozName": tableData[1],
                        "ozPid": tableData[2],
                        "ozSort": tableData[3],
                        "ozCode": tableData[4],
                        "isLock": tableData[5],
                        "remark": tableData[6], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getOrganizationDetail", methods=["POST"])
@jwt_required
@queryLog('boss_organization')
def getOrganizationDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(Organization, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "ozName": table.oz_name,
                "ozPid": table.oz_pid,
                "ozSort": table.oz_sort,
                "ozCode": table.oz_code,
                "isLock": table.is_lock,
                "remark": table.remark, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteOrganization", methods=["POST"])
@jwt_required
@deleteLog('boss_organization')
def deleteOrganization():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in ids:
        table = Organization.query.filter(Organization.oz_pid == id).all()
        if table:
            resultDict = returnErrorMsg(errorCode["oz_oz"])
            return jsonify(resultDict)
        usertable = User.query.filter(User.oz_id == id).first()
        if usertable:
            resultDict = returnErrorMsg(errorCode["oz_people"])
            return jsonify(resultDict)

    table = deleteById(Organization, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addOrganization", methods=["POST"])
@jwt_required
@addLog('boss_organization')
def addOrganization():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("ozName", None), dataDict.get("ozPid", None), dataDict.get("ozSort", None),
                 dataDict.get("ozCode", None), dataDict.get("isLock", None), dataDict.get("remark", None))
    table = insertToSQL(Organization, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataOrganization", methods=["POST"])
@jwt_required
@updateLog('boss_organization')
def updataOrganization():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'ozPid', u'ozSort', u'isLock']
    table = updataById(Organization, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)


@app.route("/findUserOzByConditions", methods=["POST"])
@jwt_required
@queryLog("base_user")
def findUserOzByConditions():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    else:
        role = Role.query.filter(Role.role_id == roleId).first()
        if not role:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        ozId = role.oz_id
        intColumnClinetNameList = ("adminId", "isLock", 'ozId', 'ozPid', 'ozSort', 'isLock')
        # tableName = User.__tablename__
        resultList = sqlFunctionCallBoss("call getUserRoleOz({})".format(roleId))

        # tableName = "view_user_role_oz"
        # newChangeDic = dict(tableChangeDic, **userChangeDic)
        # # ozList = Organization.query.filter(Organization.id != 1).all()
        ozList = Organization.query.filter(Organization.id == ozId).all()
        # adminsList, count = conditionDataListFind(dataDict, newChangeDic, intColumnClinetNameList, tableName)
        if resultList:
            talbeList = []
            infoLists = []
            for talbe in resultList:
                talbeList.append(talbe)
            for ozInfo in ozList:
                allList = {}
                allList["id"] = "b" + str(ozInfo.id)
                allList["isMenu"] = True
                allList["ids"] = ozInfo.id
                allList["pid"] = ozInfo.oz_pid
                allList["text"] = ozInfo.oz_name
                infoList = []
                for table in talbeList:
                    # if table.role_pid == roleId:
                    infoList.append({"id": table.admin_id,
                                     "text": table.admin_real_name, "adminName": table.admin_name,
                                     "ozId":ozInfo.id})
                if infoList == []:
                    continue
                allList["children"] = infoList
                infoLists.append(allList)
            # ids = [ozs["ids"] for ozs in infoLists]
            # for oz in infoLists:
            #     for id in ids:
            #         if oz["pid"] == id:
            #             infoLists[ids.index(id)]["children"].append(oz)
            #             infoLists.remove(oz)
            resultDict = returnMsg(infoLists)
            resultDict["total"] = len(infoLists)
        else:
            resultDict = returnMsg({})
            # resultDict = returnErrorMsg()
        return jsonify(resultDict)
