# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.MenuGrading import set_menus
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByColumn
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Boss.Menu import Menu, tableChangeDic as MenuChangeDict
from models.Boss.Role import Role
from models.Boss.RoleMenu import RoleMenu, tableChangeDic
from models.Boss.UserRole import tableChangeDic as UserRoleChangeDic
from version.v3.bossConfig import app


@app.route("/findRoleMenuByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_role_menu')
def findRoleMenuByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    intColumnClinetNameList = ("Id", "menuId", "menuParentId", "menuSort", "roleId", "rolePid")
    className = "view_role_menu"
    roleMenuList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, className)
    if roleMenuList:
        InfoList = []
        repeatList = []
        for tableData in roleMenuList:
            menuId = tableData[1]
            if menuId in repeatList:
                continue
            repeatList.append(menuId)
            infoDict = {
                "Id": tableData[0],
                'menuId': menuId,
                'menuKey': tableData[2],
                "menuParentId": tableData[3],
                'menuType': tableData[4],
                'menuTitle': tableData[5],
                "menuIcoUrl": tableData[6],
                'menuLinkUrl': tableData[7],
                'menuSort': tableData[8],
                "menuRemark": tableData[9],
                'roleId': tableData[10],
                'rolePid': tableData[11],
                "roleName": tableData[12],
                'roleDesc': tableData[13]
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# # 获取 列表
# @app.route("/findRoleMenuByCondition", methods=["POST"])
# @jwt_required
# @queryLog('boss_role_menu')
# def findRoleMenuBycondition():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     if dataDict.get('condition', None) == None:
#         resultDict = returnErrorMsg(errorCode["param_error"])
#         return jsonify(resultDict)
#     tablename = RoleMenu.__tablename__
#     intColumnClinetNameList = [u'id', u'roleId', u'menuId']
#     tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
#     if tableList:
#         InfoList = []
#         for tableData in tableList:
#             infoDict = {"id": tableData[0],
#                         "roleId": tableData[1],
#                         "menuId": tableData[2], }
#             infoDict = dictRemoveNone(infoDict)
#             InfoList.append(infoDict)
#         resultDict = returnMsg(InfoList)
#         resultDict["total"] = count
#     else:
#         resultDict = returnErrorMsg()
#     return jsonify(resultDict)


# 获取详情 
@app.route("/getRoleMenuDetail", methods=["POST"])
@jwt_required
@queryLog('boss_role_menu')
def getRoleMenuDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(RoleMenu, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "roleId": table.role_id,
                "menuId": table.menu_id, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteRoleMenu", methods=["POST"])
@jwt_required
@deleteLog('boss_role_menu')
def deleteRoleMenu():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(RoleMenu, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addRoleMenu", methods=["POST"])
@jwt_required
@addLog('boss_role_menu')
def addRoleMenu():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("roleId", None), dataDict.get("menuId", None))
    table = insertToSQL(RoleMenu, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataRoleMenu", methods=["POST"])
@jwt_required
@updateLog('boss_role_menu')
def updataRoleMenu():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'roleId', u'menuId']
    table = updataById(RoleMenu, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)


@app.route("/findUserMenuByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_role_menu")
def findUserMenuByCondition():
    adminId = get_jwt_identity()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    intColumnClinetNameList = ("id", "menuId", "menuParentId", "menuSort", "roleId", "rolePid", "userId")
    className = "view_user_menu"
    adminCondition = {"field": "userId", "op": "equal", "value": adminId}
    dataDict["condition"].append(adminCondition)
    otherChangeDict = {"userId": "user_id"}
    newChangeDict = dict(dict(dict(tableChangeDic, **MenuChangeDict), **UserRoleChangeDic), **otherChangeDict)
    roleMenuList, count = conditionDataListFind(dataDict, newChangeDict, intColumnClinetNameList, className)
    if roleMenuList:
        InfoList = []
        repeatList = []
        for tableData in roleMenuList:
            menuId = tableData[1]
            if menuId in repeatList:
                continue
            repeatList.append(menuId)
            infoDict = {
                "id": tableData[0],
                'menuId': menuId,
                'menuKey': tableData[2],
                "menuParentId": tableData[3],
                'menuType': tableData[4],
                'menuTitle': tableData[5],
                "menuIcoUrl": tableData[6],
                'menuLinkUrl': tableData[7],
                'menuSort': tableData[8],
                "menuRemark": tableData[9],
                'roleId': tableData[10],
                'rolePid': tableData[11],
                "roleName": tableData[12],
                'roleDesc': tableData[13]
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 条件查询
@app.route("/findUserMenuByConditions", methods=["POST"])
@jwt_required
@queryLog("boss_role_menu")
def findUserMenuByConditions():
    adminId = get_jwt_identity()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("id", "menuId", "menuParentId", "menuSort", "roleId", "rolePid", "userId")
    className = "view_user_menu"
    adminCondition = {"field": "userId", "op": "equal", "value": adminId}
    dataDict["condition"].append(adminCondition)
    otherChangeDict = {"userId": "user_id"}
    newChangeDict = dict(dict(dict(tableChangeDic, **MenuChangeDict), **UserRoleChangeDic), **otherChangeDict)
    roleMenuList, count = conditionDataListFind(dataDict, newChangeDict, intColumnClinetNameList, className)
    if roleMenuList:
        allList = []
        repeatList = []
        for table in roleMenuList:
            menuId = table[1]
            if menuId in repeatList:
                continue
            repeatList.append(menuId)
            allList.append(table)
        allLists = set_menus(0, allList)
        infoList = []
        if not allLists:
            resultDict = returnMsg({})
            return jsonify(resultDict)
        for info in allLists:
            print info.text
            oneInfo = info.get()
            infoList.append(oneInfo)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 保存信息
@app.route("/preserveRoleMenu", methods=["POST"])
@jwt_required
@updateLog("boss_role_menu")
def preserveRoleMenu():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = []
    """{roleId: 4, menuId: [249, 250, 251, 43]}
menuId: [249, 250, 251, 43]
[13, 46, 69, 74, 73, 86, 90, 43]
roleId: 4"""
    menuIdList = dataDict.get("menuId", [])
    roleId = dataDict.get("roleId", None)
    if roleId == None or len(menuIdList) == 0:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    roleTable = findById(Role, "role_id", roleId)
    if roleTable:
        idList.append(roleId)
        resualtList = []
        resualtDictInfo = deleteByColumn(RoleMenu, idList, "role_id")
        for menuId in menuIdList:
            menuTable = findById(Menu, "menu_id", menuId)
            if menuTable:
                columnsStr = (roleId, menuId)
                roleMenuTable = insertToSQL(RoleMenu, *columnsStr)
                if roleMenuTable:
                    # resultDict = tableDictSort(roleMenuTable)
                    resultDict = returnMsg({})
                    resualtList.append(resultDict)
        resualtInfo = returnMsg(resualtList)
    else:
        resualtInfo = returnErrorMsg(errorCode["param_error"])
    return jsonify(resualtInfo)
