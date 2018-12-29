# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, current_user

from common.AreaCodeGrading import set_menus
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByColumn, \
    executeSql
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Boss.Area import Area
from models.Boss.AreaSet import AreaSet as DataAreaSet, tableChangeDic
from models.Boss.Organization import Organization
from models.Boss.Role import Role
from models.Boss.User import User
from models.Boss.UserRole import UserRole
from models.Data.Department import Department
from version.v3.bossConfig import app


# 获取 列表 # 技术部 区域人员关联
@app.route("/findDataAreaSetByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_area_set')
def findDataAreaSetBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = DataAreaSet.__tablename__
    intColumnClinetNameList = [u'id', u'dataAreaId', u'userId', "ozId"]
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "userId": tableData[1],
                        "areaCode": tableData[2]}
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getDataAreaSetDetail", methods=["POST"])
@jwt_required
@queryLog('boss_area_set')
def getDataAreaSetDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(DataAreaSet, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "dataAreaId": table.data_area_id,
                "userId": table.user_id, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteDataAreaSet", methods=["POST"])
@jwt_required
@deleteLog('boss_area_set')
def deleteDataAreaSet():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(DataAreaSet, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addDataAreaSet", methods=["POST"])
@jwt_required
@addLog('boss_area_set')
def addDataAreaSet():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    dataAreaId = dataDict.get("dataAreaId", None)
    userId = dataDict.get("userId", None)
    if not (dataAreaId and userId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    columsStr = (dataAreaId, userId)
    table = insertToSQL(DataAreaSet, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataDataAreaSet", methods=["POST"])
@jwt_required
@updateLog('boss_area_set')
def updataDataAreaSet():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'dataAreaId', u'userId']
    table = updataById(DataAreaSet, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)


# 删除这里 因为 只有一张表 所以 一个人员 只能别分配到一个区域  如果分配过多 会出现误删
# 保存信息
@app.route("/preserveUserArea", methods=["POST"])
@jwt_required
@updateLog("boss_area_set")
def preserveUserArea():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = []
    areaIds = dataDict.get("areaIds", [])
    userId = dataDict.get("userId", None)
    ozId = dataDict.get("ozId", None)
    # roleId = dataDict.get("roleId", 3)
    if not (userId and ozId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminTable = current_user
    adminName = adminTable.admin_name
    roleTable = findById(User, "admin_id", userId)
    if roleTable:
        idList.append(userId)
        otherCondition = " and oz_id={}".format(ozId)
        resualtDictInfo = deleteByColumn(DataAreaSet, idList, "user_id", otherCondition)
        resualtList = []
        if areaIds:
            # 如果角色是副部长  可以为他补全省份
            # if roleId == 3:
            #     infoList = []
            #     for areaCode in areaIds:
            #         infoList.append('{}0000'.format(areaCode[:2]))
            #     areaIds = list(set(areaIds + infoList))
            for areaCode in areaIds:
                DataAreaSet.query.filter(DataAreaSet.user_id == userId).first()
                menuTable = findById(Area, "area_code", areaCode)
                if menuTable:
                    columnsStr = (userId, areaCode, adminName, ozId)
                    roleMenuTable = insertToSQL(DataAreaSet, *columnsStr)
                    if roleMenuTable:
                        resultDict = returnMsg({})
                        resualtList.append(resultDict)
        resualtInfo = returnMsg(resualtList)
    else:
        resualtInfo = returnErrorMsg("the roleId not exit!")
    return jsonify(resualtInfo)


# 普通 獲取 角色 人员列表 # 咨询部 默认
@app.route("/getUserDeptList", methods=["POST"])
@jwt_required
def getUserDeptList():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", 3)
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # adminId = get_jwt_identity()
    # UserRole.query.filter(UserRole.user_id==adminId).first()
    roleList = Role.query.filter(Role.role_pid == roleId).all()
    roleIds = [role.role_id for role in roleList]
    userRoleList = UserRole.query.filter(UserRole.role_id.in_(roleIds)).all()
    # ozId = dataDict.get("ozId", 7)
    # userList = User.query.filter(User.oz_id==ozId).all()
    # UserRole.query.filter(UserRole.)
    infoList = []
    for userrole in userRoleList:
        adminName = ""
        adminId = ""
        adminRealName = ""
        adminTelephone = ""
        table = findById(User, "admin_id", userrole.user_id)
        if userrole:
            adminName = table.admin_name
            adminRealName = table.admin_real_name
            adminTelephone = table.admin_telephone
            adminId = table.admin_id
        infoDict = {
            "adminName": adminName,
            "userId": adminId,
            "adminRealName": adminRealName,
            "adminTelephone": adminTelephone,
        }
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 菜单类型 人员列表
@app.route("/findUserDeptByConditions", methods=["POST"])
# @jwt_required
# @queryLog("base_user")
def findUserDeptByConditions():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    else:
        intColumnClinetNameList = ("adminId", "isLock", 'ozId', 'ozPid', 'ozSort', 'isLock')
        tableName = User.__tablename__
        userChangeDic = {}
        newChangeDic = dict(tableChangeDic, **userChangeDic)
        ozList = Organization.query.filter(Organization.id != 3).all()
        adminsList, count = conditionDataListFind(dataDict, newChangeDic, intColumnClinetNameList, tableName)
        if adminsList:
            talbeList = []
            infoLists = []
            for talbe in adminsList:
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
                    if table.oz_id == ozInfo.id:
                        infoList.append({"id": table.admin_id,
                                         "text": table.admin_real_name, "adminName": table.admin_name})
                if infoList == []:
                    continue
                allList["children"] = infoList
                infoLists.append(allList)
            ids = [ozs["ids"] for ozs in infoLists]
            for oz in infoLists:
                for id in ids:
                    if oz["pid"] == id:
                        infoLists[ids.index(id)]["children"].append(oz)
                        infoLists.remove(oz)
            resultDict = returnMsg(infoLists)
            resultDict["total"] = count
        else:
            resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 咨询部 政策分析 保存角色 和区域人员 保存信息 # 已废弃
@app.route("/preserveUserDeptArea", methods=["POST"])
@jwt_required
@updateLog("boss_role")
def preserveUserDeptArea():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    userIdList = dataDict.get("userId", [])
    areaCode = dataDict.get("areaCode", None)
    if not (areaCode):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    resualtList = []
    # if not userIdList:
    adminTable = current_user
    adminName = adminTable.admin_name
    otherCondition = " and oz_id={}".format(2)  # 2 咨询部
    resualtDictInfo = dbOperation.deleteByColumn(DataAreaSet, [areaCode], "area_code", otherCondition=otherCondition)
    if not resualtDictInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for userId in userIdList:
        # otherCondition = " and user_id={}".format(userId)
        # resualtDictInfo = dbOperation.deleteByColumn(DataAreaSet, areaCode, "area_code", otherCondition)
        # if not resualtDictInfo:
        #     dbOperation.commitRollback()
        #     resultDict = returnErrorMsg(errorCode["param_error"])
        #     return jsonify(resultDict)
        adminTable = findById(User, "admin_id", userId)
        if adminTable:
            columnsStr = (userId, areaCode, adminName, 2)
            adminRoleTable = dbOperation.insertToSQL(DataAreaSet, *columnsStr)
            if adminRoleTable:
                resultDict = returnMsg({})
                resualtList.append(resultDict)
            else:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["system_error"])
                return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resualtInfo = returnMsg(resualtList)
    else:
        dbOperation.commitRollback()
        resualtInfo = returnErrorMsg("inset fail")
    # else:
    #     resualtInfo = returnErrorMsg("the roleId not exit!")
    return jsonify(resualtInfo)


# 咨询部 政策分析 关系表
@app.route("/getUserDeptContactList", methods=["POST"])
@jwt_required
def getUserDeptContactList():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    areaCode = dataDict.get("areaCode", None)
    roleId = dataDict.get("roleId", 2)
    if not areaCode:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    sqlStr = "select t1.user_id,t1.area_code from boss_area_set as t1 join boss_user_role as t2 join boss_role as t3 on t1.area_code='{areaCode}' and t1.user_id=t2.user_id and t3.role_pid={roleId}".format(
        areaCode=areaCode, roleId=roleId)
    # sqlStr = "select t1.user_id,t1.area_code from boss_area_set as t1 join data_organization as t2 on t1.area_code='{areaCode}' and t1.oz_id=t2.id and t2.role".format(
    #     areaCode=areaCode)
    resultList = executeSql(sqlStr)
    infoList = []
    if resultList:
        for result in resultList:
            infoDict = {
                "userId": result[0],
                "areaCode": result[1],
            }
            infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 获取区域 有部门的区域
@app.route("/getDeptAreaList", methods=["POST"])
@jwt_required
def getDeptAreaList():
    sqlStr = """SELECT distinct t2.area_code, t2.area_name,t2.p_code from data_area as t JOIN base_area as t2 ON t.area_code=t2.area_code and t.area_code like '%00' and t.area_status = 1 """
    resultList = executeSql(sqlStr)
    infoList = []
    if resultList:
        tableList = []
        for result in resultList:
            tableList.append(result)
        allLists = set_menus("00", tableList)
        infoList = []
        if not allLists:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        for info in allLists:
            oneInfo = info.get()
            infoList.append(oneInfo)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 无用
# 获取区域 有部门的区域
@app.route("/getDeptAreaLists", methods=["POST"])
@jwt_required
def getDeptAreaLists():
    sqlStr = """SELECT distinct t2.area_code, t2.area_name from data_area as t JOIN base_area as t2 ON t.area_code=t2.area_code and t.area_code like '%00' """
    resultList = executeSql(sqlStr)
    infoLists = []
    if resultList:
        for result in resultList:
            allList = {}
            allList["id"] = result.area_code
            allList["text"] = result.area_name
            if result.area_code[2:] == "0000":
                deptList = Department.query.filter(Department.area_code == result.area_code).all()
            elif result.area_code[2:4] != "00" and result.area_code[4:6] == "00":
                deptList = Department.query.filter(Department.area_code.like("{}%".format(result.area_code[:4]))).all()
            else:
                deptList = []
            infoList = []
            for dept in deptList:
                deptDict = {}
                deptDict["deptName"] = dept.dept_name
                deptDict["id"] = dept.dept_id
                infoList.append(deptDict)
            allList["children"] = infoList
            infoLists.append(allList)
    resultDict = returnMsg(infoLists)
    return jsonify(resultDict)
