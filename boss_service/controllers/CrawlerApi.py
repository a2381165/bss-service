# -*- coding: utf-8 -*-
import json
import os
import random
from urllib import quote

from flask import request, json, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.Log import addLog
from common.OperationOfDB import conditionDataListFind3304, executeTheSQLStatement, executeSql
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg
from models.Boss.Area import Area as AreaStatus
from models.Boss.AreaSet import AreaSet
from models.Boss.Role import Role
from models.Boss.User import User
from models.Data.Department import Department
from models.Data.TempItem import TempItem
from models.Other.SourceData import SourceData, tableChangeDic
from version.v3.bossConfig import app
import Res


# 通过条件 筛选数据
@app.route("/listCrawlerData", methods=["POST"])
@jwt_required
# @queryLog("data_temp_item")
def listCrawlerData():
    adminId = get_jwt_identity()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    areaCode = dataDict.get("areaCode", "")
    roleId = dataDict.get("roleId", None)
    if not roleId:
        resultDict = returnErrorMsg("not find roleId")
        return jsonify(resultDict)

    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    if not areaCode:
        # releaseDeptIdList = getAllReleaseDept(adminId, roleId)
        releaseDeptIdList = getAllReleaseDeptS(adminId, roleId)
    else:
        releaseDeptIdList = getOneReleaseDept(areaCode, adminId, roleId)
    if len(releaseDeptIdList) == 0:
        resultDict = returnErrorMsg("not find deptId")
        return jsonify(resultDict)
    else:
        if len(releaseDeptIdList) == 1:
            releaseConditionStr = " and (dept_id in " + str(tuple(releaseDeptIdList)).replace("L", "").replace(",",
                                                                                                               "") + ")"
        else:
            releaseConditionStr = " and (dept_id in " + str(tuple(releaseDeptIdList)).replace("L", "") + ")"
    intColumnClinetNameList = ("deptId", "urlStatus")
    urlStautusCondition = {"field": "urlStatus", "op": "equal", "value": 0}
    deptIdConditonStr = "("
    for cond in dataDict["condition"]:
        field = cond["field"]
        if field == "urlStatus":
            dataDict["condition"].remove(cond)
        elif field == "deptName":
            value = cond["value"]
            deptName = "%" + value + "%"
            deptTableList = Department.query.filter(Department.dept_name.like(deptName)).all()
            for deptTable in deptTableList:
                deptId = deptTable.dept_id
                deptIdConditonStr = deptIdConditonStr + "dept_id = " + str(deptId) + " or "
            dataDict["condition"].remove(cond)
        elif field == "levelCode":
            value = cond["value"]
            levelCode = value
            deptTableList = Department.query.filter(Department.level_code == levelCode).all()
            for deptTable in deptTableList:
                deptId = deptTable.dept_id
                deptIdConditonStr = deptIdConditonStr + "dept_id = " + str(deptId) + " or "
            dataDict["condition"].remove(cond)
    if len(deptIdConditonStr) == 1:
        deptIdConditonStr = releaseConditionStr
    else:
        deptIdConditonStr = " and " + deptIdConditonStr[:-4] + ")" + releaseConditionStr
    dataDict["condition"].append(urlStautusCondition)
    tableName = "zzh_source_data"
    tableList, count = conditionDataListFind3304(dataDict, tableChangeDic, intColumnClinetNameList, tableName, None,
                                                 deptIdConditonStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            deptName = ""
            levelCode = ""
            deptId = tableData.dept_id
            if deptId:
                deptTable = Department.query.filter(Department.dept_id == deptId).first()
                if deptTable:
                    deptName = deptTable.dept_name
                    levelCode = deptTable.level_code
            infoDict = {
                "deptName": deptName,
                "taskId": tableData.task_id,
                "deptNameKey": tableData.dept_name_key,
                "deptId": deptId,
                "itemTitle": tableData.item_title,
                "itemContent": tableData.item_content,
                "itemPulishdate": tableData.item_pulishdate,
                "keyWords": tableData.key_words,
                "itemUrl": tableData.item_url,
                "urlStatus": tableData.url_status,
                "createTime": str(tableData.create_time),
                "itemType": tableData.item_type,
                "levelCode": levelCode,
            }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnMsg({})
    return jsonify(resultDict)


# 批量筛选
@app.route("/dealCrawlersItemStatus", methods=["POST"])
@jwt_required
@addLog("data_temp_item")
def dealCrawlersItemStatus():
    adminId = get_jwt_identity()
    adminTable = User.query.filter(User.admin_id == adminId).first()
    jsonData = request.get_data()
    dictData = json.loads(jsonData)
    taskIds = dictData.get("taskIds", [])

    if len(taskIds) != 0:
        dateTimeNow = getTimeStrfTimeStampNow()
        dbOperation = OperationOfDB()
        successCount = 0
        failedCount = 0
        for taskId in taskIds:
            taskUrlTable = SourceData.query.filter(SourceData.task_id == taskId, SourceData.url_status == 0).first()
            if taskUrlTable:
                # try:
                #     itemDeadLine = taskUrlTable.item_deadline
                #     timeSort = parser.parse(itemDeadLine)
                # except:
                #     timeSort = None
                deptId = taskUrlTable.dept_id
                itemContent = taskUrlTable.item_content
                if itemContent:
                    itemContent = quote('[{"titleItem":"","storItem":0,"contactItem":%s }]' % itemContent, safe=":, /")

                itemImgurl = getItemUrlByDeptId(deptId)
                # columnsStr = (taskUrlTable.dept_id, taskUrlTable.item_url, taskUrlTable.item_title, itemImgurl,
                #               taskUrlTable.item_pulishdate,
                #               dictData.get('itemAlbum', None),
                #               itemContent,
                #               dictData.get('itemIndustryIds', None),
                #               dictData.get("itemLabelIds", None),
                #               dictData.get('checkPerson', None), 0,
                #               dictData.get('checkRemark', None),
                #               dictData.get('checkTime', None),
                #               adminTable.admin_name,
                #               dateTimeNow,
                #               taskUrlTable.item_type,
                #               dictData.get('itemContentAttach', None),
                #               dictData.get('tempItemStatus', 1), dictData.get("isContentJson", 1))
                columnsStr = (
                    taskUrlTable.dept_id,
                    taskUrlTable.item_url,
                    taskUrlTable.item_title,
                    itemImgurl,
                    taskUrlTable.item_pulishdate,
                    dictData.get("itemAlbum", None),
                    dictData.get("itemContent", None),
                    dictData.get("itemIndustryIds", None),
                    dictData.get("itemLabelIds", None),
                    dictData.get("checkPerson", None),
                    0,
                    dictData.get("checkRemark", None),
                    dictData.get("checkTime", None),
                    adminTable.admin_name,
                    dateTimeNow,
                    taskUrlTable.item_type,
                    # dictData.get("createPerson", None),
                    # dictData.get("createTime", None),
                    # dictData.get("itemType", None),
                    dictData.get("itemContentAttach", None),
                    dictData.get("tempItemStatus", 1),
                    dictData.get("isContentJson", 1),
                    dictData.get("isClose", None),
                    dictData.get("itemDeadline", None),
                    dictData.get("isSecular", None),
                    dictData.get("mediaType", None),
                    dictData.get("mediaUrl", None),)
                tempItemTable = dbOperation.insertToSQL(TempItem, *columnsStr)
                taskUrlTable.url_status = 1
                taskUrlTableFin = dbOperation.addTokenToSql(taskUrlTable)
                if tempItemTable and taskUrlTableFin:
                    successCount += 1
                else:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg()
                    return jsonify(resultDict)
            else:
                failedCount += 1
        if dbOperation.commitToSQL():
            infoDict = {"successCount": successCount, "failedCount": failedCount}
            resultDict = returnMsg(infoDict)
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("commit failed")
    else:
        resultDict = returnErrorMsg("not find taskIds!")
    return jsonify(resultDict)


# 批量剔除
@app.route("/dealCrawlers", methods=["POST"])
@jwt_required
@addLog("data_temp_item")
def dealCrawlers():
    """剔除数据"""
    adminId = get_jwt_identity()
    adminTable = User.query.filter(User.admin_id == adminId).first()
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    taskIds = dataDict.get("taskIds", [])
    infoDict = dataDict.get("info", {})
    if len(taskIds) != 0:
        dbOperation = OperationOfDB()
        successCount = 0
        failedCount = 0
        dateTimeNow = getTimeStrfTimeStampNow()
        if infoDict:
            for taskId in taskIds:
                taskUrlTable = SourceData.query.filter(SourceData.task_id == taskId, SourceData.url_status == 0).first()
                if taskUrlTable:
                    deptId = taskUrlTable.dept_id
                    itemImgurl = getItemUrlByDeptId(deptId)
                    columnsStr = (
                        infoDict.get("deptId", None),
                        infoDict.get("itemUrl", None),
                        infoDict.get("itemTitle", None),
                        itemImgurl,
                        infoDict.get("itemPulishdate", None),
                        infoDict.get("itemAlbum", None),
                        infoDict.get("itemContent", None),
                        infoDict.get("itemIndustryIds", None),
                        infoDict.get("itemLabelIds", None),
                        dataDict.get("checkPerson", None),
                        0,
                        dataDict.get("checkRemark", None),
                        dataDict.get("checkTime", None),
                        adminTable.admin_name,
                        dateTimeNow,
                        taskUrlTable.item_type,
                        # dataDict.get("createPerson", None),
                        # dataDict.get("createTime", None),
                        # dataDict.get("itemType", None),
                        dataDict.get("itemContentAttach", None),
                        dataDict.get("tempItemStatus", 2),
                        dataDict.get("isContentJson", 1),
                        dataDict.get("isClose", None),
                        infoDict.get("itemPulishdate", None),
                        dataDict.get("isSecular", None),
                        dataDict.get("mediaType", None),
                        dataDict.get("mediaUrl", None))
                    tempItemTable = dbOperation.insertToSQL(TempItem, *columnsStr)
                    taskUrlTable.url_status = 1
                    taskUrlTableFin = dbOperation.addTokenToSql(taskUrlTable)
                    if tempItemTable and taskUrlTableFin:
                        successCount += 1
                    else:
                        dbOperation.commitRollback()
                        resultDict = returnErrorMsg()
                        return jsonify(resultDict)
                else:
                    failedCount += 1
        else:
            for taskId in taskIds:
                taskUrlTable = SourceData.query.filter(SourceData.task_id == taskId, SourceData.url_status == 0).first()
                if taskUrlTable:
                    # try:
                    #     itemDeadLine = taskUrlTable.item_deadline
                    #     timeSort = parser.parse(itemDeadLine)
                    # except:
                    #     timeSort = None
                    deptId = taskUrlTable.dept_id
                    itemImgurl = getItemUrlByDeptId(deptId)
                    columnsStr = (
                        taskUrlTable.dept_id,
                        taskUrlTable.item_url,
                        taskUrlTable.item_title,
                        itemImgurl,
                        taskUrlTable.item_pulishdate,
                        dataDict.get("itemAlbum", None),
                        dataDict.get("itemContent", None),
                        dataDict.get("itemIndustryIds", None),
                        dataDict.get("itemLabelIds", None),
                        dataDict.get("checkPerson", None),
                        0,
                        dataDict.get("checkRemark", None),
                        dataDict.get("checkTime", None),
                        adminTable.admin_name,
                        dateTimeNow,
                        taskUrlTable.item_type,
                        # dataDict.get("createPerson", None),
                        # dataDict.get("createTime", None),
                        # dataDict.get("itemType", None),
                        dataDict.get("itemContentAttach", None),
                        dataDict.get("tempItemStatus", 2),
                        dataDict.get("isContentJson", 1),
                        dataDict.get("isClose", None),
                        dataDict.get("itemDeadline", None),
                        dataDict.get("isSecular", None),
                        dataDict.get("mediaType", None),
                        dataDict.get("mediaUrl", None))

                    tempItemTable = dbOperation.insertToSQL(TempItem, *columnsStr)
                    taskUrlTable.url_status = 1
                    taskUrlTableFin = dbOperation.addTokenToSql(taskUrlTable)
                    if tempItemTable and taskUrlTableFin:
                        successCount += 1
                    else:
                        dbOperation.commitRollback()
                        resultDict = returnErrorMsg()
                        return jsonify(resultDict)
                else:
                    failedCount += 1
        if dbOperation.commitToSQL():
            infoDict = {"successCount": successCount, "failedCount": failedCount}
            resultDict = returnMsg(infoDict)
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("commit failed")
    else:
        resultDict = returnErrorMsg("not find taskIds!")
    return jsonify(resultDict)

# 使用中  正常
def getAllReleaseDeptS(adminId, roleId):
    """查询所有添加区域部门id列表"""
    areaCodeList = []
    releaseDeptIdList = []
    if str(roleId) == Res.all_role["jsbbz"]:
        areaCodeSql = "select area_code from data_area where area_status =1"
    else:
        areaCodeSql = "SELECT t1.area_code FROM data_area as t1 JOIN boss_area_set as t2 join boss_role as t3 ON t1.area_status=1 and t2.user_id={} and  t1.area_code = t2.area_code  and t3.role_id={} and t2.oz_id=t3.oz_id;".format(
            adminId, roleId)
    areaList = executeSql(areaCodeSql)
    leftInfoList = []
    for area in areaList:
        if area[0][2:] == "0000":
            areaCodeList.append(str(area[0]))
        else:
            leftInfoList.append(str(area[0][:4]))
    if not (areaCodeList or leftInfoList):
        return areaCodeList
    if len(areaCodeList) == 1:
        areaCodeList = str(tuple(areaCodeList)).replace(",", "")
        # sSql += "area_code = {} ".format(areaCodeList[0])
    elif len(areaCodeList) > 1:
        areaCodeList = tuple(areaCodeList)
    if len(leftInfoList) == 1:
        leftInfoList = str(tuple(leftInfoList)).replace(",", "")
    elif len(leftInfoList) > 1:
        leftInfoList = tuple(leftInfoList)
    sqlStr = """select t1.dept_id from data_department as t1 join data_area as t2 on (t1.area_code in {}  or (left(t2.area_code,4) in {} and  t1.area_code =t2.area_code))""".format(
        areaCodeList, leftInfoList)
    releaseDeptColList = executeSql(sqlStr)
    for deptCol in releaseDeptColList:
        releaseDeptIdList.append(deptCol[0])
    return sorted(list(set(releaseDeptIdList)))


# 使用中
def getOneReleaseDept(areaCode, adminId, roleId):
    """查询所有添加区域部门id列表"""
    # releaseDeptIdList = []
    # if areaCode[2:4] != '00':
    #     allSql = "select dept_id from data_department join data_area on  data_area.area_status=1 and data_area.area_code like '{}%' and data_department.area_code=data_area.area_code".format(
    #         areaCode[:4])
    # else:
    #     allSql = "select dept_id from data_department join data_area on  data_area.area_status=1 and data_area.area_code = '{}' and data_department.area_code=data_area.area_code".format(
    #         areaCode)
    # releaseDeptColList = executeSql(allSql)
    # for deptCol in releaseDeptColList:
    #     releaseDeptIdList.append(int(deptCol[0]))
    # return releaseDeptIdList
    # areaSql = "select area_code from data_area where area_code like '{}%' and area_status=1".format(areaCode[:4])
    # areaSql = "select area_code from data_area where area_code='{}' and area_status=1".format(areaCode)
    # allSql = "select dept_id from data_department where area_code in ({})".format(areaSql)
    releaseList = []
    releaseDeptIdList = []
    role = Role.query.filter(Role.role_id == roleId).first()
    if not role:
        return releaseDeptIdList
    if str(roleId) != Res.all_role["jsbbz"]:
        ozId = role.oz_id
        table = AreaSet.query.filter(AreaSet.oz_id == ozId, AreaSet.user_id == adminId,
                                     AreaSet.area_code == areaCode).first()
        if not table:
            return releaseDeptIdList
    if areaCode[2:4] != '00':
        areaTableList = AreaStatus.query.filter(AreaStatus.area_code.like("{}%".format(areaCode[:4])),
                                                AreaStatus.area_status == 1).all()
    else:
        areaTableList = AreaStatus.query.filter(AreaStatus.area_code == areaCode, AreaStatus.area_status == 1).all()
    for areaTable in areaTableList:
        releaseList.append(str(areaTable.area_code))
    if len(releaseList) == 0:
        return releaseDeptIdList
    elif len(releaseList) == 1:
        sql_str = "select dept_id from data_department where area_code = {}".format(releaseList[0])
    else:
        sql_str = "select dept_id from data_department where (area_code in " + str(
            tuple(releaseList)).replace("L", "") + str(")")
    releaseDeptColList = executeTheSQLStatement(sql_str)
    for deptCol in releaseDeptColList:
        releaseDeptIdList.append(int(deptCol[0]))
    return releaseDeptIdList


# 咨询师业务查询使用中 ItemServerApi
def getOneReleaseDepts(areaCode):
    """查询所有添加区域部门id列表"""
    # releaseDeptIdList = []
    # if areaCode[2:4] != '00':
    #     allSql = "select dept_id from data_department join data_area on  data_area.area_status=1 and data_area.area_code like '{}%' and data_department.area_code=data_area.area_code".format(
    #         areaCode[:4])
    # else:
    #     allSql = "select dept_id from data_department join data_area on  data_area.area_status=1 and data_area.area_code = '{}' and data_department.area_code=data_area.area_code".format(
    #         areaCode)
    # releaseDeptColList = executeSql(allSql)
    # for deptCol in releaseDeptColList:
    #     releaseDeptIdList.append(int(deptCol[0]))
    # return releaseDeptIdList
    # areaSql = "select area_code from data_area where area_code like '{}%' and area_status=1".format(areaCode[:4])
    # areaSql = "select area_code from data_area where area_code='{}' and area_status=1".format(areaCode)
    # allSql = "select dept_id from data_department where area_code in ({})".format(areaSql)

    releaseList = []
    releaseDeptIdList = []
    # table = AreaSet.query.filter(AreaSet.oz_id ==ozId,AreaSet.user_id==adminId,AreaSet.area_code==areaCode).first()
    # if not table:
    #     return releaseDeptIdList
    if areaCode[2:4] != '00':
        areaTableList = AreaStatus.query.filter(AreaStatus.area_code.like("{}%".format(areaCode[:4])),
                                                AreaStatus.area_status == 1).all()
    else:
        areaTableList = AreaStatus.query.filter(AreaStatus.area_code == areaCode, AreaStatus.area_status == 1).all()
    for areaTable in areaTableList:
        releaseList.append(str(areaTable.area_code))
    if len(releaseList) == 0:
        return releaseDeptIdList
    elif len(releaseList) == 1:
        sql_str = "select dept_id from data_department where (area_code in " + str(
            tuple(releaseList)).replace("L", "").replace(",", "") + str(")")
    else:
        sql_str = "select dept_id from data_department where (area_code in " + str(
            tuple(releaseList)).replace("L", "") + str(")")
    releaseDeptColList = executeTheSQLStatement(sql_str)
    for deptCol in releaseDeptColList:
        releaseDeptIdList.append(int(deptCol[0]))
    return releaseDeptIdList


# 查询图片 使用中
def getItemUrlByDeptId(dept_id):
    try:
        deptTable = Department.query.filter(Department.dept_id == dept_id).first()
        img_list = ["./static/dept_img/sblc_tupian1@2x.png"]
        if deptTable:
            categoryCode = deptTable.category.category_code
            imagePath = categoryCode[0] + "00"
            if imagePath == "000":
                walk_path = "./static/dept_img"
            else:
                walk_path = "./static/dept_img/" + imagePath
            img_list = []
            for img_path, img_dir, img_file in os.walk(walk_path):
                for file_i in img_file:
                    file_path = img_path + "/" + file_i
                    img_list.append(file_path)
        item_image = random.sample(img_list, 1)[0].replace("\\", "/")
    except:
        item_image = "./static/dept_img/sblc_tupian1@2x.png"
    return item_image[2:]


# 未使用
def getReleaseArea(areaType):
    areaTableList = AreaStatus.query.filter(AreaStatus.area_type == areaType, AreaStatus.area_status == 1).all()
    areaIdList = []
    for areaTable in areaTableList:
        areaIdList.append(areaTable.area_id)
    return areaIdList


# 使用中 废弃
def getAllReleaseDept(adminId, roleId):
    """查询所有添加区域部门id列表"""
    areaCodeList = []
    releaseDeptIdList = []
    # 普通
    # areaCodeSql = "select area_code from data_area where area_status=1 and id in (select data_area_id from boss_area_set where user_id={})".format(
    #     adminId)
    # 优化
    areaCodeSql = "SELECT t1.area_code FROM data_area as t1 JOIN boss_area_set as t2 join boss_role as t3 ON t1.area_status=1 and t2.user_id={} and  t1.area_code = t2.area_code  and t3.role_id={} and t2.oz_id=t3.oz_id;".format(
        adminId, roleId)

    # print areaCodeSql
    areaList = executeSql(areaCodeSql)
    leftInfoList = []
    for area in areaList:
        # if area[0][2:] == "0000":
        #     leftInfoList.append(str(area[0]))
        # else:
        areaCodeList.append(str(area[0]))
    # print areaCodeList
    if not areaCodeList:
        return areaCodeList
    # sSql = "("
    if len(areaCodeList) == 1:
        areaCodeList = str(tuple(areaCodeList)).replace(",", "")
        # sSql += "area_code = {} ".format(areaCodeList[0])
    elif len(areaCodeList) > 1:
        areaCodeList = tuple(areaCodeList)
        # sSql += "area_code in {} ".format(tuple(areaCodeList[0]))
    # if len(leftInfoList) == 1:
    #     if sSql != "(":
    #         sSql += " or left(area_code,4) = '{}' ".format(areaCodeList[0][:4])
    #     else:
    #         sSql += " left(area_code,4) = '{}' ".format(areaCodeList[0][:4])
    # elif len(leftInfoList) > 1:
    #     if sSql != "(":
    #         sSql += " or left(area_code,4) in {} ".format(tuple([area[:4] for area in areaCodeList]))
    #     else:
    #         sSql += " left(area_code,4) in {} ".format(tuple([area[:4] for area in areaCodeList]))
    # sSql += ")"
    sqlStr = """select dept_id from data_department where area_code in {}""".format(areaCodeList)
    # sqlStr = """select dept_id from data_department where """ + sSql
    # print sqlStr

    releaseDeptColList = executeSql(sqlStr)
    for deptCol in releaseDeptColList:
        releaseDeptIdList.append(deptCol[0])
    return sorted(list(set(releaseDeptIdList)))
