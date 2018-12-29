# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required

from common.AreaCodeGrading import set_menus
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.DeptItemGrading import getDeptItem
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, executeSql
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Boss.AreaSet import AreaSet as DataAreaSet
from models.Boss.DeptItem import DeptItem, tableChangeDic
from models.Data.Department import Department, tableChangeDic as deptChangeDict
from version.v3.bossConfig import app


# 获取部门项目  项目顶层分析 项目方向维护 中使用
@app.route("/getAreaCodeDeptItemList", methods=["POST"])
def getAreaCodeDeptItemList():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    deptId = dataDict.get("deptId", "")
    # code = dataDict.get("code", "")
    if not deptId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # deptItemList = DeptItem.query.filter(DeptItem.dept_id == deptId, DeptItem.code.like("%0000")).all()
    deptItemList = DeptItem.query.filter(DeptItem.dept_id == deptId).all()
    infoList = []
    for deptItem in deptItemList:
        infoList.append(deptItem)
    allLists = getDeptItem(infoList)
    infoList = []
    if not allLists:
        resultDict = returnMsg([])
        return jsonify(resultDict)
    for info in allLists:
        oneInfo = info.get()
        infoList.append(oneInfo)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 项目方向分析 获取区域 # 根据区域启动来筛选 # 只显示省市
@app.route("/getDeptItemList", methods=["POST"])
@jwt_required
@queryLog('boss_dept_item')
def getDeptItemList():
    sqlStr = """SELECT distinct t2.area_code, t2.area_name,t2.p_code from data_area as t JOIN base_area as t2 ON t.area_code=t2.area_code and t.area_code like '%00' and t.area_status = 1 """
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


# 树形 区域  勾选
@app.route("/getDeptItemListCheck", methods=["POST"])
@jwt_required
@queryLog('boss_dept_item')
def getDeptItemListCheck():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = DataAreaSet.__tablename__
    intColumnClinetNameList = [u'id', u'dataAreaId', u'userId', "ozId"]
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    InfoList = []
    if tableList:
        for tableData in tableList:
            InfoList.append(tableData)
    sqlStr = """SELECT distinct t2.area_code, t2.area_name,t2.p_code from data_area as t JOIN base_area as t2  ON t.area_code=t2.area_code and t.area_code like '%00' and t.area_status = 1 """
    areaCodeList = executeSql(sqlStr)
    infoList = []
    if areaCodeList:
        tableList = []
        for result in areaCodeList:
            tableList.append(result)
        allLists = set_menus("00", tableList, InfoList)
        infoList = []
        if not allLists:
            resultDict = returnMsg([])
            return jsonify(resultDict)
        for info in allLists:
            oneInfo = info.get()
            infoList.append(oneInfo)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 获取部门
@app.route("/getAreaCodeToDept", methods=["POST"])
@jwt_required
@queryLog('boss_dept_item')
def getAreaCodeToDept():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    areaCode = dataDict.get("areaCode", "")
    if not areaCode:
        deptList = Department.query.all()
    else:
        if areaCode[2:4] != "00":
            deptList = Department.query.filter(Department.area_code.like("{}%".format(areaCode[:4]))).all()
        else:
            deptList = Department.query.filter(Department.area_code == areaCode).all()
    infoList = []
    for table in deptList:
        infoDict = {
            "deptId": table.dept_id,
            "deptCode": table.dept_code,
            "deptPid": table.dept_pid,
            "deptName": table.dept_name,
            "deptAddress": table.dept_address,
            "deptUrl": table.dept_url,
            "isLock": table.is_lock,
            "levelCode": table.level_code,
            "areaCode": table.area_code,
            "categoryId": table.category_id,
        }
        infoDict = dictRemoveNone(infoDict)
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 通过条件筛选部门
@app.route("/getDeptByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_dept_item')
def getDeptByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    if condition != []:
        for field in condition:
            if field.get("field") == "areaCode":
                areaCode = field.get("value")
                if areaCode[2:4] != "00":
                    field["op"] = "like"
                    field["value"] = "{}%".format(areaCode[:4])
    tablename = Department.__tablename__
    intColumnClinetNameList = [u'deptId', u'deptPid', u'isLock', u'categoryId']
    tableList, count = conditionDataListFind(dataDict, deptChangeDict, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for table in tableList:
            infoDict = {"deptId": table.dept_id,
                        "deptCode": table.dept_code,
                        "deptPid": table.dept_pid,
                        "deptName": table.dept_name,
                        "deptAddress": table.dept_address,
                        "deptUrl": table.dept_url,
                        "isLock": table.is_lock,
                        "levelCode": table.level_code,
                        "areaCode": table.area_code,
                        "categoryId": table.category_id,
                        "pcode": "000000"}
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取 列表
@app.route("/findDeptItemByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_dept_item')
def findDeptItemBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = DeptItem.__tablename__
    intColumnClinetNameList = [u'id', u'deptId', u'isLock']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "deptId": tableData[1],
                        "type": tableData[2],
                        "name": tableData[3],
                        "code": tableData[4],
                        "pcode": tableData[5],
                        "remark": tableData[6],
                        "isLock": tableData[7],
                        "createTime": tableData[8], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getDeptItemDetail", methods=["POST"])
@jwt_required
@queryLog('boss_dept_item')
def getDeptItemDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(DeptItem, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "deptId": table.dept_id,
                "type": table.type,
                "name": table.name,
                "code": table.code,
                "pcode": table.pcode,
                "remark": table.remark,
                "isLock": table.is_lock,
                "createTime": table.create_time, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteDeptItem", methods=["POST"])
@jwt_required
@deleteLog('boss_dept_item')
def deleteDeptItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("ids", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in ids:
        table = findById(DeptItem, "id", id)
        code = table.code
        deptItemList = DeptItem.query.filter(DeptItem.pcode == code).first()
        if deptItemList:
            resultDict = returnErrorMsg(errorCode["dept_item_has_son"])
            return jsonify(resultDict)

    table = deleteById(DeptItem, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addDeptItem", methods=["POST"])
@jwt_required
@addLog('boss_dept_item')
def addDeptItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    now = getTimeStrfTimeStampNow()  # create_time
    deptId = dataDict.get("deptId", "")
    name = dataDict.get("name", "")
    pcode = dataDict.get("pcode", "")
    remark = dataDict.get("remark", "")
    isLock = dataDict.get("isLock", None)
    if not (deptId and name and pcode and isLock != None):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    deptItem = DeptItem.query.filter(DeptItem.pcode == pcode, DeptItem.dept_id == deptId).order_by(
        DeptItem.create_time.desc()).first()
    if len(pcode) != 6:
        resultDict = returnErrorMsg("pcode must has six ")
        return jsonify(resultDict)
    if pcode == "000000":
        type = 1
        if deptItem:
            code = str(int(deptItem.code) + 10000).zfill(6)
        else:
            code = "010000"
    elif pcode[:2] != "00" and pcode[2:6] == "0000":
        type = 2
        if deptItem:
            code = str(int(deptItem.code) + 100).zfill(6)
        else:
            code = pcode[:2] + "0100"
    elif pcode[2:4] != "00" and pcode[4:6] == "00":
        type = 3
        if deptItem:
            code = str(int(deptItem.code) + 1).zfill(6)
        else:
            code = pcode[:4] + "01"
    else:
        resultDict = returnErrorMsg("pcode not matching")
        return jsonify(resultDict)
    columsStr = (deptId, type, name, code, pcode, remark, isLock, now)
    table = insertToSQL(DeptItem, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataDeptItem", methods=["POST"])
@jwt_required
@updateLog('boss_dept_item')
def updataDeptItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'deptId', u'isLock']
    table = updataById(DeptItem, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
