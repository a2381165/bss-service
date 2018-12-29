# -*- coding: utf-8 -*-
import datetime
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required

from common.FormatStr import dictRemoveNone
from common.OperationOfDB import insertToSQL, conditionDataListFind, updataById, deleteByIdBoss
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.ItemContentAttach import ItemContentAttach, tableChangeDic
from version.v3.bossConfig import app


# 获取项目附件列表
def getItemContentAttachList(item_id, id_type="item_id"):
    itemContentAttachList = []
    itemContentAttachTableList = []
    if id_type == "item_id":
        itemContentAttachTableList = ItemContentAttach.query.filter(ItemContentAttach.item_id == item_id).all()

    for itemContentAttachTable in itemContentAttachTableList:
        tableDict = {
            "id": itemContentAttachTable.id,
            "itemId": itemContentAttachTable.item_id,
            "attachExtensionName": itemContentAttachTable.attach_extension_name,
            "attachSize": itemContentAttachTable.attach_size,
            "attachTitle": itemContentAttachTable.attach_title,
            "attachPath": itemContentAttachTable.attach_path,
            "createTime": str(itemContentAttachTable.create_time)
        }
        itemContentAttachList.append(tableDict)
    return itemContentAttachList


# 根据itemId获取信息
@app.route("/getItemContentAttachByItemId", methods=["POST"])
@jwt_required
def getItemContentAttachByItemId():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ItemId = dataDict.get("itemId")
    if not ItemId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    itemContentAttachList = getItemContentAttachList(ItemId, "item_id")
    resultDict = returnMsg(itemContentAttachList)
    return jsonify(resultDict)


# 更新
@app.route("/updateItemContentAttach", methods=["POST"])
@jwt_required
def updateItemContentAttach():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "id"
    intColumnClinetNameList = ("itemId", "id")
    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in idList:
        tempItemUp = updataById(ItemContentAttach, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if tempItemUp == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif tempItemUp == 0:
            resultDict = returnErrorMsg("the item content attach not exit!")
            return jsonify(resultDict)
        else:
            infoDic = infoDictSort(tempItemUp)
        infoList.append(infoDic)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 删除
@app.route("/deleteItemContentAttach", methods=["POST"])
@jwt_required
def deleteItemContentAttach():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not (idList and str(idList) != "[None]"):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    count = deleteByIdBoss(ItemContentAttach, idList, "id")
    if count:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg({})
    return jsonify(resultDict)


# 根据条件查询
@app.route("/queryItemContentAttachByCondition", methods=["POST"])
@jwt_required
def findItemContentAttachByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("itemId", "Id", "attachExtensionName")
    tableName = ItemContentAttach.__tablename__
    itemList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName)
    if itemList:
        InfoList = []
        for tableData in itemList:
            infoDict = infoDictSort(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情
@app.route("/findItemContentAttachById", methods=["POST"])
@jwt_required
def findItemContentAttachById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('Id')
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    itemTable = ItemContentAttach.query.filter(ItemContentAttach.id == id).first()
    if itemTable:
        infoDict = infoDictSort(itemTable)
        resultDict = returnMsg(infoDict)
    else:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 添加
@app.route("/addItemContentAttach", methods=["POST"])
@jwt_required
def addItemContentAttach():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)

    attachTitle = dataDict.get('attachTitle')
    attachPath = dataDict.get('attachPath')
    itemContentAttachTable = ItemContentAttach.query.filter(ItemContentAttach.attach_title == attachTitle,
                                                            ItemContentAttach.attach_path == attachPath).first()
    if itemContentAttachTable:
        resultDict = returnErrorMsg("item content attach already exists")
        return jsonify(resultDict)
    itemId = dataDict.get('itemId')
    attachTitle = dataDict.get('attachTitle')
    attachPath = dataDict.get('attachPath')
    if not (itemId and attachTitle and attachPath):
        # resultDict = returnErrorMsg(errorCode["param_error"])
        resultDict = returnErrorMsg(errorCode["param_enough"])
        return jsonify(resultDict)
    attachCreateTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    columnsStr = (itemId, dataDict.get('attachExtensionName',None), dataDict.get('attachSize',None),
                  attachTitle,attachPath, attachCreateTime)
    itemTable = insertToSQL(ItemContentAttach, *columnsStr)
    if itemTable:
        infoDict = infoDictSort(itemTable)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def infoDictSort(table):
    infoDict = {
        "id": table.id,
        "itemId": table.item_id,
        "attachExtensionName": table.attach_extension_name,
        "attachSize": table.attach_size,
        "attachTitle": table.attach_title,
        "attachPath": table.attach_path,
        "createTime": table.create_time,
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict
