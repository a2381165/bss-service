# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import not_

from common.Log import addLog, deleteLog, updateLog, queryLog
from common.OperationOfDB import insertToSQL, findById, conditionDataListFind, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Base.Area import Area  as AreaCode
from models.Data.Category import Category
from models.Data.Department import Department, tableChangeDic
from version.v3.bossConfig import app


# 通过条件 筛选 ok
@app.route("/findDepartmentByCondition", methods=["POST"])
@jwt_required
@queryLog("data_department")
def findDepartmentByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("deptId", "deptPid", "isLock", "categoryId")
    tableName = Department.__tablename__
    deptList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    priviceList = []
    if deptList:
        infoList = []
        for tableData in deptList:
            if tableData.area_code[2:6] == "0000":
                priviceList.append(tableData)
        for s in priviceList:
            x = 0
            deptTableInfo = Department.query.filter(Department.area_code == s.area_code).first()
            provincTableInfo = AreaCode.query.filter(AreaCode.area_code == s.area_code).first()
            if not provincTableInfo:
                continue
            infoDict = {
                "deptId": deptTableInfo.dept_id,
                "deptCode": deptTableInfo.dept_code,
                'deptPid': deptTableInfo.dept_pid,
                'deptName': deptTableInfo.dept_name,
                'deptAddress': deptTableInfo.dept_address,
                'deptUrl': deptTableInfo.dept_url,
                'areaCode': deptTableInfo.area_code,
                "isLock": deptTableInfo.is_lock,
                "categoryId": deptTableInfo.category_id,
                "levelCode": deptTableInfo.level_code,
                "desUrl": deptTableInfo.des_url,
                "id": provincTableInfo.area_id,
                "name": provincTableInfo.area_name,
                "code": provincTableInfo.area_code,
                "pCode": provincTableInfo.p_code,
                "children": []
            }
            infoList.append(infoDict)
            cityTableList = Department.query.filter(Department.area_code.like("{}%00".format(s.area_code[:2])),
                                                    not_(Department.area_code == s.area_code)).all()
            if not cityTableList:
                continue
            for c in cityTableList:
                deptTableInfo = Department.query.filter(Department.area_code == c.area_code).first()
                cityTableInfo = AreaCode.query.filter(AreaCode.area_code == c.area_code).first()
                cityDict = {
                    "deptId": deptTableInfo.dept_id,
                    "deptCode": deptTableInfo.dept_code,
                    'deptPid': deptTableInfo.dept_pid,
                    'deptName': deptTableInfo.dept_name,
                    'deptAddress': deptTableInfo.dept_address,
                    'deptUrl': deptTableInfo.dept_url,
                    'areaCode': deptTableInfo.area_code,
                    "isLock": deptTableInfo.is_lock,
                    "categoryId": deptTableInfo.category_id,
                    "levelCode": deptTableInfo.level_code,
                    "desUrl": deptTableInfo.des_url,
                    "id": cityTableInfo.area_id,
                    "name": cityTableInfo.area_name,
                    "code": cityTableInfo.area_code,
                    "pCode": cityTableInfo.p_code,
                    "children": []
                }
                areaCodeTableList = Department.query.filter(
                    Department.area_code.like("{}%".format(cityTableInfo.area_code[:4])),
                    not_(Department.area_code == cityTableInfo.area_code)).all()
                infoDict["children"].append(cityDict)
                infoList.remove(infoDict)
                infoList.append(infoDict)
                if areaCodeTableList:
                    for areaCodeTable in areaCodeTableList:
                        # districtTable = Department.query.filter(areaCodeTable.area_code == Department.area_code).first()
                        districtTable = AreaCode.query.filter(AreaCode.area_code == areaCodeTable.area_code).first()
                        deptTableInfo = Department.query.filter(Department.area_code == c.area_code).first()
                        if districtTable:
                            disDict = {
                                "deptId": deptTableInfo.dept_id,
                                "deptCode": deptTableInfo.dept_code,
                                'deptPid': deptTableInfo.dept_pid,
                                'deptName': deptTableInfo.dept_name,
                                'deptAddress': deptTableInfo.dept_address,
                                'deptUrl': deptTableInfo.dept_url,
                                'areaCode': deptTableInfo.area_code,
                                "isLock": deptTableInfo.is_lock,
                                "categoryId": deptTableInfo.category_id,
                                "levelCode": deptTableInfo.level_code,
                                # "desUrl": deptTableInfo.des_url,
                                "id": districtTable.area_id,
                                "name": districtTable.area_name,
                                "code": districtTable.area_code,
                                "pCode": districtTable.p_code,
                            }
                            infoDict["children"][x]["children"].append(disDict)
                            infoList.remove(infoDict)
                            infoList.append(infoDict)

                        else:
                            continue
                else:
                    continue
            x += 1
        resultDict = returnMsg(infoList)
        count = Department.query.all()
        resultDict["total"] = len(count)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 更新 ok
@app.route("/updateDepartment", methods=["POST"])
@jwt_required
@updateLog("data_department")
def updateDepartmentById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "dept_id"
    intColumnClinetNameList = ("deptId", "deptPid", "isLock", "categoryId")

    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    for id in idList:
        deptUp = updataById(Department, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if deptUp == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif deptUp == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        else:
            InfoDic = tableDictSort(deptUp)
        infoList.append(InfoDic)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 删除
@app.route("/deleteDepartment", methods=["POST"])
@jwt_required
@deleteLog("data_department")
def delDepartment():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.deleteByIdBoss(Department, id, "dept_id")
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("delete fail")
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("delete fail")
    return jsonify(resultDict)


# 通过条件 筛选视图 ok
@app.route("/findViewDeptByCondition", methods=["POST"])
@jwt_required
@queryLog("data_department")
def findViewDeptByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition') == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("deptId", "deptPid", "isLock", "categoryId","levelCode")
    viewChangeDict = tableChangeDic
    deptList, count = conditionDataListFind(dataDict, viewChangeDict, intColumnClinetNameList, Department.__tablename__)
    if deptList:

        InfoList = []
        for tableData in deptList:
            try:
                table = Category.query.filter(Category.category_id == tableData[9]).first()
                categoryName = table.category_name
            except:
                categoryName = None
            areaCode = tableData[8]
            areaTable = AreaCode.query.filter(AreaCode.area_code == areaCode).first()
            if areaTable:
                p_code = areaTable.p_code
            else:
                p_code = None
            provinceName, cityName, districtName = getAreaCode(areaCode)
            infoDict = {
                "deptId": tableData[0],
                'deptCode': tableData[1],
                'deptPid': tableData[2],
                'deptName': tableData[3],
                'deptAddress': tableData[4],
                'deptUrl': tableData[5],
                'isLock': tableData[6],
                'levelCode': tableData[7],
                'areaCode': tableData[8],
                'categoryId': tableData[9],
                'pCode': p_code,
                'districtName': districtName,
                'provinceName': provinceName,
                'cityName': cityName,
                'categoryName': categoryName,
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 查看详情
@app.route("/findDepartmentById", methods=["POST"])
@jwt_required
@queryLog("data_department")
def findDepartmentById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('deptId', None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    deptTable = findById(Department, "dept_id", id)
    if deptTable:
        infoDict = tableDictSort(deptTable)
        resultDict = returnMsg(infoDict)
    elif deptTable == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 添加 ok
@app.route("/addDepartment", methods=["POST"])
@jwt_required
@addLog("data_department")
def addDepartment():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnsStr = (dataDict.get("deptCode", None),
                  dataDict.get("deptPid", None),
                  dataDict.get("deptName", None),
                  dataDict.get("deptAddress", None),
                  dataDict.get("deptUrl", None),
                  dataDict.get("areaCode", None),
                  dataDict.get("isLock", None),
                  dataDict.get("categoryId", None),
                  dataDict.get("levelCode", None))
    deptTable = insertToSQL(Department, *columnsStr)
    if deptTable:
        infoDict = tableDictSort(deptTable)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def tableDictSort(table):
    infoDict = {
        "deptId": table.dept_id,
        "deptCode": table.dept_code,
        'deptPid': table.dept_pid,
        'deptName': table.dept_name,
        'deptAddress': table.dept_address,
        'deptUrl': table.dept_url,
        'areaCode': table.area_code,
        "isLock": table.is_lock,
        "categoryId": table.category_id,
        "levelCode": table.level_code,
    }
    return infoDict


def getAreaCode(areaCode):
    provinceName = None
    cityName = None
    districtName = None
    try:
        areaCode = areaCode
        if areaCode:
            if areaCode[:2] != "00":
                newAreaCode = "{}0000".format(areaCode[:2])
                areaCodetable = AreaCode.query.filter(AreaCode.area_code == newAreaCode).first()
                if areaCodetable:
                    provinceName = areaCodetable.area_name
            if areaCode[2:4] != "00":
                newAreaCode = "{}00".format(areaCode[:4])
                areaCodetable = AreaCode.query.filter(AreaCode.area_code == newAreaCode).first()
                if areaCodetable:
                    cityName = areaCodetable.area_name
            if areaCode[4:6] != "00":
                newAreaCode = "{}".format(areaCode)
                areaCodetable = AreaCode.query.filter(AreaCode.area_code == newAreaCode).first()
                if areaCodetable:
                    districtName = areaCodetable.area_name
        return provinceName, cityName, districtName
    except:
        return provinceName, cityName, districtName
