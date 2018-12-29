# -*- coding: utf-8 -*-
import json

from flask import request, json, jsonify
from flask_jwt_extended import jwt_required

from common.OperationOfDB import insertToSQL, conditionDataListFind, updataById, deleteByIdBoss
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.ItemContent import ItemContent, tableChangeDic
from version.v3.bossConfig import app


# 获取内容列表
def getItemContentList(item_id, id_type="item_id"):
    itemContentList = []
    itemContentTableList = []
    if id_type == "item_id":
        itemContentTableList = ItemContent.query.filter(ItemContent.item_id == item_id).all()
    for itemContentTable in itemContentTableList:
        tableDict = {
            "Id": itemContentTable.id,
            "itemId": itemContentTable.item_id,
            "isChapterTitle": itemContentTable.is_chapter_title,
            "chapterTitle": itemContentTable.chapter_title,
            "chapterContent": itemContentTable.chapter_content,
            "chapterIndex": itemContentTable.chapter_index,
            "albumCover": itemContentTable.albumCover
        }
        itemContentList.append(tableDict)
    return itemContentList


# 根据itemId查询数据
@app.route("/getItemContentByItemId", methods=["POST"])
@jwt_required
def getItemContentByItemId():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ItemId = dataDict.get("itemId")
    if not ItemId:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    itemContentList = getItemContentList(ItemId, "item_id")
    resultDict = returnMsg(itemContentList)
    return jsonify(resultDict)


# 更新
@app.route("/updateItemContent", methods=["POST"])
@jwt_required
def updateItemContent():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "id"
    intColumnClinetNameList = (u'id', u'itemId', u'isChapterTitle', u'chapterIndex')
    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    for id in idList:
        tempItemUp = updataById(ItemContent, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if tempItemUp == None:
            resultDict = returnErrorMsg()
            return jsonify(resultDict)
        elif tempItemUp == 0:
            resultDict = returnErrorMsg("the item content not exit!")
            return jsonify(resultDict)
        else:
            infoDic = infoDictSort(tempItemUp)
        infoList.append(infoDic)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 删除
@app.route("/deleteItemContent", methods=["POST"])
@jwt_required
def deleteItemContent():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])

    count = deleteByIdBoss(ItemContent, idList, "id")
    if count:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 通过条件
@app.route("/findItemContentByCondition", methods=["POST"])
@jwt_required
def findItemContentByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("itemId", "id", "chapterTitle")
    tableName = ItemContent.__tablename__
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


# 查看详情
@app.route("/findItemContentById", methods=["POST"])
@jwt_required
def findItemContentById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('Id')
    if id == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    itemTable = ItemContent.query.filter(ItemContent.id == id).first()
    if itemTable:
        infoDict = infoDictSort(itemTable)
        resultDict = returnMsg(infoDict)
    else:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


@app.route("/addItemContent", methods=["POST"])
@jwt_required
def addItemContent():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)

    itemId = dataDict.get('itemId', None)
    chapterTitle = dataDict.get('chapterTitle', None)
    chapterContent = dataDict.get('chapterContent', None)
    isChapterTitle = dataDict.get('isChapterTitle', 0)
    chapterIndex = dataDict.get('chapterIndex', None)
    albumCover = dataDict.get('albumCover', None)
    if not (itemId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if chapterTitle:
        isChapterTitle = 1

    itemContentTable = ItemContent.query.filter(ItemContent.chapter_title == chapterTitle,
                                                ItemContent.chapter_content == chapterContent).first()
    if itemContentTable:
        resultDict = returnErrorMsg("item content already exists")
        return jsonify(resultDict)
    columnsStr = (itemId, isChapterTitle, chapterTitle,
                  chapterContent, chapterIndex, albumCover)
    itemTable = insertToSQL(ItemContent, *columnsStr)
    if itemTable:
        infoDict = infoDictSort(itemTable)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def infoDictSort(itemTable):
    infoDict = {
        "id": itemTable.id,
        "itemId": itemTable.item_id,
        'isChapterTitle': itemTable.is_chapter_title,
        'chapterTitle': itemTable.chapter_title,
        'chapterContent': itemTable.chapter_content,
        'chapterIndex': itemTable.chapter_index,
        "albumCover": itemTable.album_cover
    }
    return infoDict
