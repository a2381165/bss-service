# -*- coding: utf-8 -*-
import Res
import json

from flask import request, json, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required,current_user
from sqlalchemy import not_

from DataSourceApi import getAreaCode
from common.Log import queryLog, addLog, updateLog, deleteLog
from common.OperationOfDB import deleteById, updataById, conditionDataListFind, deleteByIdBoss, findById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Base.Area import Area as AreaCode
from models.Boss.Area import Area as AreaStatus, tableChangeDic
from models.Boss.AreaSet import AreaSet
from models.Boss.Role import Role
from version.v3.bossConfig import app


# 查看区域列表
@app.route("/findAreaStatusAddrList", methods=["POST"])
@jwt_required
@queryLog("boss_area")
def findAreaStatusAddrList():
    if not request.json:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    addrList = dataDict.get("addrList", [])
    open_city_dict = {}
    infoDict = {}

    areaStatusTableList = AreaStatus.query.filter(AreaStatus.area_status == 1).all()
    for areaStatusTable in areaStatusTableList:
        open_city_dict[areaStatusTable.area_code] = areaStatusTable.id
    if len(addrList) == 0:
        areaCodeTableList = AreaCode.query.filter(AreaCode.area_code.like("%0000")).all()
        if areaCodeTableList:
            for areaCodeTable in areaCodeTableList:
                areaID = areaCodeTable.area_code
                if areaID not in open_city_dict.keys():
                    continue
                infoDict = {
                    "areaId": areaCodeTable.area_id,
                    "areaName": areaCodeTable.area_name,
                    "areaCode": areaCodeTable.area_code,
                }
                infoList.append(infoDict)
            resultDict = returnMsg(infoList)
        else:
            resultDict = returnErrorMsg(errorCode["param_error"])
    elif len(addrList) == 1:
        provincTableInfo = AreaCode.query.filter(AreaCode.area_code == "{}0000".format(addrList[0][:2])).first()
        cityTableInfo = AreaCode.query.filter(AreaCode.area_code == "{}00".format(addrList[0][:4])).first()

        if addrList[0][2:4] == "00":
            areaCodeTableList = AreaCode.query.filter(AreaCode.area_code.like("{}%00".format(addrList[0][:2])),
                                                      not_(AreaCode.area_code == addrList[0])).all()
            if areaCodeTableList:
                for areaCodeTable in areaCodeTableList:
                    cityTable = AreaCode.query.filter(areaCodeTable.area_code == AreaCode.area_code).first()
                    if cityTable:
                        if cityTable.area_code not in open_city_dict.keys():
                            continue
                        infoDict = {
                            "provinceId": provincTableInfo.area_id,
                            "provinceName": provincTableInfo.area_name,
                            "provinceCode": provincTableInfo.area_code,
                            "cityId": cityTable.area_id,
                            "cityName": cityTable.area_name,
                            "cityCode": cityTable.area_code,
                        }
                        infoList.append(infoDict)
                    else:
                        resultDict = returnErrorMsg(errorCode["param_error"])
                        return jsonify(resultDict)
                resultDict = returnMsg(infoList)
            else:
                resultDict = returnErrorMsg(errorCode["param_error"])
        elif addrList[0][4:6] == "00":
            areaCodeTableList = AreaCode.query.filter(AreaCode.area_code.like("{}%".format(addrList[0][:4])),
                                                      not_(AreaCode.area_code == addrList[0])).all()
            if areaCodeTableList:
                for areaCodeTable in areaCodeTableList:
                    districtTable = AreaCode.query.filter(areaCodeTable.area_code == AreaCode.area_code).first()
                    if districtTable:
                        if districtTable.area_code not in open_city_dict.keys():
                            continue
                        infoDict = {
                            "provinceId": provincTableInfo.area_id,
                            "provinceName": provincTableInfo.area_name,
                            "provinceCode": provincTableInfo.area_code,
                            "cityId": cityTableInfo.area_id,
                            "cityName": cityTableInfo.area_name,
                            "cityCode": cityTableInfo.area_code,
                            "districtId": districtTable.area_id,
                            "districtName": districtTable.area_name,
                            "districtCode": districtTable.area_code,
                        }
                        infoList.append(infoDict)
                    else:
                        resultDict = returnErrorMsg(errorCode["param_error"])
                        return jsonify(resultDict)
                resultDict = returnMsg(infoList)
            else:
                resultDict = returnErrorMsg(errorCode["param_error"])
        else:
            areaCodeTableList = AreaCode.query.filter(AreaCode.area_code == addrList[0]).first()
            if areaCodeTableList:
                infoDict = {
                    "districtId": areaCodeTableList.area_id,
                    "districtName": areaCodeTableList.area_name,
                    "districtCode": areaCodeTableList.area_code,
                }
                resultDict = returnMsg(infoDict)
            else:
                resultDict = returnErrorMsg(errorCode["param_error"])
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])

    return jsonify(resultDict)


# 更新区域状态
@app.route("/updateAreaStatus", methods=["POST"])
@jwt_required
@updateLog("boss_area")
def updateAreaStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "id"
    intColumnClinetNameList = ("id", "areaStatus")
    infoList = []
    idList = dataDict.get("ids")
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in idList:
        table = updataById(AreaStatus, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if table == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif table == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        else:
            infoDic = tableDictSort(table)
            infoList.append(infoDic)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)



# 通过条件 筛选
@app.route("/findAreaStatusByCondition", methods=["POST"])
@jwt_required
@queryLog("boss_area")
def findAreaStatusByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("id", "areaStatus", "Id")
    className = AreaStatus.__tablename__
    # sqlStr = "SELECT * FROM {} WHERE area_code like '%00' WHERE ".format("data_area")
    orderByStr = " order by area_code desc "
    adminsList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, className,orderByStr=orderByStr)
    if adminsList:
        InfoList = []
        for tableData in adminsList:
            areaInfo = AreaCode.query.filter(AreaCode.area_code == tableData[1]).first()
            if areaInfo:
                areaName = areaInfo.area_name
            else:
                areaName = ""
            infoDict = {
                "Id": tableData[0],
                'areaCode': tableData[1],
                'areaStatus': tableData[2],
                'areaName': areaName,
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 删除
@app.route("/deleteAreaStatus", methods=["POST"])
@jwt_required
@deleteLog("boss_area")
def deleteAreaStatusByIds():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    idList = dataDict.get("idArray", [])
    if len(idList) < 1:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for areaCode in idList:
        areaStatusTableSub = False
        if areaCode[2:4] == "00":
            areaStatusTableSub = AreaStatus.query.filter(
                AreaStatus.area_code.like("{}%00".format(areaCode[:2])),
                not_(AreaStatus.area_code == areaCode)).all()
            if not areaStatusTableSub:
                infoList.append(areaCode)
        elif areaCode[4:6] == "00":
            areaStatusTableSub = AreaStatus.query.filter(
                AreaStatus.area_code.like("{}%".format(areaCode[:4])),
                not_(AreaStatus.area_code == areaCode)).all()
            if not areaStatusTableSub:
                infoList.append(areaCode)
        else:
            infoList.append(areaCode)
        if areaStatusTableSub:
            resultDict = returnErrorMsg("can not delete")
            return jsonify(resultDict)
    if not infoList:
        resultDict = returnErrorMsg("can not delete")
        return jsonify(resultDict)
    else:
        for areaCode in infoList:
            table = findById(AreaStatus, "area_code", areaCode, isStrcheck=True)
            if table:
                setTable = AreaSet.query.filter(AreaSet.area_code == table.area_code).first()
                if setTable:
                    resultDict = returnErrorMsg(errorCode["area_set_people"])
                    # resultDict = returnErrorMsg("this areaCode has penple")
                    return jsonify(resultDict)
    count = deleteByIdBoss(AreaStatus, infoList, "area_code", isInt=False)
    if len(infoList) == count:
        resultDict = returnMsg({"count": count})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 强制联合删除
@app.route("/forceDeleteAreaStatus", methods=["POST"])
@jwt_required
@deleteLog("boss_area")
def forceDeleteAreaStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    if len(idList) < 1:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # 强制删除
    for id in idList:
        areaStatusTable = AreaStatus.query.filter(AreaStatus.id == id).first()
        if areaStatusTable:
            areaList = []
            areaList.append(areaStatusTable)
            areaIdList = []

            def areaCode_make_tree(list):
                for areaCodeInfo in list:
                    if areaCodeInfo.area_code[2:4] == "00":
                        areaCodeList = AreaStatus.query.filter(
                            AreaStatus.area_code.like("{}%00".format(areaCodeInfo.area_code[:2])),
                            not_(AreaStatus.area_code == areaCodeInfo.area_code)).all()
                        if areaCodeList:
                            areaCode_make_tree(areaCodeList)
                        areaIdList.append(areaCodeInfo.id)
                    elif areaCodeInfo.area_code[4:6] == "00":
                        areaCodeList = AreaStatus.query.filter(
                            AreaStatus.area_code.like("{}%".format(areaCodeInfo.area_code[:4])),
                            not_(AreaStatus.area_code == areaCodeInfo.area_code)).all()
                        if areaCodeList:
                            areaCode_make_tree(areaCodeList)
                        areaIdList.append(areaCodeInfo.id)
                    else:
                        areaIdList.append(areaCodeInfo.id)
                return areaIdList

            areaIdList = areaCode_make_tree(areaList)
            resultDict = deleteById(AreaStatus, areaIdList, "id")
        else:
            resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 查看详情
@app.route("/findAreaStatusById", methods=["POST"])
@jwt_required
@queryLog("boss_area")
def findAreaStatusById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('Id')
    areaCode = dataDict.get("areaCode", None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    adminRoleTable = AreaStatus.query.filter(AreaStatus.id == id).first()
    if adminRoleTable:
        infoDict = tableDictSort(adminRoleTable)
        resultDict = returnMsg(infoDict)
    elif adminRoleTable == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 添加
@app.route("/addAreaStatus", methods=["POST"])
@jwt_required
@addLog("boss_area")
def addAreaStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    areaCodeList = dataDict.get("areaCodeList")
    if areaCodeList == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for areaCode in areaCodeList:
        areaStatuTable = AreaStatus.query.filter(AreaStatus.area_code == areaCode).first()
        if areaStatuTable:
            if areaStatuTable.area_status == 1:
                continue
            areaStatuTable.area_status = 1
            if not dbOperation.addTokenToSql(areaStatuTable):
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("update area status failed")
                return jsonify(resultDict)
        else:
            columnsStr = (areaCode, 1)
            if not dbOperation.insertToSQL(AreaStatus, *columnsStr):
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("add area status failed")
                return jsonify(resultDict)
    if not dbOperation.commitToSQL():
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("commit failed")
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 查看列表 并进行筛选
@app.route("/findAreaAddrList", methods=["POST"])
@jwt_required
@queryLog("boss_area")
def findAreaAddrList():
    if not request.json:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    addrList = dataDict.get("addrList", [])
    aeraStatusList = AreaStatus.query.all()
    Statuslist = []
    for x in aeraStatusList:
        Statuslist.append(x.area_code)
    if len(addrList) == 0:
        areaCodeTableList = AreaCode.query.filter(AreaCode.area_code.like("%0000"),
                                                  not_(AreaCode.area_code.in_(Statuslist))).all()
        if areaCodeTableList:
            for areaCodeTable in areaCodeTableList:
                infoDict = {
                    "areaId": areaCodeTable.area_id,
                    "areaName": areaCodeTable.area_name,
                    "areaCode": areaCodeTable.area_code,
                }
                infoList.append(infoDict)
            resultDict = returnMsg(infoList)
            resultDict["total"] = len(infoList)

        else:
            resultDict = returnErrorMsg(errorCode["param_error"])
    elif len(addrList) == 1:
        provincTableInfo = AreaCode.query.filter(AreaCode.area_code == "{}0000".format(addrList[0][:2])).first()
        cityTableInfo = AreaCode.query.filter(AreaCode.area_code == "{}00".format(addrList[0][:4])).first()
        if addrList[0][2:4] == "00":
            areaCodeTableList = AreaCode.query.filter(AreaCode.area_code.like("{}%00".format(addrList[0][:2])),
                                                      not_(AreaCode.area_code == addrList[0]),
                                                      not_(AreaCode.area_code.in_(Statuslist))).all()
            if areaCodeTableList:
                for areaCodeTable in areaCodeTableList:
                    cityTable = AreaCode.query.filter(areaCodeTable.area_code == AreaCode.area_code).first()
                    if cityTable:
                        infoDict = {
                            "provinceId": provincTableInfo.area_id,
                            "provinceName": provincTableInfo.area_name,
                            "provinceCode": provincTableInfo.area_code,
                            "cityId": cityTable.area_id,
                            "cityName": cityTable.area_name,
                            "cityCode": cityTable.area_code,
                        }
                        infoList.append(infoDict)
                    else:
                        resultDict = returnErrorMsg(errorCode["param_error"])
                        return jsonify(resultDict)
                    resultDict = returnMsg(infoList)
                    resultDict["total"] = len(infoList)
            else:
                resultDict = returnErrorMsg([])
        elif addrList[0][4:6] == "00":
            Statuslist.append(addrList[0])
            areaCodeTableList = AreaCode.query.filter(AreaCode.area_code.like("{}%".format(addrList[0][:4])),
                                                      AreaCode.area_code.notin_(Statuslist)).all()
            if areaCodeTableList:
                for areaCodeTable in areaCodeTableList:
                    districtTable = AreaCode.query.filter(areaCodeTable.area_code == AreaCode.area_code).first()
                    if districtTable:
                        infoDict = {
                            "provinceId": provincTableInfo.area_id,
                            "provinceName": provincTableInfo.area_name,
                            "provinceCode": provincTableInfo.area_code,
                            "cityId": cityTableInfo.area_id,
                            "cityName": cityTableInfo.area_name,
                            "cityCode": cityTableInfo.area_code,
                            "districtId": districtTable.area_id,
                            "districtName": districtTable.area_name,
                            "districtCode": districtTable.area_code,
                        }
                        infoList.append(infoDict)
                    else:
                        resultDict = returnErrorMsg(errorCode["param_error"])
                        return jsonify(resultDict)
                    resultDict = returnMsg(infoList)
                    resultDict["total"] = len(infoList)

            else:
                resultDict = returnErrorMsg([])
        else:
            areaCodeTableList = AreaCode.query.filter(AreaCode.area_code == addrList[0]).first()
            if areaCodeTableList:
                infoDict = {
                    "districtId": areaCodeTableList.area_id,
                    "districtName": areaCodeTableList.area_name,
                    "districtCode": areaCodeTableList.area_code,
                }
                resultDict = returnMsg(infoDict)
                resultDict["total"] = len(infoList)
            else:
                resultDict = returnErrorMsg([])
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)

#  平铺 区域
# 数据维护  筛选池 获取自己的区域 # 同时根据部门来
@app.route("/getOwnArea", methods=["POST"])
@jwt_required
@queryLog("boss_area")
def getOwnArea():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not roleId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # 如果部长 全部
    if str(roleId) in (Res.all_role["jsbbz"],Res.all_role["zxbbz"]):
        areaList = AreaStatus.query.filter( AreaStatus.area_status == 1,AreaStatus.area_code.like("%00")).all()
    else:
        role = Role.query.filter(Role.role_id == roleId).first()
        if role:
            ozId = role.oz_id
        else:
            ozId = ""
        if not ozId:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)

        adminId = get_jwt_identity()
        userAreaSet = AreaSet.query.filter(AreaSet.user_id == adminId, AreaSet.oz_id == ozId).all()
        dataAeraList = [areaSet.area_code for areaSet in userAreaSet]
        areaList = AreaStatus.query.filter(AreaStatus.area_code.in_(dataAeraList), AreaStatus.area_status == 1).all()
    infoList = []
    for area in areaList:
        provinceName, cityName, districtName = getAreaCode(area.area_code)
        areaName = provinceName + cityName + districtName
        infoDict = {
            "id": area.id,
            'areaCode': area.area_code,
            'areaStatus': area.area_status,
            'areaName': areaName,
        }
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


def tableDictSort(table):
    tableDict = {
        "Id": table.id,
        # "areaType": table.area_type,
        'areaCode': table.area_code,
        'areaStatus': table.area_status,
        # "areaPid": table.area_pid
    }
    return tableDict
