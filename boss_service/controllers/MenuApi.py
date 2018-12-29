# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required

from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Boss.Menu import Menu, tableChangeDic
from version.v3.bossConfig import app


# 获取 列表 
@app.route("/findMenuByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_menu')
def findMenuBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = Menu.__tablename__
    intColumnClinetNameList = [u'menuId', u'menuParentId', u'menuSort', u'isSys', u'isLock']
    orderByStr = " order by menu_sort asc"
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename,orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"menuId": tableData[0],
                        "menuKey": tableData[1],
                        "menuParentId": tableData[2],
                        "menuType": tableData[3],
                        "menuTitle": tableData[4],
                        "menuIcoUrl": tableData[5],
                        "menuLinkUrl": tableData[6],
                        "menuSort": tableData[7],
                        "menuRemark": tableData[8],
                        "isSys": tableData[9],
                        "isLock": tableData[10], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getMenuDetail", methods=["POST"])
@jwt_required
@queryLog('boss_menu')
def getMenuDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("menuId", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(Menu, "menu_id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"menuId": table.menu_id,
                "menuKey": table.menu_key,
                "menuParentId": table.menu_parent_id,
                "menuType": table.menu_type,
                "menuTitle": table.menu_title,
                "menuIcoUrl": table.menu_ico_url,
                "menuLinkUrl": table.menu_link_url,
                "menuSort": table.menu_sort,
                "menuRemark": table.menu_remark,
                "isSys": table.is_sys,
                "isLock": table.is_lock, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteMenuByIds", methods=["POST"])
@jwt_required
@deleteLog('boss_menu')
def deleteMenuByIds():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in ids:
        table = Menu.query.filter(Menu.menu_parent_id == id).all()
        if table:
            resultDict = returnErrorMsg(errorCode["menu_menu"])
            return jsonify(resultDict)

    table = deleteById(Menu, ids, "menu_id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addMenu", methods=["POST"])
@jwt_required
@addLog('boss_menu')
def addMenu():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("menuKey", None), dataDict.get("menuParentId", None), dataDict.get("menuType", None),
                 dataDict.get("menuTitle", None), dataDict.get("menuIcoUrl", None), dataDict.get("menuLinkUrl", None),
                 dataDict.get("menuSort", None), dataDict.get("menuRemark", None), dataDict.get("isSys", None),
                 dataDict.get("isLock", None))
    table = insertToSQL(Menu, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updateMenuById", methods=["POST"])
@jwt_required
@updateLog('boss_menu')
def updateMenuById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "menu_id"
    intColumnClinetNameList = ("menuId", "menuParentId", "menuSort", "isLock", "isSys")
    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in idList:
        menuUp = updataById(Menu, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if menuUp == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif menuUp == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        else:
            resultDict = returnMsg({})
        infoList.append(resultDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)
