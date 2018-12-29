# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required, current_user, get_jwt_identity
from pypinyin import lazy_pinyin, FIRST_LETTER

from common.AreaCodeGrading import set_menus
from common.DatatimeNow import returnEmailCodeTime, getTimeToStrfdate
from common.FormatStr import dictRemoveNone
from common.Log import addLog, queryLog, deleteLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind, executeSql
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from common.UserAreaDept import getAreaSql
from models.Base.Area import Area
from models.Boss.Role import Role
from models.Boss.SpiderScript import SpiderScript
from models.Data.Category import Category
from models.Data.Department import Department
from models.Data.Source import Source, tableChangeDic
from version.v3.bossConfig import app


# 数据源导入接口 放在了CategoryInsertApi 下

# 通过条件查找数据源  获取列表 ok # 获取自己区域数据
@app.route("/findDataSourceByCondition", methods=["POST"])
@jwt_required
@queryLog("data_source")
def findDataSourceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId","")
    adminId = get_jwt_identity()
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition",[])
    areaCode = ""
    for _con in condition:
        if _con["field"] == "areaCode":
            areaCode = _con["value"]
            condition.remove(_con)
    sqlStr = getAreaSql(adminId,roleId,areaCode)
    if not sqlStr:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("sourceId", "levelCode", "checkStatus", "isLock")
    tableName = "view_data_source_area"
    orderByStr = " order by create_time desc "
    dataSourceList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName,
                                                  orderByStr=orderByStr,deptIdConditonStr=sqlStr)
    if dataSourceList:
        InfoList = []
        for tableData in dataSourceList:
            areaCode = tableData[2]
            provinceName, cityName, districtName = getAreaCode(areaCode)
            infoDict = {
                "sourceId": tableData[0],
                "levelCode": tableData[1],
                "areaCode": tableData[2],
                "deptCategory": tableData[3],
                "deptName": tableData[4],
                "deptAddress": tableData[5],
                "deptUrl": tableData[6],
                "desUrl": tableData[7],
                "createTime": getTimeToStrfdate(tableData[8]),
                "createPerson": tableData[9],
                "checkStatus": tableData[10],
                "checkTime": getTimeToStrfdate(tableData[11]),
                "checkPerson": tableData[12],
                "checkRemark": tableData[13],
                "isLock": tableData[14],
                "provinceName": provinceName,
                "cityName": cityName,
                "districtName": districtName
            }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 数据源转化为部门 ok
@app.route("/changeDataSource", methods=["POST"])
@jwt_required
@addLog("data_source")
def changeDataSource():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    checkStatus = dataDict.get("checkStatus", 0)
    if checkStatus != 3:
        resultDict = returnErrorMsg("checkStatus must be 3!")
        return jsonify(resultDict)
    dataDict["isLock"] = 1
    dbOperation = OperationOfDB()
    columnId = Source.source_id
    dataSourceUp = dbOperation.updateThis(Source, columnId, id, dataDict, tableChangeDic)
    if dataSourceUp == None:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg()
    elif dataSourceUp == 0:
        dbOperation.commitRollback()
        InfoDic = {}
        resultDict = returnMsg(InfoDic)
    else:
        infoList = []
        departmentTable, scrapyRuleTable = addDataToDepartment(dataSourceUp, dbOperation)
        if departmentTable == None or scrapyRuleTable == None:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("this data incorrect!")
            return jsonify(resultDict)
        areaCode = dataSourceUp.area_code
        provinceName, cityName, districtName = getAreaCode(areaCode)
        dataSourceDic = {
            "sourceId": dataSourceUp.source_id,
            "levelCode": dataSourceUp.level_code,
            "areaCode": dataSourceUp.area_code,
            "deptCategory": dataSourceUp.dept_category,
            "deptName": dataSourceUp.dept_name,
            "deptAddress": dataSourceUp.dept_address,
            "deptUrl": dataSourceUp.dept_url,
            "createTime": str(dataSourceUp.create_time),
            "createPerson": dataSourceUp.create_person,
            "checkStatus": dataSourceUp.check_status,
            "checkTime": str(dataSourceUp.check_time),
            "checkPerson": dataSourceUp.check_person,
            "checkRemark": dataSourceUp.check_remark,
            "isLock": dataSourceUp.is_lock,
            "desUrl": dataSourceUp.des_url,
            'districtName': districtName,
            'provinceName': provinceName,
            'cityName': cityName
        }
        departmentDict = {
            "deptId": departmentTable.dept_id,
            "deptCode": departmentTable.dept_code,
            'deptPid': departmentTable.dept_pid,
            'deptName': departmentTable.dept_name,
            'deptAddress': departmentTable.dept_address,
            'deptUrl': departmentTable.dept_url,
            'areaCode': departmentTable.area_code,
            "isLock": departmentTable.is_lock,
            "categoryId": departmentTable.category_id,
            "levelCode": departmentTable.level_code,
            "desUrl": departmentTable.des_url,
        }
        scrapyRuleDict = {
            "ruleId": scrapyRuleTable.rule_id,
            'deptId': scrapyRuleTable.dept_id,
            'remark': scrapyRuleTable.remark,
            'isLock': scrapyRuleTable.is_lock,
            "deptNameKey": scrapyRuleTable.dept_name_key,
            "scrapyRule": scrapyRuleTable.scrapy_rule
        }
        infoList.append(dataSourceDic)
        infoList.append(departmentDict)
        infoList.append(scrapyRuleDict)
        resultDict = returnMsg(infoList)
    if dbOperation.commitToSQL():
        return jsonify(resultDict)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("change fail")
        return jsonify(resultDict)


# 数据源审核 ok
@app.route("/updateDataSourceCheckStatus", methods=["POST"])
@jwt_required
@addLog("data_source")
def updateDataSourceCheckStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", None)
    checkStatus = dataDict.get("checkStatus", 0)
    checkTime = dataDict.get("checkTime", None)
    timeNow, expireTime = returnEmailCodeTime()
    if checkTime != None:
        dataDict["checkTime"] = str(timeNow)
    if checkStatus == 3:
        dataDict["isLock"] = 1
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dataDict["checkPerson"] = current_user.admin_name
    infoList = []

    dbOperation = OperationOfDB()
    for id in idList:
        columnId = Source.source_id
        dataSourceUp = dbOperation.updateThis(Source, columnId, id, dataDict, tableChangeDic)
        if dataSourceUp == None:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif dataSourceUp == 0:
            InfoDic = {"error_id": id, }
            infoList.append(InfoDic)
        else:
            if checkStatus == 3:
                departmentTable, scrapyRuleTable = addDataToDepartment(dataSourceUp, dbOperation)
                if departmentTable == None or scrapyRuleTable == None:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("this data incorrect!")
                    return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(infoList)
        return jsonify(resultDict)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("updata fail")
        return jsonify(resultDict)


# 更新数据源 ok
@app.route("/updateDataSource", methods=["POST"])
@jwt_required
@deleteLog("data_source")
def updateDataSource():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("sourceId", None)
    checkStatus = dataDict.get("checkStatus", 0)
    if checkStatus == 3:
        dataDict["isLock"] = 1
    dbOperation = OperationOfDB()
    columnId = Source.source_id
    dataSourceUp = dbOperation.updateThis(Source, columnId, id, dataDict, tableChangeDic)
    if dataSourceUp == None:
        resultDict = returnErrorMsg()
    elif dataSourceUp == 0:
        InfoDic = {}
        resultDict = returnMsg(InfoDic)
    else:
        if checkStatus == 3:
            departmentTable, scrapyRuleTable = addDataToDepartment(dataSourceUp, dbOperation)
            if departmentTable == None or scrapyRuleTable == None:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("this data incorrect!")
                return jsonify(resultDict)
        resultDict = returnMsg({})
    if dbOperation.commitToSQL():
        return jsonify(resultDict)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("updata fail")
        return jsonify(resultDict)


# 删除数据源 ok
@app.route("/deleteDataSource", methods=["POST"])
@jwt_required
@deleteLog("data_source")
def deleteDataSource():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = deleteById(Source, idList, "source_id")
    return jsonify(resultDict)


# 查看数据源信息 ok
@app.route("/findDataSourceById", methods=["POST"])
@jwt_required
@queryLog("data_source")
def findDataSourceById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('sourceId', None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dataSourceTable = findById(Source, "source_id", id)
    if dataSourceTable:
        infoDict = tableDictSort(dataSourceTable)
        resultDict = returnMsg(infoDict)
    elif dataSourceTable == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 添加数据源信息 ok
@app.route("/addDataSource", methods=["POST"])
@jwt_required
@addLog("data_source")
def addDataSource():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    dateTimeNow, expireTime = returnEmailCodeTime()
    columnsStr = (
        dataDict.get("levelCode", None),
        dataDict.get("areaCode", None),
        dataDict.get("deptCategory", None),
        dataDict.get("deptName", None),
        dataDict.get("deptAddress", None),
        dataDict.get("deptUrl", None),
        dataDict.get("desUrl", None),
        str(dateTimeNow),
        dataDict.get("createPerson", None),
        dataDict.get("checkStatus", 0),
        dataDict.get("checkTime", None),
        dataDict.get("checkPerson", None),
        dataDict.get("checkRemark", None),
        dataDict.get("isLock", 0),)
    dataSourceTable = insertToSQL(Source, *columnsStr)
    if dataSourceTable:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def tableDictSort(table):
    infoDict = {
        "sourceId": table.source_id,
        "levelCode": table.level_code,
        "areaCode": table.area_code,
        "deptCategory": table.dept_category,
        "deptName": table.dept_name,
        "deptAddress": table.dept_address,
        "deptUrl": table.dept_url,
        "createTime": getTimeToStrfdate(table.create_time),
        "createPerson": table.create_person,
        "checkStatus": table.check_status,
        "checkTime": getTimeToStrfdate(table.check_time),
        "checkPerson": table.check_person,
        "checkRemark": table.check_remark,
        "isLock": table.is_lock,
        "desUrl": table.des_url,
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict


# 咨询师 数据源 获取区域 # 根据区域启动来筛选 # 全部都显示  # DeptItemApi getDeptItemList
@app.route("/getItemDeptAreaByConditon", methods=["POST"])
@jwt_required
@queryLog('boss_dept_item')
def getItemDeptAreaByConditon():
    sqlStr = """SELECT distinct t2.area_code, t2.area_name,t2.p_code from data_area as t JOIN base_area as t2 ON t.area_code=t2.area_code and t.area_status = 1 """
    areaCodeList = executeSql(sqlStr)
    infoList = []
    if areaCodeList:
        tableList = []
        for result in areaCodeList:
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


# 咨询师 数据源 获取区域 # 根据分配区域启动来筛选
@app.route("/getUserItemDeptAreaByConditon", methods=["POST"])
@jwt_required
# @queryLog('boss_dept_item')
def getUserItemDeptAreaByConditon():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    roleInfo = findById(Role, "role_id", roleId)
    if not roleInfo:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    ozId = roleInfo.oz_id
    # userId = get_jwt_identity()
    userId = 11
    sqlStr = """SELECT distinct t2.area_code, t2.area_name,t2.p_code from data_area as t JOIN base_area as t2 join boss_area_set as t3 ON t.area_code=t2.area_code and t.area_status = 1 and t3.area_code=t.area_code and t3.oz_id={} and t3.user_id={}""".format(
        ozId, userId)
    areaCodeList = executeSql(sqlStr)
    infoList = []
    if areaCodeList:
        tableList = []
        for result in areaCodeList:
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


def addDataToDepartment(dataSourceUp, dbOperation):
    try:
        categoryTable = Category.query.filter(Category.category_id == dataSourceUp.dept_category).first()
        if categoryTable:
            categoryCode = categoryTable.category_code
        else:
            categoryCode = None
        areaCode = dataSourceUp.area_code
        departmentTable = Department.query.filter(Department.area_code == dataSourceUp.area_code,
                                                  Department.dept_name == dataSourceUp.dept_name).first()
        if departmentTable:
            deptId = departmentTable.dept_id
            deptUrl = departmentTable.dept_url
            if areaCode and categoryCode:
                deptNameKey = str(str(areaCode) + str(categoryCode) + "".join(
                    lazy_pinyin(departmentTable.dept_name, FIRST_LETTER)).encode("utf-8"))
                deptNameKey = deptNameKey.replace("(", "_")
                deptNameKey = deptNameKey.replace("（", "_")
                deptNameKey = deptNameKey.replace(")", "")
                deptNameKey = deptNameKey.replace("）", "")
                scriptCount = SpiderScript.query.filter(SpiderScript.dept_name_key.like(deptNameKey + "%")).count()
                # 如果有重复的表名，则在后面添加一个两位的字符串
                if scriptCount != 0:
                    deptNameKey = deptNameKey + str(scriptCount).zfill(2)
            else:
                return None, None
        else:
            # departmentColumnsStr = (
            #     None, None, dataSourceUp.dept_name, dataSourceUp.dept_address, dataSourceUp.dept_url,
            #     dataSourceUp.is_lock, dataSourceUp.level_code, dataSourceUp.area_code, dataSourceUp.dept_category)
            departmentColumnsStr = (
                None, None, None, dataSourceUp.dept_name, dataSourceUp.dept_address, dataSourceUp.dept_url,
                dataSourceUp.is_lock, dataSourceUp.level_code, dataSourceUp.area_code, dataSourceUp.dept_category)

            departmentTable = dbOperation.insertToSQL(Department, *departmentColumnsStr)
            deptId = departmentTable.dept_id
            deptUrl = departmentTable.dept_url
            if areaCode and categoryCode:
                deptNameKey = str(str(areaCode) + str(categoryCode) + "".join(
                    lazy_pinyin(departmentTable.dept_name, FIRST_LETTER)).encode("utf-8"))
                #  部门名称中带有（）()的情况左括号替换为_；右括号删除；、替换为_
                deptNameKey = deptNameKey.replace(r"(", "_")
                deptNameKey = deptNameKey.replace(r"（", "_")
                deptNameKey = deptNameKey.replace(r")", "")
                deptNameKey = deptNameKey.replace(r"）", "")
                deptNameKey = deptNameKey.replace(r"、", "_")
                scriptCount = SpiderScript.query.filter(SpiderScript.dept_name_key.like(deptNameKey + "%")).count()
                # 如果有重复的表名，则在后面添加一个两位的字符串
                if scriptCount != 0:
                    deptNameKey = deptNameKey + str(scriptCount).zfill(2)
            else:
                return None, None
        scriptTable = SpiderScript.query.filter(SpiderScript.dept_id == deptId).first()
        if scriptTable:
            return departmentTable, scriptTable
        scriptRuleColumnsStr = (deptNameKey, deptId, deptUrl, None, None, None, 0, None, None, None, None, 1)
        scrapyRuleTable = dbOperation.insertToSQL(SpiderScript, *scriptRuleColumnsStr)
        return departmentTable, scrapyRuleTable
    except Exception, e:
        print e
        return None, None


def getAreaCode(areaCode):
    provinceName = ""
    cityName = ""
    districtName = ""
    try:
        areaCode = areaCode
        if areaCode:
            if areaCode[:2] != "00":
                newAreaCode = "{}0000".format(areaCode[:2])
                areaCodetable = Area.query.filter(Area.area_code == newAreaCode).first()
                if areaCodetable:
                    provinceName = areaCodetable.area_name
            if areaCode[2:4] != "00":
                newAreaCode = "{}00".format(areaCode[:4])
                areaCodetable = Area.query.filter(Area.area_code == newAreaCode).first()
                if areaCodetable:
                    cityName = areaCodetable.area_name
            if areaCode[4:6] != "00":
                newAreaCode = "{}".format(areaCode)
                areaCodetable = Area.query.filter(Area.area_code == newAreaCode).first()
                if areaCodetable:
                    districtName = areaCodetable.area_name
        return provinceName, cityName, districtName
    except:
        return provinceName, cityName, districtName
