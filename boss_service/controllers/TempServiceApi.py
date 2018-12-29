# coding:utf-8
from flask import jsonify, json, request, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, updataById, findById, insertToSQL,deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnErrorMsg, returnMsg, returnErrorMsg, errorCode
from models.Data.Service import Service
from models.Data.TempService import TempService, TempServiceChangeDic as tableChangeDic,intList
from version.v3.bossConfig import app
from common.UserAreaDept import getAreaSql
from models.Data.ServiceAttach import ServiceAttach
from models.Boss.DeptItem import DeptItem
from common.DeptItemGrading import getDeptItem
from models.Data.Item import Item
from models.Boss.Area import Area


# 获取底层分析列表
@app.route("/findTempServiceByCondition", methods=["POST"])
@jwt_required
def findTempServiceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", "")
    areaCode = dataDict.get("areaCode", "")
    if not (dataDict.has_key("condition") and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminId = get_jwt_identity()
    sqlStr = getAreaSql(adminId, roleId, areaCode)
    if not sqlStr:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newDict = {
        "field": "servicePerson",
        "op": "equal",
        "value": current_user.admin_name
    }
    condition.append(newDict)
    intColumnClinetNameList = [u'id', u'itemId', u'directionName', u'checkStatus', u'isSecular', u'isEvaluate', u'categoryType']
    # tableName = "view_temp_service_item_dept"
    tableName = "view_temp_service_item_dept"
    orderByStr = " order by create_time desc "
    resultList, count = conditionDataListFind(dataDict, newChangeDict, intColumnClinetNameList, tableName,
                                              deptIdConditonStr=sqlStr, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            declareList = []
            materialList = []
            sheetContent = []
            policySourceText = []
            expathDict = {}
            sheetContentNum = tableData[8]
            materialListNum = tableData[9]
            forecastPathNum = tableData[10]
            declareListNum = tableData[16]
            if declareListNum:
                try:
                    declareList = json.loads(declareListNum)
                except:
                    declareList = []
            if materialListNum:
                try:
                    materialList = json.loads(materialListNum)
                except:
                    materialList = []
            if sheetContentNum:
                try:
                    sheetContent = json.loads(sheetContentNum)
                except:
                    sheetContent = []
            # if tableData[2]:
            #     try:
            #         policySource = json.loads(tableData[2])
            #     except:
            #         policySource = []
            #     try:
            #         for _s_attch in json.loads(tableData[2]):
            #             table = findById(ServiceAttach, "id", _s_attch)
            #             if table:
            #                 title = table.attach_title
            #                 policySourceText.append(title)
            #     except Exception as e:
            #         print e
            #         policySourceText = []
            if forecastPathNum:
                try:
                    expathDict = json.loads(forecastPathNum)
                    expathDict["path"] = url_for("static", filename=expathDict["path"], _external=True)
                except Exception as e:
                    expathDict = {}
            infoDict = {
                "id": tableData[0],
                "itemId": tableData[1],
                "servicePrice": tableData[2],
                "serviceStarttime": tableData[3],
                "isSecular": tableData[4],
                "serviceDeadline": tableData[5],
                "directionName": tableData[6],
                "policySource": tableData[7],
                # "sheetContent": tableData[8],
                # "materialList": tableData[9],
                # "forecastPath": tableData[10],
                "isEvaluate": tableData[11],
                "servicePerson": tableData[12],
                "serviceContactPerson": tableData[13],
                "serviceContactPhone": tableData[14],
                "serviceContent": tableData[15],
                # "declareList": tableData[16],
                "checkStatus": tableData[17],
                "checkPerson": tableData[18],
                "checkTime": tableData[19],
                "checkRemark": tableData[20],
                "createPerson": tableData[21],
                "createTime": tableData[22],
                "deptName": tableData[23],
                "levelCode": tableData[24],
                "categoryName": tableData[25],
                "areaCode": tableData[26],
                "itemUrl": tableData[27],
                "itemTitle": tableData[28],
                "itemImgurl": tableData[29],
                "itemPulishdate": tableData[30],
                "itemType": tableData[31],
                "isLock": tableData[32],
                "isService": tableData[33],
                "isContentJson": tableData[34],
                "isClose": tableData[35],
                "itemDeadline": tableData[36],
                "categoryType": tableData[37],
                "serviceName": tableData[38],
                "servciceProcess": tableData[39],
                "mediaType": tableData[40],
                "mediaUrl": tableData[41],
                # "policySource": policySource,
                "policySourceText": policySourceText,
                "materialList": materialList,
                "forecastPath": expathDict,
                "declareList": declareList,
                "sheetContent": sheetContent,
            }
            infoDict = dictRemoveNone(infoDict)
            infoList.append(infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取底层分析列表 部长专用
@app.route("/findMinisterTempServiceByCondition", methods=["POST"])
@jwt_required
def findMinisterTempServiceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", "")
    areaCode = dataDict.get("areaCode", "")
    if not (dataDict.has_key("condition") and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminId = get_jwt_identity()
    sqlStr = getAreaSql(adminId, roleId, areaCode)
    if not sqlStr:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'itemId', u'directionName', u'checkStatus', u'isSecular', u'isEvaluate', u'categoryType']
    # tableName = "view_temp_service_item_dept"
    tableName = "view_temp_service_item_dept"
    orderByStr = " order by item_pulishdate desc "
    if sqlStr:
        resultList, count = conditionDataListFind(dataDict, newChangeDict, intColumnClinetNameList, tableName,
                                                  deptIdConditonStr=sqlStr,
                                                  orderByStr=orderByStr)
    else:
        resultList, count = conditionDataListFind(dataDict, newChangeDict, intColumnClinetNameList, tableName,
                                                  orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            declareList = []
            materialList = []
            sheetContent = []
            policySourceText = []
            forecastPath = ""
            sheetContentNum = tableData[8]
            materialListNum = tableData[9]
            forecastPathNum = tableData[10]
            declareListNum = tableData[16]
            if declareListNum:
                try:
                    declareList = json.loads(declareListNum)
                except:
                    declareList = []
            if materialListNum:
                try:
                    materialList = json.loads(materialListNum)
                except:
                    materialList = []
            if sheetContentNum:
                try:
                    sheetContent = json.loads(sheetContentNum)
                except:
                    sheetContent = []
            # if tableData[2]:
            #     try:
            #         policySource = json.loads(tableData[2])
            #     except:
            #         policySource = []
            #     try:
            #         for _s_attch in json.loads(tableData[2]):
            #             table = findById(ServiceAttach, "id", _s_attch)
            #             if table:
            #                 title = table.attach_title
            #                 policySourceText.append(title)
            #     except Exception as e:
            #         print e
            #         policySourceText = []
            if forecastPathNum:
                try:
                    forecastPath = url_for("static", filename=forecastPathNum, _external=True)
                except Exception as e:
                    print e
                    forecastPath = ""
            infoDict = {
                "id": tableData[0],
                "itemId": tableData[1],
                "servicePrice": tableData[2],
                "serviceStarttime": tableData[3],
                "isSecular": tableData[4],
                "serviceDeadline": tableData[5],
                "directionName": tableData[6],
                "policySource": tableData[7],
                # "sheetContent": tableData[8],
                # "materialList": tableData[9],
                # "forecastPath": tableData[10],
                "isEvaluate": tableData[11],
                "servicePerson": tableData[12],
                "serviceContactPerson": tableData[13],
                "serviceContactPhone": tableData[14],
                "serviceContent": tableData[15],
                # "declareList": tableData[16],
                "checkStatus": tableData[17],
                "checkPerson": tableData[18],
                "checkTime": tableData[19],
                "checkRemark": tableData[20],
                "createPerson": tableData[21],
                "createTime": tableData[22],
                "deptName": tableData[23],
                "levelCode": tableData[24],
                "categoryName": tableData[25],
                "areaCode": tableData[26],
                "itemUrl": tableData[27],
                "itemTitle": tableData[28],
                "itemImgurl": tableData[29],
                "itemPulishdate": tableData[30],
                "itemType": tableData[31],
                "isLock": tableData[32],
                "isService": tableData[33],
                "isContentJson": tableData[34],
                "isClose": tableData[35],
                "itemDeadline": tableData[36],
                "categoryType": tableData[37],
                "serviceName": tableData[38],
                "servciceProcess": tableData[39],
                "mediaType": tableData[40],
                "mediaUrl": tableData[41],
                # "policySource": policySource,
                "policySourceText": policySourceText,
                "materialList": materialList,
                "forecastPath": forecastPath,
                "declareList": declareList,
                "sheetContent": sheetContent,
            }
            infoDict = dictRemoveNone(infoDict)
            infoList.append(infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 更新 完善 提交
@app.route("/updateTempService", methods=["POST"])
@jwt_required
def updateTempService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", None)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.has_key("serviceDeadline"):
        if not dataDict.get("serviceDeadline"):
            dataDict.pop("serviceDeadline")
    if dataDict.has_key("serviceContactPhone"):
        if len(dataDict.get("serviceContactPhone")) != 11:
            resultDict = returnErrorMsg(errorCode["phone_args_fail"])
            return jsonify(resultDict)
    # if dataDict.has_key("serviceContent"):
    #     print len(dataDict["serviceContent"])
    #     print dataDict["serviceContent"]
    intColumnClinetNameList = [u'id', u'itemId', u'isSecular', u'isEvaluate', u'checkStatus', u'categoryType']
    table = updataById(TempService, dataDict, "id", id, tableChangeDic, intColumnClinetNameList=intColumnClinetNameList)
    if table:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg("update fail")
    return jsonify(resultDict)


# 送审
@app.route("/updateSendTempServiceStatus", methods=["POST"])
@jwt_required
def updateSendTempServiceStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", None)
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    newDict = {"checkStatus": 1}
    intColumnClinetNameList = [u'id', u'itemId', u'directionName', u'checkStatus', u'isSecular', u'isEvaluate', u'categoryType']
    table = updataById(TempService, newDict, "id", id, tableChangeDic, intColumnClinetNameList=intColumnClinetNameList)
    if table:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg("update fail")
    return jsonify(resultDict)

# 咨询副部长 审核
@app.route("/checkCoTempService",methods=["POST"])
@jwt_required
def checkCoTempService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus", "")

    if not (id and checkStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    itemServiceInfo = findById(TempService, "id", id)
    if not itemServiceInfo:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    # 更新tempService
    tempServiceInfo = dbOperation.updateThis(TempService, TempService.id, id, dataDict, tableChangeDic)
    if not tempServiceInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
    return jsonify(resultDict)

# 审核
@app.route("/checkTempService", methods=["POST"])
@jwt_required
def checkTempService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus", "")

    if not (id and checkStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    itemServiceInfo = findById(TempService, "id", id)
    if not itemServiceInfo:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    # 审核通过
    if checkStatus == 5:
        # 创建正式服务表
        table = itemServiceInfo
        now = getTimeStrfTimeStampNow()
        serviceStr = (
            table.item_id,table.service_name, table.policy_source, table.service_price, table.service_starttime, table.service_deadline,
            table.direction_name, table.service_content, table.sheet_content, table.material_list,
            table.forecast_path, table.service_contact_person, table.service_contact_phone, table.is_secular,
            table.is_evaluate, table.declare_list, now,
            table.category_type, table.servcice_process)
        serviceInfo = dbOperation.insertToSQL(Service, *serviceStr)
        if not serviceInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["system_error"])
            return jsonify(resultDict)
        # 更新  正式item isService
        itemInfo = findById(Item, "item_id", table.item_id)
        if not itemInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        itemInfo.is_service = 1
        itemInfo = dbOperation.addTokenToSql(itemInfo)
        if not itemInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    else:
        pass
    # 更新tempService
    tempServiceInfo = dbOperation.updateThis(TempService, TempService.id, id, dataDict, tableChangeDic)
    if not tempServiceInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["system_error"])
    return jsonify(resultDict)


# 新增
@app.route("/addTempService", methods=["POST"])
@jwt_required
def addTempService():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    itemId = dataDict.get("itemId", "")
    if not itemId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    itemInfo = findById(Item,"item_id",itemId)
    if not Area.query.filter(Area.area_code==itemInfo.area_code,Area.area_status==1).first():
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


    adminName = current_user.admin_name
    now = getTimeStrfTimeStampNow()
    itemId = dataDict.get("itemId", None)
    servicePrice = dataDict.get("servicePrice", None)
    serviceStarttime = dataDict.get("serviceStarttime", None)
    isSecular = dataDict.get("isSecular", None)
    # serviceDeadline = dataDict.get("serviceDeadline", None)
    directionName = dataDict.get("directionName", None)
    policySource = dataDict.get("policySource", None)
    sheetContent = dataDict.get("sheetContent", None)
    materialList = dataDict.get("materialList", None)
    forecastPath = dataDict.get("forecastPath", None)
    isEvaluate = dataDict.get("isEvaluate", None)
    servicePerson = dataDict.get("servicePerson", adminName)
    serviceContactPerson = dataDict.get("serviceContactPerson", None)
    serviceContactPhone = dataDict.get("serviceContactPhone", None)
    serviceContent = dataDict.get("serviceContent", None)
    declareList = dataDict.get("declareList", None)
    checkStatus = dataDict.get("checkStatus", 0)
    checkPerson = dataDict.get("checkPerson", None)
    checkTime = dataDict.get("checkTime", None)
    checkRemark = dataDict.get("checkRemark", None)
    createPerson = dataDict.get("createPerson", None)
    createTime = dataDict.get("createTime", now)
    serviceDeadline = None
    categoryType = dataDict.get("categoryType", 1)  # 1 自营 2 第三方
    serviceName = dataDict.get("serviceName", None)  # 产品服务名称
    servciceProcess = dataDict.get("servciceProcess", None)  # 产品服务流程

    if dataDict.has_key("serviceDeadline"):
        if not dataDict.get("serviceDeadline"):
            dataDict.pop("serviceDeadline")
        else:
            serviceDeadline = dataDict.get("serviceDeadline")
    tempServiceStr = (itemId, servicePrice, serviceStarttime, isSecular, serviceDeadline, directionName, policySource,
                      sheetContent, materialList, forecastPath, isEvaluate, servicePerson, serviceContactPerson,
                      serviceContactPhone, serviceContent, declareList, checkStatus, checkPerson, checkTime,
                      checkRemark, createPerson,
                      createTime, categoryType, serviceName, servciceProcess)
    table = insertToSQL(TempService, *tempServiceStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
    else:
        resultDict = returnMsg({})
    return jsonify(resultDict)


# 获取部门项目  项目顶层分析 项目方向维护 中使用
@app.route("/getAreaCodeDeptItemListRole", methods=["POST"])
@jwt_required
def getAreaCodeDeptItemListRole():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", "")
    deptId = dataDict.get("deptId", "")
    # code = dataDict.get("code", "")
    if not (deptId or roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if deptId:
        # deptItemList = DeptItem.query.filter(DeptItem.dept_id == deptId, DeptItem.code.like("%0000")).all()
        deptItemList = DeptItem.query.filter(DeptItem.dept_id == deptId).all()
        infoList = []
        for deptItem in deptItemList:
            infoList.append(deptItem)
        allLists = getDeptItem(infoList)
        infoList = []
        if not allLists:
            resultDict = returnMsg({})
            return jsonify(resultDict)
        for info in allLists:
            oneInfo = info.get()
            infoList.append(oneInfo)
    else:
        pass
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 分发分析单
@app.route("/assignTempServiceToCounselor", methods=["POST"])
@jwt_required
def assignTempServiceToCounselor():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", None)
    idList = dataDict.get("ids", None)
    servicePerson = dataDict.get("servicePerson", "")
    if not (id and servicePerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if id and not idList:
        idList = [id]
    newDict = {"servicePerson": servicePerson}
    dbOperation = OperationOfDB()

    for id in idList:
        intColumnClinetNameList = [u'id', u'itemId', u'directionName', u'checkStatus', u'isSecular', u'isEvaluate', u'categoryType']
        table = dbOperation.updateThis(TempService, TempService.id, id, newDict, tableChangeDic,
                                       intColumnClinetNameList=intColumnClinetNameList)
        # table = updataById(TempService, newDict, "id", id, tableChangeDic, intColumnClinetNameList=intColumnClinetNameList)
        # updataById(TempService, newDict, "id", id, tableChangeDic, intColumnClinetNameList=intColumnClinetNameList)
        if not table:
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 选择咨询师
@app.route("/choiceCounselor", methods=["POST"])
@jwt_required
def choiceCounselor():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = (u'adminId', u'isLock', u'ozId', u'id', u'roleId', u'userId')
    tableName = "view_role_user"
    condition = dataDict.get("condition")
    newList = [{
        "field": "roleId",
        "op": "equal",
        "value": 5
    }, {
        "field": "isLock",
        "op": "equal",
        "value": 1
    },
    ]
    for newDict in newList:
        condition.append(newDict)
    adminsList, count = conditionDataListFind(dataDict, adminChangeDic, intColumnClinetNameList, tableName)
    if adminsList:
        adminInfoList = []
        for tableData in adminsList:
            if tableData[11] == -1:
                continue
            adminDict = {
                # "id": tableData[0],
                "adminId": tableData[1],
                "adminName": tableData[2],
                # "adminToken": tableData[3],
                # "adminRefreshToken": tableData[4],
                # "adminSalt": tableData[5],
                # "adminPassword": tableData[6],
                "adminDesc": tableData[7],
                "adminRealName": tableData[8],
                "adminTelephone": tableData[9],
                "adminEmail": tableData[10],
                "adminAddTime": tableData[11],
                "isLock": tableData[12],
                "ozId": tableData[13],
                "roleId": tableData[14],
                "rolePid": tableData[15],
                "roleName": tableData[16],
                "roleDesc": tableData[17],
                "isSys": tableData[18],
                "servicePerson": tableData[2],
            }
            adminDict = dictRemoveNone(adminDict)
            adminInfoList.append(adminDict)
        resultDict = returnMsg(adminInfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 删除

newChangeDict = {
    "id": "id",
    "itemId": "item_id",
    "policySource": "policy_source",
    "servicePrice": "service_price",
    "serviceStarttime": "service_starttime",
    "serviceDeadline": "service_deadline",
    "directionName": "direction_name",
    "materialList": "material_list",
    "forecastPath": "forecast_path",
    "checkStatus": "check_status",
    "checkPerson": "check_person",
    "checkTime": "check_time",
    "checkRemark": "check_remark",
    "servicePerson": "service_person",
    "serviceContactPerson": "service_contact_person",
    "serviceContactPhone": "service_contact_phone",
    "createTime": "create_time",
    "isSecular": "is_secular",
    "isEvaluate": "is_evaluate",
    "evaluateQuestions": "evaluate_questions",
    "deptId": "dept_id",
    "itemUrl": "item_url",
    "itemTitle": "item_title",
    "itemImgurl": "item_imgurl",
    "itemPulishdate": "item_pulishdate",
    "itemType": "item_type",
    "itemSort": "item_sort",
    "isTop": "is_top",
    "isLock": "is_lock",
    "isService": "is_service",
    "isContentJson": "is_content_json",
    "areaCode": "area_code",
    "deptName": "dept_name",
    "deptAddress": "dept_address",
    "deptUrl": "dept_url",
    "levelCode": "level_code",
    "materialContent": "material_content",
}

# user user_role
adminChangeDic = {
    "id": "id",
    "adminId": "admin_id",
    "adminName": "admin_name",
    "adminToken": "admin_token",
    "adminRefreshToken": "admin_refresh_token",
    "adminSalt": "admin_salt",
    "adminPassword": "admin_password",
    "adminDesc": "admin_desc",
    "adminRealName": "admin_real_name",
    "adminTelephone": "admin_telephone",
    "adminEmail": "admin_email",
    "adminAddTime": "admin_add_time",
    "isLock": "is_lock",
    "ozId": "oz_id",
    "roleId": "role_id",
    "rolePid": "role_pid",
    "roleName": "role_name",
    "roleDesc": "role_desc",
    "isSys": "is_sys",
}
