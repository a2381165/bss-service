# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, updataById, findById, addTokenToSql,deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from common.UserAreaDept import getAreaSql
from controllers.CrawlerApi import getAllReleaseDeptS, getOneReleaseDepts
from models.Boss.User import User
from models.Data.Department import Department
from models.Data.Item import Item
from models.Data.ItemService import ItemService, tableChangeDic
from models.Data.TempService import TempService
from version.v3.bossConfig import app


# 项目顶层分析 列表
@app.route("/findItemServiceByCondition", methods=["POST"])
@jwt_required
def findItemServiceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    areaCode = dataDict.get("areaCode", "")
    roleId = dataDict.get("roleId", "")
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminId = get_jwt_identity()
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    first = False
    for _cond in condition:
        if _cond["field"] == "isLock":
            first = True
    if not first:
        newDict = {
            "field": "isLock",
            "op": "equal",
            "value": 1
        }
        condition.append(newDict)
    sqlStr = getAreaSql(adminId, roleId, areaCode)
    if not sqlStr:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = (u'id', u'itemId', u'deptId', "isLock", "checkStatus")
    tableName = "view_item_server_dept_cate"
    orderByStr = " order by create_time desc "
    newChagne = {"areaCode": "area_code"}
    newChagne = dict(view_item_server_dept_cate, **newChagne)
    itemList, count = conditionDataListFind(dataDict, newChagne, intColumnClinetNameList, tableName,
                                            orderByStr=orderByStr, deptIdConditonStr=sqlStr)
    if itemList:
        InfoList = []
        for tableData in itemList:
            if tableData[5]:
                directions = tableData[5].split("/")
            else:
                directions = []
            infoDict = {
                "id": tableData[0],
                "itemId": tableData[1],
                "deptId": tableData[2],
                "createPerson": tableData[3],
                "createTime": tableData[4],
                "directions": tableData[5],
                "checkStatus": tableData[6],
                "checkPerson": tableData[7],
                "checkRemark": tableData[8],
                "checkTime": tableData[9],
                "isLock": tableData[10],
                "itemUrl": tableData[11],
                "itemTitle": tableData[12],
                "itemImgurl": tableData[13],
                "itemPulishdate": tableData[14],
                "itemIsLock": tableData[15],
                "itemType": tableData[16],
                "isService": tableData[17],
                "isContentJson": tableData[18],
                "isClose": tableData[19],
                "itemDeadline": tableData[20],
                "isSecular": tableData[21],
                "deptName": tableData[22],
                "levelCode": tableData[23],
                "categoryName": tableData[24],
                "areaCode": tableData[25],
                "itemSort": tableData[26],
                "isTop": tableData[27],
                "directionsText": directions,
            }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 编辑子方向 # 放弃维护 # 送审 # 退回
@app.route("/updateItemService", methods=["POST"])
@jwt_required
def updateItemService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", None)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'itemId', u'deptId', "isLock", "checkStatus","isLock"]
    dataDict["createPerson"] = current_user.admin_name
    table = updataById(ItemService, dataDict, "id", id, tableChangeDic, intColumnClinetNameList=intColumnClinetNameList)
    if table:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg("update fail")
    return jsonify(resultDict)


# 筛选
@app.route("/chooseItemService", methods=["POST"])
@jwt_required
def chooseItemService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", None)
    isLock = dataDict.get("isLock",None)
    if not (idList and isLock):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'itemId', u'deptId', "isLock", "checkStatus"]
    dataDict["createPerson"] = current_user.admin_name
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.updateThis(ItemService, ItemService.id, id, dataDict, tableChangeDic,
                                       intColumnClinetNameList=intColumnClinetNameList)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("update fail")
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("update fail")
    return jsonify(resultDict)


#  # 送审
@app.route("/updateSendItemServiceStatus", methods=["POST"])
@jwt_required
def updateSendItemServiceStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", None)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'itemId', u'deptId', "checkStatus"]
    newDict = {"checkStatus": 1, "createPerson": current_user.admin_name}
    table = updataById(ItemService, newDict, "id", id, tableChangeDic, intColumnClinetNameList=intColumnClinetNameList)
    if table:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg("update fail")
    return jsonify(resultDict)


# 审核
@app.route("/checkItemService", methods=["POST"])
@jwt_required
def checkItemService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus", "")

    if not (id and checkStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    itemServiceInfo = findById(ItemService, "id", id)
    if not itemServiceInfo:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminName = current_user.admin_name
    now = getTimeStrfTimeStampNow()
    dataDict["checkPerson"] = adminName
    dataDict["checkTime"] = now
    dbOperation = OperationOfDB()
    # 审核通过
    if checkStatus == 2:
        # 支持方向
        directions = str(itemServiceInfo.directions).split("/")
        for direction_name in directions:
            # 创建临时底层项目分析表
            # TempService
            itemId = itemServiceInfo.item_id
            itemInfo = findById(Item, "item_id", itemId)
            # directionInfo = findById(DeptItem, "id", direction_id)
            # direction_name = directionInfo.name
            tempServiceStr = [itemId]
            tempServiceStr.extend([None, ] * 24)  # 25
            tempServiceStr[2] = itemInfo.item_pulishdate  # service_starttime
            tempServiceStr[3] = itemInfo.is_secular  # 0  # is_secular
            tempServiceStr[4] = itemInfo.item_deadline  # service_deadline
            tempServiceStr[5] = direction_name  # 方向名称
            tempServiceStr[10] = 0  # is_evaluate
            tempServiceStr[16] = 0  # checkStatus
            tempServiceStr[20] = current_user.admin_name  # create_person
            tempServiceStr[21] = now  # create_time

            tempServiceInfo = dbOperation.insertToSQL(TempService, *tempServiceStr)
            if not tempServiceInfo:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["system_error"])
                return jsonify(resultDict)
    # 更新ItemService
    itemServiceInfo = dbOperation.updateThis(ItemService, ItemService.id, id, dataDict, tableChangeDic)
    if not itemServiceInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitToSQL()
        resultDict = returnErrorMsg("commit fail")
    return jsonify(resultDict)


# 选择 咨询师 来处理底层分析 那这里就需要展示列表了
@app.route("/choiceUserInTempService", methods=["POST"])
def choiceUserInTempService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", None)
    userId = dataDict.get("userId", None)
    if not (id and userId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(TempService, "id", id)
    userInfo = findById(User, "admin_id", userId)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table.service_person = userInfo.admin_name
    table = addTokenToSql(table)
    if not table:
        resultDict = returnErrorMsg("update fail")
    else:
        resultDict = returnMsg({})
    return jsonify(resultDict)


### 咨询师业务筛序
# 根据条件查询
@app.route("/findItemServerByConditions", methods=["POST"])
@jwt_required
def findItemServerByConditions():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    areaCode = dataDict.get("areaCode")
    roleId = dataDict.get("roleId", "")
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminId = get_jwt_identity()
    if not areaCode:
        if roleId:
            releaseDeptIdList = getAllReleaseDeptS(adminId, roleId)
        else:
            resultDict = returnErrorMsg("not find roleId")
            return jsonify(resultDict)
    else:
        releaseDeptIdList = getOneReleaseDepts(areaCode)
    if len(releaseDeptIdList) == 0:
        resultDict = returnErrorMsg("not find deptId")
        return jsonify(resultDict)
    else:
        if len(releaseDeptIdList) == 1:
            releaseConditionStr = " and (dept_id in " + str(tuple(releaseDeptIdList)).replace("L", "").replace(",",
                                                                                                               "") + ")"
        else:
            releaseConditionStr = " and (dept_id in " + str(tuple(releaseDeptIdList)).replace("L", "") + ")"
    # intColumnClinetNameList = ("deptId", "urlStatus")
    # urlStautusCondition = {"field": "urlStatus", "op": "equal", "value": 0}
    deptIdConditonStr = "("
    for cond in dataDict["condition"]:
        field = cond["field"]
        if field == "deptName":
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
        if dataDict.get("condition") == []:
            deptIdConditonStr = " where " + releaseConditionStr[4:]
        else:
            deptIdConditonStr = releaseConditionStr
    else:
        if dataDict.get("condition") == []:
            deptIdConditonStr = " where " + deptIdConditonStr[:-4] + ")" + releaseConditionStr
        else:
            deptIdConditonStr = " and " + deptIdConditonStr[:-4] + ")" + releaseConditionStr

    intColumnClinetNameList = ("itemId", "deptId", "itemSort",
                               "isLock", "isTop", "isService", "levelCode",)
    tableName = Item.__tablename__
    orderByStr = " order by item_sort asc ,create_time desc "
    # condition = dataDict.get("condition", [])
    # for daDict in condition:
    #     if daDict.get("field", None) == "levelCode":
    #         deptList = Department.query.filter(Department.level_code == int(daDict.get("value")))
    #         deptIds = [int(dept.dept_id) for dept in deptList]
    #         if len(deptIds) == 1:
    #             deptIds = str(tuple(deptIds)).replace(",", "")
    #         else:
    #             deptIds = str(tuple(deptIds))
    #         newDict = {
    #             "field": "deptId",
    #             "op": "in",
    #             "value": deptIds
    #         }
    #         condition.remove(daDict)
    #         condition.append(newDict)
    #     elif daDict.get("field", None) == "deptName":
    #         deptList = Department.query.filter(Department.dept_name.like("%{}%".format(str(daDict.get("value")))))
    #         deptIds = [int(dept.dept_id) for dept in deptList]
    #         if len(deptIds) == 1:
    #             deptIds = str(tuple(deptIds)).replace(",", "")
    #         else:
    #             deptIds = str(tuple(deptIds))
    #         newDict = {
    #             "field": "deptId",
    #             "op": "in",
    #             "value": deptIds
    #         }
    #         condition.remove(daDict)
    #         condition.append(newDict)
    # newChange = dict(tableChangeDic,**otherChangeDic)
    itemList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName,
                                            deptIdConditonStr=deptIdConditonStr,
                                            orderByStr=orderByStr)
    if itemList:
        InfoList = []
        for itemTable in itemList:
            # infoDict = returnInformation(itemTable)
            infoDict = {}
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

# 删除
@app.route("/deleteItemService", methods=["POST"])
@jwt_required
def deleteItemService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(ItemService, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)

# 筛选


view_item_server_dept_cate = {
    "id": "id",
    "itemId": "item_id",
    "deptId": "dept_id",
    "createPerson": "create_person",
    "createTime": "create_time",
    "directions": "directions",
    "checkStatus": "check_status",
    "checkPerson": "check_person",
    "checkRemark": "check_remark",
    "checkTime": "check_time",
    "isLock": "is_lock",
    "itemUrl": "item_url",
    "itemTitle": "item_title",
    "itemImgurl": "item_imgurl",
    "itemPulishdate": "item_pulishdate",
    "itemIsLock": "item_is_lock",
    "itemType": "item_type",
    "isService": "is_service",
    "isContentJson": "is_content_json",
    "isClose": "is_close",
    "itemDeadline": "item_deadline",
    "isSecular": "is_secular",
    "deptName": "dept_name",
    "levelCode": "level_code",
    "categoryName": "category_name",
    "areaCode": "area_code",
    "itemSort": "item_sort",
    "isTop": "is_top",
}
