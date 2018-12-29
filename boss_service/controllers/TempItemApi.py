# -*- coding: utf-8 -*-
import json
from urllib import unquote

from flask import request, json, jsonify, url_for
from flask_jwt_extended import jwt_required, current_user

from Res import AuditCode
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.Log import addLog, queryLog, deleteLog, updateLog
from common.OperationOfDB import deleteById, insertToSQL, findById, conditionDataListFind, updataById,deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, returnErrorMsg, errorCode
from models.Data.Album import Album
from models.Data.Category import Category
from models.Data.Department import Department
from models.Data.Industry import Industry
from models.Data.Item import Item
from models.Data.ItemContent import ItemContent
from models.Data.ItemContentAttach import ItemContentAttach
from models.Data.ItemIndustry import ItemIndustry
from models.Data.ItemLabel import ItemLabel
from models.Data.Label import Label
from models.Data.TempItem import TempItem, TempItemChangeDic as tableChangeDic
from models.Data.ItemService import ItemService
from version.v3.bossConfig import app
from urllib import quote
import datetime
from common.uploadFile import zilbImage


def findItemTypeMedia(itemType):
    if itemType == 1:
        mediaType = 2
    elif itemType == 2:
        mediaType = 1
    else:
        mediaType = None
    return mediaType


# 修改
@app.route("/updateTempItem", methods=["POST"])
@jwt_required
@updateLog("data_temp_item")
def updateTempItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    infoList = []
    idList = dataDict.get("ids", None)
    dataDict["createTime"] = getTimeStrfTimeStampNow()
    if not idList:
        resultDict = returnErrorMsg("not find ids!")
        return jsonify(resultDict)
    itemId = "item_id"
    intColumnClinetNameList = (
        u'itemId', u'deptId', u'checkStatus', u'itemType', u'tempItemStatus', u'isContentJson', u'isClose',
        u'isSecular',
        "mediaType")
    dbOperation = OperationOfDB()
    for id in idList:
        if dataDict.get("checkStatus", None) == 1:
            table = findById(TempItem, "item_id", id)
            if not table:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("not find table")
                return jsonify(resultDict)
            if not table.item_content:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["tempItem_not_content"])
                return jsonify(resultDict)
            try:
                table = json.loads(unquote(table.item_content))
                if not table[0]["contactItem"]:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg(errorCode["tempItem_not_content"])
                    return jsonify(resultDict)
            except:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["tempItem_not_content"])
                return jsonify(resultDict)
        if dataDict.has_key("itemDeadline") and dataDict["itemDeadline"] == "":
            dataDict.pop("itemDeadline")
        itemType = dataDict.get("itemType", "")
        if itemType:
            mediaType = dataDict.get("mediaType", "")
            if not mediaType:
                mediaType = findItemTypeMedia(itemType)
                if mediaType:
                    dataDict["mediaType"] = mediaType
        else:
            tempItemInfo = findById(TempItem, "item_id", id)
            if tempItemInfo:
                itemType = tempItemInfo.item_type
                mediaType = findItemTypeMedia(itemType)
                if mediaType:
                    dataDict["mediaType"] = mediaType
            else:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["query_fail"])
                return jsonify(resultDict)
        if dataDict.has_key("itemAlbum"):
            itemAlbum = dataDict.get("itemAlbum")
            zilbImage(itemAlbum)
        menuUp = dbOperation.updateThis(TempItem,TempItem.item_id,id,dataDict,tableChangeDic)
        # menuUp = updataById(TempItem, dataDict, itemId, id, tableChangeDic, intColumnClinetNameList)
        if not menuUp :
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)

    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)
    # if menuUp == None:
    #     resultDict = returnErrorMsg()
    # elif menuUp == 0:
    #     resultDict = returnErrorMsg("the itemId not exit!")
    # else:
    #     infoDict = infoDictSort(menuUp)
    #     infoList.append(infoDict)
    #     resultDict = returnMsg(infoList)
    # return jsonify(resultDict)


# 审核
@app.route("/checkTempItem", methods=["POST"])
@jwt_required
@updateLog("data_temp_item")
def checkTempItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    checkStatus = dataDict.get("checkStatus", None)
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg("not find ids!")
        return jsonify(resultDict)
    adminTable = current_user
    adminName = adminTable.admin_name
    dateTimeNow = getTimeStrfTimeStampNow()
    dataDict["checkTime"] = dateTimeNow
    dataDict["checkPerson"] = adminName
    infoList = []
    dbOperation = OperationOfDB()
    for id in idList:
        itemTimeTable = TempItem.query.filter(TempItem.item_id == id).first()
        # 审核通过就先创建service_code
        # if checkStatus == AuditCode["pass"]:
        #     serviceCode = createServiceCode(itemTimeTable)
        #     if serviceCode:
        #         serviceCode = serviceCode
        #     else:
        #         resultDict = returnErrorMsg("create serviceCode failed")
        #         return jsonify(resultDict)
        itemTimeTable.updateTable(dataDict)
        tempItemUp = dbOperation.addTokenToSql(itemTimeTable)
        if not tempItemUp:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("update failed")
            return jsonify(resultDict)
        else:
            # 创建数据到item等表中
            if (checkStatus == AuditCode["pass"]):
                depttable = findById(Department, "dept_id", tempItemUp.dept_id)
                itemTableCheck = Item.query.filter(Item.dept_name == depttable.dept_name,
                                                   Item.item_title == tempItemUp.item_title).first()
                if itemTableCheck:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("item already exists")
                    return jsonify(resultDict)

                itemTable = addDataToItemTable(tempItemUp, dbOperation, depttable)
                if itemTable:
                    infoDict = infoDictSort(tempItemUp)
                    infoList.append(infoDict)
                else:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg("commit failed!")
                    return jsonify(resultDict)
            else:
                pass
                # 不在时间范围内只更新数据
                # dbOperation.commitRollback()
                # resultDict = returnErrorMsg("update failed")
                # return jsonify(resultDict)

    if dbOperation.commitToSQL():
        resultDict = returnMsg(infoList)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg("commit failed")
    return jsonify(resultDict)


#  删除
@app.route("/deleteTempItem", methods=["POST"])
@jwt_required
@deleteLog("data_temp_item")
def deleteTempItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    dbOperation = OperationOfDB()
    for id in idList:
        table = findById(TempItem,"item_id",id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        table.temp_item_status = 2
        table = dbOperation.addTokenToSql(table)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 镇删除
@app.route("/deleteRealTempItem", methods=["POST"])
@jwt_required
@deleteLog("data_temp_item")
def deleteRealTempItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(TempItem, idList, "item_id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)
    return jsonify(resultDict)


# 数据维护  员 使用 默认 create_person
@app.route("/findTempItemByCondition", methods=["POST"])
@jwt_required
@queryLog("data_temp_item")
def findTempItemByCondition():
    """good"""
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    intColumnClinetNameList = (
        "itemId", "deptId", "itemType", "tempItemStatus", "isContentJson", "checkStatus", "mediaType")
    adminTable = current_user
    adminName = adminTable.admin_name
    condition = dataDict["condition"]
    adminDict = {"field": "createPerson", "op": "equal", "value": adminName}
    condition.append(adminDict)
    orderByStr = " order by create_time desc "
    tableName = TempItem.__tablename__
    tempItemList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName,
                                                orderByStr=orderByStr)
    if tempItemList:
        InfoList = []
        for tableData in tempItemList:
            deptId = tableData[1]
            deptName = ""
            levelCode = ""
            categoryName = ""
            industryNames = ""
            labelNames = ""
            itemAlbum = []
            deptTable = Department.query.filter(Department.dept_id == deptId).first()
            if deptTable:
                deptName = deptTable.dept_name
                levelCode = deptTable.level_code
                try:
                    categoryInfo = Category.query.filter(Category.category_id == deptTable.category_id).first()
                    categoryName = categoryInfo.category_name
                except:
                    categoryName = ""
            itemIndustryIds = tableData[8]
            if itemIndustryIds:
                # industryList = Industry.query.filter(Industry.industry_id.in_(itemIndustryIds)).all()
                # if industryList:
                #     industryNames = "/".join([industry.industry_name for industry in industryList])
                industryList = itemIndustryIds.split(",")
                industryNameList = []
                for industryId in industryList:
                    industryTable = Industry.query.filter(Industry.industry_id == industryId).first()
                    if industryTable:
                        industryName = industryTable.industry_name
                    else:
                        industryName = ""
                    industryNameList.append(industryName)
                industryNames = "/".join(industryNameList)

            itemLableIds = tableData[9]
            if itemLableIds:
                # labelList = Label.query.filter(Label.label_id.in_(itemLableIds)).all()
                # if labelList:
                #     labelNames = "/".join([label.label_name for label in labelList if label.label_name])
                labelList = itemLableIds.split(",")
                labelNameList = []
                for labelId in labelList:
                    labelTable = Label.query.filter(Label.label_id == labelId).first()
                    if labelTable:
                        labelName = labelTable.label_name
                    else:
                        labelName = ""
                    labelNameList.append(labelName)
                labelNames = "/".join(labelNameList)
            # for image in itemAlbums:
            #     resultFile = url_for("static", filename=image, _external=True)
            #     itemAlbum.append(resultFile)
            # except:
            #     itemAlbum = []
            # itemContent = getItemContent(itemId)
            infoDict = {
                "itemId": tableData[0],
                "deptId": tableData[1],
                "itemUrl": tableData[2],
                "itemTitle": tableData[3],
                "itemImgurl": tableData[4],
                "itemPulishdate": tableData[5],
                "itemAlbum": tableData[6],
                # "itemAlbum": itemAlbum,
                "itemContent": tableData[7],
                # "itemIndustryIds": tableData[8],
                # "itemLabelIds": tableData[9],
                "checkPerson": tableData[10],
                "checkStatus": tableData[11],
                "checkRemark": tableData[12],
                "checkTime": tableData[13],
                "createPerson": tableData[14],
                "createTime": tableData[15],
                "itemType": tableData[16],
                "itemContentAttach": tableData[17],
                "tempItemStatus": tableData[18],
                "isContentJson": tableData[19],
                "isClose": tableData[20],
                "itemDeadline": tableData[21],
                "isSecular": tableData[22],
                "mediaType": tableData[23],
                "mediaUrl": tableData[24],
                "itemIndustryIds": itemIndustryIds,
                "itemLabelIds": itemLableIds,
                "labelNames": labelNames,
                "deptName": deptName,
                "categoryName": categoryName,
                "levelCode": levelCode,
                "industryNames": industryNames
            }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 数据审核员 使用 无默认
@app.route("/findTempItemByConditions", methods=["POST"])
@jwt_required
@queryLog("data_temp_item")
def findTempItemByConditions():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg("not find condition!")
        return jsonify(resultDict)
    intColumnClinetNameList = (
        "itemId", "deptId", "itemType", "tempItemStatus", "isContentJson", "checkStatus", "mediaType")
    # areaCode = dataDict.get("areaCode", "")
    # releaseDeptIdList = []
    # if areaCode:
    #     releaseDeptIdList = getOneReleaseDepts(areaCode)
    # if len(releaseDeptIdList) != 0:
    #     condition = dataDict["condition"]
    #     newDict = {}
    #     newDict["field"] = "deptId"
    #     newDict["op"] = "in"
    #     newDict["value"] = tuple(releaseDeptIdList)
    #     condition.append(newDict)
    orderByStr = " order by create_time desc "
    tableName = TempItem.__tablename__
    tempItemList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName,
                                                orderByStr=orderByStr)
    if tempItemList:
        InfoList = []
        for tableData in tempItemList:
            deptId = tableData[1]
            deptName = ""
            levelCode = ""
            categoryName = ""
            industryNames = ""
            labelNames = ""
            deptTable = Department.query.filter(Department.dept_id == deptId).first()
            if deptTable:
                deptName = deptTable.dept_name
                levelCode = deptTable.level_code
                try:
                    categoryInfo = Category.query.filter(Category.category_id == deptTable.category_id).first()
                    categoryName = categoryInfo.category_name
                except:
                    categoryName = ""
            itemIndustryIds = tableData[8]
            if itemIndustryIds:
                # industryList = Industry.query.filter(Industry.industry_id.in_(itemIndustryIds)).all()
                # if industryList:
                #     industryNames = "/".join([industry.industry_name for industry in industryList])
                industryList = itemIndustryIds.split(",")
                industryNameList = []
                for industryId in industryList:
                    industryTable = Industry.query.filter(Industry.industry_id == industryId).first()
                    if industryTable:
                        industryName = industryTable.industry_name
                    else:
                        industryName = ""
                    industryNameList.append(industryName)
                industryNames = "/".join(industryNameList)

            itemLableIds = tableData[9]
            if itemLableIds:
                # labelList = Label.query.filter(Label.label_id.in_(itemLableIds)).all()
                # if labelList:
                #     labelNames = "/".join([label.label_name for label in labelList if label.label_name])
                labelList = itemLableIds.split(",")
                labelNameList = []
                for labelId in labelList:
                    labelTable = Label.query.filter(Label.label_id == labelId).first()
                    if labelTable:
                        labelName = labelTable.label_name
                    else:
                        labelName = ""
                    labelNameList.append(labelName)
                labelNames = "/".join(labelNameList)

            # itemContent = getItemContent(itemId)
            infoDict = {
                "itemId": tableData[0],
                "deptId": tableData[1],
                "itemUrl": tableData[2],
                "itemTitle": tableData[3],
                "itemImgurl": tableData[4],
                "itemPulishdate": tableData[5],
                "itemAlbum": tableData[6],
                "itemContent": tableData[7],
                # "itemIndustryIds": tableData[8],
                # "itemLabelIds": tableData[9],
                "checkPerson": tableData[10],
                "checkStatus": tableData[11],
                "checkRemark": tableData[12],
                "checkTime": tableData[13],
                "createPerson": tableData[14],
                "createTime": tableData[15],
                "itemType": tableData[16],
                "itemContentAttach": tableData[17],
                "tempItemStatus": tableData[18],
                "isContentJson": tableData[19],
                "isClose": tableData[20],
                "itemDeadline": tableData[21],
                "isSecular": tableData[22],
                "itemIndustryIds": itemIndustryIds,
                "itemLabelIds": itemLableIds,
                "labelNames": labelNames,
                "deptName": deptName,
                "categoryName": categoryName,
                "levelCode": levelCode,
                "industryNames": industryNames
            }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情
@app.route("/findTempItemById", methods=["POST"])
@jwt_required
@queryLog("data_temp_item")
def findTempItemById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('itemId', None)
    if id == None:
        resultDict = returnErrorMsg("not find itemId!")
        return jsonify(resultDict)
    tempItemTable = findById(TempItem, "item_id", id)
    if tempItemTable:
        infoDict = infoDictSort(tempItemTable)
        resultDict = returnMsg(infoDict)
    elif tempItemTable == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 添加数据
@app.route("/addTempItem", methods=["POST"])
@jwt_required
@addLog("data_temp_item")
def addTempItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    dateTimeNow = getTimeStrfTimeStampNow()
    adminTable = current_user
    createPerson = adminTable.admin_name
    itemContentList = []
    itemContent = dataDict.get("itemContent", "")
    itemContentDict = {
        "isChapterTitle": 0,
        "titleItem": "",
        "contactItem": itemContent,
        "chapterIndex": 0
    }
    itemContentList.append(itemContentDict)
    # itemContent = json.dumps(itemContent)
    itemContent = quote(json.dumps(itemContentList), safe=":, /")

    columnsStr = (dataDict.get("deptId", None), dataDict.get("itemUrl", None),
                  dataDict.get("itemTitle", None), dataDict.get("itemImgurl", None),
                  dataDict.get("itemPulishdate", None),
                  dataDict.get("itemAlbum", None), itemContent,
                  dataDict.get("itemIndustryIds", None), dataDict.get("itemLabelIds", None),
                  dataDict.get("checkPerson", None), 0,
                  dataDict.get("checkRemark", None), dataDict.get("checkTime", None),
                  createPerson, dateTimeNow,
                  dataDict.get("itemType", None), dataDict.get("itemContentAttach", None),
                  1, dataDict.get("isContentJson", 2), dataDict.get("isClose", 0), dataDict.get("itemDeadline", None),
                  dataDict.get("isSecular", 0),dataDict.get("mediaType",0),dataDict.get("mediaUrl",None))
    tempItemTable = insertToSQL(TempItem, *columnsStr)
    if tempItemTable:
        infoDict = infoDictSort(tempItemTable)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 转交他人
@app.route("/transferTempItem", methods=["POST"])
@jwt_required
@updateLog("data_temp_item")
def transferTempItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", None)
    dataDict["createTime"] = getTimeStrfTimeStampNow()
    if not idList:
        resultDict = returnErrorMsg("not find ids!")
        return jsonify(resultDict)
    if not dataDict.has_key("createPerson"):
        resultDict = returnErrorMsg("not choice person")
        return jsonify(resultDict)
    intColumnClinetNameList = (
    u'itemId', u'deptId', u'checkStatus', u'itemType', u'tempItemStatus', u'isContentJson', u'isClose',
    u'isSecular', "mediaType")
    dbOperation = OperationOfDB()
    for id in idList:
        menuUp = dbOperation.updateThis(TempItem, TempItem.item_id, id, dataDict, tableChangeDic,
                                        intColumnClinetNameList=intColumnClinetNameList)
        if not menuUp:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)





def infoDictSort(table):
    # itemId = tempItemTable.item_id
    # itemContent = getItemContent(itemId)
    infoDict = {
        "itemId": table.item_id,
        "deptId": table.dept_id,
        "itemUrl": table.item_url,
        "itemTitle": table.item_title,
        "itemImgurl": table.item_imgurl,
        "itemPulishdate": table.item_pulishdate,
        "itemAlbum": table.item_album,
        "itemContent": table.item_content,
        "itemIndustryIds": table.item_industry_ids,
        "itemLabelIds": table.item_label_ids,
        "checkPerson": table.check_person,
        "checkStatus": table.check_status,
        "checkRemark": table.check_remark,
        "checkTime": table.check_time,
        "createPerson": table.create_person,
        "createTime": table.create_time,
        "itemType": table.item_type,
        "itemContentAttach": table.item_content_attach,
        "tempItemStatus": table.temp_item_status,
        "isContentJson": table.is_content_json,
        "isClose": table.is_close,
        "itemDeadline": table.item_deadline,
        "isSecular": table.is_secular,
        "media_type": table.media_type,
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict


# 添加到附件表
def addItemContentAttach(itemId, itemContentAttach, dbOperation):
    contentStr = unquote(itemContentAttach.encode("utf8"))
    try:
        contentList = json.loads(contentStr)
    except:
        dbOperation.commitRollback()
        return False
    for contentDict in contentList:
        if type(contentDict) == dict:
            attachExtensionName = contentDict.get("attachExtensionName", None)
            attachSize = contentDict.get("attachSize", None)
            attachTitle = contentDict.get("title", None)
            attachPath = contentDict.get("content", None)
            ItemContentAttachTable = ItemContentAttach.query.filter(ItemContentAttach.item_id == itemId,
                                                                    ItemContentAttach.attach_title == attachTitle).first()
            dateTimeNow = getTimeStrfTimeStampNow()
            # 有数据就更新
            if ItemContentAttachTable:
                tempItemContentUpDict = {
                    "itemId": itemId,
                    "attachExtensionName": attachExtensionName,
                    'attachSize': attachSize,
                    'attachTitle': attachTitle,
                    'attachPath': attachPath,
                    'createTime': dateTimeNow
                }
                ItemContentAttachTable.updateTable(tempItemContentUpDict)
                if not dbOperation.addTokenToSql(ItemContentAttachTable):
                    dbOperation.commitRollback()
                    return False
            else:
                # 无数据就新增
                contentList = (itemId,
                               attachExtensionName,
                               attachSize,
                               attachTitle,
                               attachPath,
                               dateTimeNow)
                if not dbOperation.insertToSQL(ItemContentAttach, *contentList):
                    dbOperation.commitRollback()
                    return False
        else:
            dbOperation.commitRollback()
            return False
    return True


# 添加到内容表
def addItemContent(itemId, itemContent, dbOperation):
    contentStr = unquote(itemContent.encode("utf8"))
    try:
        contentList = json.loads(contentStr)
    except ValueError:
        if isinstance(contentStr, str):
            contentStr = (itemId, 0, None, contentStr, 0, None)
            if not dbOperation.insertToSQL(ItemContent, *contentStr):
                dbOperation.commitRollback()
                return False
        else:
            return False
        return True
    except:
        dbOperation.commitRollback()
        return False
    for contentDict in contentList:
        if type(contentDict) == dict:
            # isChapterTitle = contentDict.get("isChapterTitle",None)
            chapterTitle = contentDict.get("titleItem", None)
            chapterContent = contentDict.get("contactItem", None)
            chapterIndex = contentDict.get("storItem", 0)
            albumCover = contentDict.get("albumCover", None)
            if not chapterIndex:
                chapterIndex = 0
            if chapterTitle:
                isChapterTitle = 1
            else:
                isChapterTitle = 0

            ItemContentTable = ItemContent.query.filter(ItemContent.item_id == itemId,
                                                        ItemContent.chapter_index == chapterIndex).first()
            if ItemContentTable:
                tempItemContentUpDict = {
                    "itemId": itemId,
                    "isChapterTitle": isChapterTitle,
                    'chapterTitle': chapterTitle,
                    'chapterContent': chapterContent,
                    'chapterIndex': chapterIndex,
                    'albumCover': albumCover
                }
                ItemContentTable.updateTable(tempItemContentUpDict)
                if not dbOperation.addTokenToSql(ItemContentTable):
                    dbOperation.commitRollback()
                    return False
            else:
                contentList = (itemId, isChapterTitle, chapterTitle, chapterContent, chapterIndex, albumCover)
                if not dbOperation.insertToSQL(ItemContent, *contentList):
                    dbOperation.commitRollback()
                    return False
        else:
            dbOperation.commitRollback()
            return False
    return True


# 添加到相册表
def addItemAlbum(itemId, itemAlbum, dbOperation):
    # contentStr = unquote(itemAlbum.encode("utf8"))
    try:
        contentList = json.loads(itemAlbum)
    except:
        dbOperation.commitRollback()
        return False
    from common.uploadFile import itemPhotoUpload
    picName = "accept"
    temporary = "formal"
    contentList = itemPhotoUpload(contentList, itemId, temporary, picName)
    if not contentList:
        dbOperation.commitRollback()
        return False
    for index, contentDict in enumerate(contentList):
        AlbumTable = Album.query.filter(Album.album_index == index,
                                        Album.album_path == contentDict).first()
        dateTimeNow = getTimeStrfTimeStampNow()
        if AlbumTable:
            tempItemContentUpDict = {
                "itemId": itemId,
                "albumIndex": index,
                'albumPath': contentDict,
                'createTime': dateTimeNow
            }
            AlbumTable.updateTable(tempItemContentUpDict)
            if not dbOperation.addTokenToSql(AlbumTable):
                dbOperation.commitRollback()
                return False
        else:
            contentList = (itemId,
                           index,
                           contentDict,
                           dateTimeNow)
            if not dbOperation.insertToSQL(Album, *contentList):
                dbOperation.commitRollback()
                return False
    return True


# 创建服务Code
def createServiceCode(itemTimeTable):
    """时间（8位）+行政区划代码（6位）+类型位（类别3 +第几个项目（8位）25位（数字）"""
    # itemTimeTable = TempItem.query.filter(TempItem.item_id == itemId).first()
    if itemTimeTable:
        itemDeadline = itemTimeTable.item_deadline
        tiemStamp = str(itemDeadline).replace("-", "")
        try:
            areaCode = itemTimeTable.dept.area_code
        except:
            return None
        try:
            categoryCode = itemTimeTable.dept.category.category_code
        except:
            return None
        categoryCodeStr = str(categoryCode).zfill(3)
        count = itemTimeTable.item_id
        countStr = str(count).zfill(8)
        serviceCode = tiemStamp + str(areaCode) + categoryCodeStr + countStr
        return serviceCode
    else:
        return None


# tempItem审核通过创建item数据
def addDataToItemTable(tempItemUp, dbOperation, depttable):
    isTop = 0
    itemSort = 99
    isLock = 1
    isService = 0
    categoryTable = findById(Category, "category_id", depttable.category_id)
    now = datetime.datetime.now()
    if tempItemUp.item_deadline > now:
        isClose = 0
    else:
        isClose = 1
    # except :
    #     isClose = 0
    now = getTimeStrfTimeStampNow()
    columnsStr = (
        depttable.dept_name, depttable.level_code, categoryTable.category_name, depttable.area_code,
        tempItemUp.item_url,
        tempItemUp.item_title, tempItemUp.item_imgurl,
        tempItemUp.item_pulishdate, tempItemUp.item_type, itemSort, isTop, isLock, isService,
        tempItemUp.is_content_json, now, isClose, tempItemUp.item_deadline, tempItemUp.is_secular,
        tempItemUp.media_type, tempItemUp.media_url)
    itemTable = dbOperation.insertToSQL(Item, *columnsStr)
    resAlbum = ""
    resContent = ""
    resAttach = ""
    serverTable = ""
    if itemTable:
        itemId = itemTable.item_id
        # 项目为截至才会产生服务 # 这里不再生成服务模板  直接 放到后面添加
        # if itemId and (itemDeadline > dateTimeNow):
        #     addTempService(itemId, serviceCode, adminName, dbOperation)
        # 添加到行业
        itemIndustryIds = tempItemUp.item_industry_ids
        if itemIndustryIds:
            industryIdList = itemIndustryIds.split(",")
            for industryId in industryIdList:
                industryItemTable = ItemIndustry.query.filter(ItemIndustry.item_id == itemId, ItemIndustry.
                                                              industry_id == int(industryId)).first()
                if industryItemTable:
                    continue
                industryListStr = (itemId, int(industryId))
                if not dbOperation.insertToSQL(ItemIndustry, *industryListStr):
                    dbOperation.commitRollback()
                    return False
        # 添加到标签
        itemLabelIds = tempItemUp.item_label_ids
        if itemLabelIds:
            labelIdList = itemLabelIds.split(",")
            for labelId in labelIdList:
                labelItemTable = ItemLabel.query.filter(ItemLabel.item_id == itemId, ItemLabel.
                                                        label_id == int(labelId)).first()
                if labelItemTable:
                    continue
                labelListStr = (itemId, int(labelId), "")
                if not dbOperation.insertToSQL(ItemLabel, *labelListStr):
                    dbOperation.commitRollback()
                    return False
        # 添加到附件
        if tempItemUp.item_content_attach:
            resAttach = addItemContentAttach(itemId, tempItemUp.item_content_attach, dbOperation)
        else:
            resAttach = True
        # 添加到内容
        if tempItemUp.item_content:
            resContent = addItemContent(itemId, tempItemUp.item_content, dbOperation)
        # 添加到相册
        if tempItemUp.item_album:
            resAlbum = addItemAlbum(itemId, tempItemUp.item_album, dbOperation)
        else:
            resAlbum = True
        # 添加顶层分析 关系表 # 如果是申报项目创建分析表
        if tempItemUp.item_type == 1:
            isLock = 1
            itemserverStr = (itemId, tempItemUp.dept_id, None, None, None, 0, None, None, None, isLock)
            serverTable = dbOperation.insertToSQL(ItemService, *itemserverStr)
        else:
            serverTable = True
    if resAlbum and resContent and resAttach and serverTable:
        return True
    else:
        return False


# 更新
def update(idList, dataDict, infoList):
    if not idList:
        resultDict = returnErrorMsg("not find ids!")
        return resultDict
    itemId = "item_id"
    intColumnClinetNameList = (
        "itemId", "deptId", "checkStatus", "itemType", "tempItemStatus", "isContentJson", "mediaType")
    for id in idList:
        menuUp = updataById(TempItem, dataDict, itemId, id, tableChangeDic, intColumnClinetNameList)
        if menuUp == None:
            resultDict = returnErrorMsg()
        elif menuUp == 0:
            resultDict = returnErrorMsg("the itemId not exit!")
        else:
            infoDict = infoDictSort(menuUp)
            infoList.append(infoDict)
            resultDict = returnMsg(infoList)
    return resultDict

# # 添加到服务表
# def addTempService(itemId, serviceCode, adminName, dbOperation):
#     dateTimeNow = getTimeStrfTimeStampNow()
#     tempServiceTable = TempService.query.filter(TempService.item_id == itemId,
#                                                 TempService.service_code == serviceCode).first()
#
#     if tempServiceTable:
#         tempItemContentUpDict = {
#             "itemId": itemId,
#             "serviceCode": serviceCode,
#             'createTime': dateTimeNow,
#             "checkStatus": 0,
#             "createTime": dateTimeNow
#         }
#         tempServiceTable.updateTable(tempItemContentUpDict)
#         if not dbOperation.addTokenToSql(tempServiceTable):
#             dbOperation.commitRollback()
#             return False
#     else:
#         columnsStr = (
#             itemId, serviceCode, None, None, None, None, None, None, None, None, None, None, 0, None, None, None, "",
#             dateTimeNow)
#         if not dbOperation.insertToSQL(TempService, *columnsStr):
#             dbOperation.commitRollback()
#             return False
#
# 送审
# @app.route("/checkTempItem", methods=["POST"])
# @jwt_required
# def checkTempItem():
#     jsonData = request.get_data()
#     dataDict = json.loads(jsonData)
#     infoList = []
#     idList = dataDict.get("ids", [])
#     checkStatus = dataDict.get("checkStatus", None)
#     if not (idList and checkStatus):
#         resultDict = returnErrorMsg("not find ids or checkStatus!")
#         return jsonify(resultDict)
#     resultDict = update(idList, dataDict, infoList)
#     return jsonify(resultDict)
# # 测试
# @app.route("/upTemp", methods=["POST"])
# def upTemp():
#     # [{u'content': u'45678123', u'title': u'hjuanghang'}]
#     itemContentAttach = "%5B%7B%22chapterContent%22%3A%20%22%3Cp%3E%5Cu554a%5Cu54c8%5Cu54c8%5Cu54c8%3C/p%3E%22%2C%20%22chapterIndex%22%3A%201%2C%20%22chapterTitle%22%3A%20%22%28%5Cu7a7a%29%22%2C%20%22isChapterTitle%22%3A%201%7D%2C%20%7B%22chapterContent%22%3A%20%22%3Cp%3E%5Cu563f%5Cu563f%3C/p%3E%22%2C%20%22chapterIndex%22%3A%202%2C%20%22chapterTitle%22%3A%20%221%22%2C%20%22isChapterTitle%22%3A%201%7D%2C%20%7B%22chapterContent%22%3A%20%22%3Cp%3E%5Cu54c8%5Cu54c8%5Cu54c8%5Cu54c8%3C/p%3E%22%2C%20%22chapterIndex%22%3A%203%2C%20%22chapterTitle%22%3A%20%222%22%2C%20%22isChapterTitle%22%3A%201%7D%5D"
#     contentStr = unquote(itemContentAttach.encode("utf8"))
#     contentList = json.loads(contentStr)
#     for contentDict in contentList:
#     resultDict = returnErrorMsg("success!")
#     return jsonify(resultDict)
