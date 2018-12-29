# coding:utf-8
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import not_

import Res
from common.Log import queryLog, addLog, updateLog, deleteLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind, updataById
from common.ReturnMessage import returnMsg, errorCode, returnErrorMsg
from models.Base.Area import Area, tableChangeDic
from version.v3.bossConfig import app


# 查看列表
@app.route("/findAddrList", methods=["POST"])
@jwt_required
@queryLog("base_area")
def findAddrList():
    if not request.json:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    addrList = dataDict.get("addrList", [])

    if len(addrList) == 0:
        areaCodeTableList = Area.query.filter(Area.area_code.like("%0000")).all()
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
        provincTableInfo = Area.query.filter(Area.area_code == "{}0000".format(addrList[0][:2])).first()
        cityTableInfo = Area.query.filter(Area.area_code == "{}00".format(addrList[0][:4])).first()
        if addrList[0][2:4] == "00":
            if str(addrList[0]) == "100000":
                resultDict = returnMsg({})
                return jsonify(resultDict)
            areaCodeTableList = Area.query.filter(Area.area_code.like("{}%00".format(addrList[0][:2])),
                                                  not_(Area.area_code == addrList[0])).all()
            if areaCodeTableList:
                for areaCodeTable in areaCodeTableList:
                    cityTable = Area.query.filter(areaCodeTable.area_code == Area.area_code).first()
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
                resultDict = returnErrorMsg(errorCode["param_error"])
        elif addrList[0][4:6] == "00":
            areaCodeTableList = Area.query.filter(Area.area_code.like("{}%".format(addrList[0][:4])),
                                                  not_(Area.area_code == addrList[0])).all()
            if areaCodeTableList:
                for areaCodeTable in areaCodeTableList:
                    districtTable = Area.query.filter(areaCodeTable.area_code == Area.area_code).first()
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
                resultDict = returnErrorMsg(errorCode["param_error"])
        else:
            areaCodeTableList = Area.query.filter(Area.area_code == addrList[0]).first()
            if areaCodeTableList:
                infoDict = {
                    "districtId": areaCodeTableList.area_id,
                    "districtName": areaCodeTableList.area_name,
                    "districtCode": areaCodeTableList.area_code,
                }
                resultDict = returnMsg(infoDict)
                resultDict["total"] = len(infoList)
            else:
                resultDict = returnErrorMsg(errorCode["param_error"])
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 更新
@app.route("/updateAreaCode", methods=["POST"])
@jwt_required
@updateLog("base_area")
def updateAreaCode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "area_id"
    intColumnClinetNameList = ["areaId"]
    infoList = []
    idList = dataDict.get("ids", None)
    areaStatus = dataDict.get("areaStatus", None)
    areaCode = dataDict.get('areaCode', None)
    if not (idList and areaStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    for id in idList:
        menup = findById(Area, "area_id", id)
        if not menup:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        if Area == None:
            areaCode = menup.area_code

        dataDict.pop("areaStatus")
        if areaStatus == Res.addAreaCode["province"] and areaCode[2:6] == "0000":
            table = updataById(Area, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        elif areaStatus == Res.addAreaCode["city"] and areaCode[2:4] != "00" and areaCode[4:6] == "00":
            table = updataById(Area, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        elif areaStatus == Res.addAreaCode["district"] and areaCode[4:6] != "00":
            table = updataById(Area, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        else:
            resultDict = returnErrorMsg(errorCode["area_code_no_matching"])
            return jsonify(resultDict)

        if table == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif table == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        else:
            infoDict = tableDictSort(table)
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 删除
@app.route("/deleteAreaCode", methods=["POST"])
@jwt_required
@deleteLog("base_area")
def deleteAreaCode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    idListOk = []

    areaStatus = dataDict.get("areaStatus", None)
    if not (idList and areaStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    for id in idList:
        if areaStatus == Res.addAreaCode["province"] and id[2:6] == "0000":
            idListOk.append(id)
        elif areaStatus == Res.addAreaCode["city"] and id[2:4] != "00" and id[4:6] == "00":
            idListOk.append(id)
        elif areaStatus == Res.addAreaCode["district"] and id[4:6] != "00":
            idListOk.append(id)
        else:
            resultDict = returnErrorMsg(errorCode["area_code_no_matching"])
            return jsonify(resultDict)

    if len(idListOk) == 0:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    resultDict = deleteById(Area, idListOk, "area_code", isInt=False)
    return jsonify(resultDict)


# 传入父area_code 查询子类
# 通过条件筛选
@app.route("/findAreaCodeByCondition", methods=["POST"])
@jwt_required
@queryLog("base_area")
def findAreaCodeByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("areaId")
    tableName = Area.__tablename__
    conditionList = dataDict.get('condition', None)

    if len(conditionList) == 0:
        conditionList.append({})
        conditionList[0]["field"] = "pCode"
        conditionList[0]["op"] = "equal"
        conditionList[0]["value"] = "00"
        tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    else:
        tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)

    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {
                "areaId": tableData[0],
                'areaName': tableData[1],
                'areaCode': tableData[2],
                'areaZip': tableData[3],
                'pCode': tableData[4]
            }
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 查看详情
@app.route("/findDistrictById", methods=["POST"])
@jwt_required
@queryLog("base_area")
def findDistrictById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('AreaId', None)
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(Area, "area_id", id)
    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    elif table == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 添加
@app.route("/addAreaCode", methods=["POST"])
@jwt_required
@addLog("base_area")
def addAreaCode():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)

    areaCode = dataDict.get('areaCode', None)
    areaStatus = dataDict.get("areaStatus", None)
    areaName = dataDict.get("areaName", None)
    pCode = dataDict.get("pCode", None)
    areaZip = dataDict.get('areaZip', None)
    if areaStatus == Res.addAreaCode["province"]:
        pCode = "00"
    if not (areaCode and areaStatus and areaName and pCode and len(areaCode) == 6):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    hasAreaTable = Area.query.filter(Area.area_code == areaCode).first()
    if hasAreaTable:
        resultDict = returnErrorMsg(errorCode["area_code_exist"])
        return jsonify(resultDict)
    if areaStatus == Res.addAreaCode["province"] and areaCode[2:6] == "0000":
        columnsStr = (areaName, areaCode, areaZip, pCode)
        table = insertToSQL(Area, *columnsStr)
    elif areaStatus == Res.addAreaCode["city"] and areaCode[4:6] == "00" and areaCode[2:4] != "00":
        columnsStr = (areaName, areaCode, areaZip, pCode)
        table = insertToSQL(Area, *columnsStr)
    elif areaStatus == Res.addAreaCode["district"] and areaCode[4:6] != "00":
        columnsStr = (areaName, areaCode, areaZip, pCode)
        table = insertToSQL(Area, *columnsStr)
    else:
        resultDict = returnErrorMsg(errorCode["area_code_no_matching"])
        return jsonify(resultDict)

    if table:
        infoDict = tableDictSort(table)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 脚本导入areaCode
@app.route("/addAreaCodeAll", methods=["POST"])
@jwt_required
@addLog("base_area")
def addAreaCodeAll():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)

    cityList = dataDict.get("sub")
    for citys in cityList:
        # citys = citysx["sub"][0]
        columnsStr = (
            citys.get('name', None), citys.get('code', None), citys.get('areaZip', None), citys.get("pCode", "000000"))
        table = insertToSQL(Area, *columnsStr)
        for city in citys["sub"]:
            # x = ["110000","120000","310000","500000"]
            # if citys.get("code") in x:
            #     if first:
            #         columnsStr = (
            #             "市辖区", "{}0100".format(citys.get('code', None)[:2]),None,city.get("pCode", citys.get("code")))
            #         table = insertToSQL(Area, *columnsStr)
            #         first = False
            #     columnsStr = (
            #         city.get('name', None), city.get('code', None), city.get('areaZip', None),
            #         "{}0100".format(citys.get('code', None)[:2]))
            #     table = insertToSQL(Area, *columnsStr)
            # else:
            columnsStr = (
                city.get('name', None), city.get('code', None), city.get('areaZip', None),
                city.get("pCode", citys.get("code")))
            table = insertToSQL(Area, *columnsStr)
            if city.get("sub", None):
                for x in city["sub"]:
                    columnsStr = (x.get('name', None), x.get('code', None), x.get('areaZip', None),
                                  x.get("pCode", city.get("code")))
                    table = insertToSQL(Area, *columnsStr)

    resultDict = returnMsg({"ok":"ok"})
    return jsonify(resultDict)


def tableDictSort(table):
    infoDict = {
        "areaId": table.area_id,
        'areaName': table.area_name,
        'areaCode': table.area_code,
        'areaZip': table.area_zip,
        'pCode': table.p_code
    }
    return infoDict
