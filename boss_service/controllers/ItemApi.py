# coding:utf-8

import json
import sys

from flask import request, json, jsonify,url_for
from flask_jwt_extended import jwt_required

from common.FormatStr import dictRemoveNone
from common.OperationOfDB import insertToSQL, findById, conditionDataListFind, updataById, \
    executeTheSQLStatement
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from controllers.TempItemApi import addItemContent
from models.Data.Album import Album
from models.Data.Category import Category
from models.Data.Department import Department
from models.Data.Industry import Industry
from models.Data.Item import Item, ItemChangeDic as tableChangeDic
from models.Data.ItemContent import ItemContent
from models.Data.ItemContentAttach import ItemContentAttach
from models.Data.ItemIndustry import ItemIndustry
from models.Data.ItemLabel import ItemLabel
from models.Data.Label import Label
from version.v3.bossConfig import app
from TempItemApi import findItemTypeMedia
reload(sys)
sys.setdefaultencoding("utf-8")


# 行业关系表
@app.route("/chuleItemIdData", methods=["POST"])
@jwt_required
def chuleItemIdData():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    itemIds = dataDict.get('itemIds', [])
    if len(itemIds) == 0:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    sqlStr = "select * from data_item where item_id not in " + str(itemIds).replace("[", "(").replace("]", ")")
    itemTableList = executeTheSQLStatement(sqlStr)
    if itemTableList:
        infoList = []
        for itemTable in itemTableList:
            infoDict = infoDictSort(itemTable)
            infoList.append(infoDict)
        resultDict = returnMsg(infoList)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 更新项目行业
def updateItemIndustry(itemIndustryIds, item_id, dbOperation):
    itemIndustryTableList = ItemIndustry.query.filter(ItemIndustry.item_id == item_id).all()
    industryIdListOld = []
    for itemIndustryTable in itemIndustryTableList:
        industryIdListOld.append(itemIndustryTable.industry_id)
    industryIdList = itemIndustryIds.split(",")
    if industryIdListOld.sort() == industryIdList.sort():
        return True
    deleteIndustryIdList = list(set(industryIdListOld).difference(set(industryIdList)))
    addIndustryIdList = list(set(industryIdList).difference(set(industryIdListOld)))
    # dbOperation = OperationOfDB()
    if len(deleteIndustryIdList):
        delete_sql_str = "delete from data_item_industry where item_id=%s and industry_id in " % item_id, str(
            deleteIndustryIdList).replace("[", "(").replace("]", ")")
        dbOperation.executeTheSQLStatement(delete_sql_str)
    for industryId in addIndustryIdList:
        industryListStr = (item_id, int(industryId))
        if not dbOperation.insertToSQL(ItemIndustry, *industryListStr):
            dbOperation.commitRollback()
            return False
    # if not dbOperation.commitToSQL():
    #     dbOperation.commitRollback()
    #     return False
    return True


# 更新项目标签
def updateItemLable(itemLabelIds, item_id, dbOperation):
    itemLabelTableList = ItemLabel.query.filter_by(item_id=item_id).all()
    labelIdListOld = []
    for itemLableTable in itemLabelTableList:
        labelIdListOld.append(itemLableTable.label_id)
    labelIdList = itemLabelIds.split(",")
    if labelIdListOld.sort() == labelIdList.sort():
        return True
    deleteLabelIdList = list(set(labelIdListOld).difference(set(labelIdList)))
    addLabelIdList = list(set(labelIdList).difference(set(labelIdListOld)))
    # dbOperation = OperationOfDB()
    if len(deleteLabelIdList):
        delete_sql_str = "delete from data_item_label where item_id =%s and  label_id in " % item_id, str(
            deleteLabelIdList).replace("[", "(").replace("]", ")")
        dbOperation.executeTheSQLStatement(delete_sql_str)
    for labelId in addLabelIdList:
        labelListStr = (item_id, int(labelId))
        if not dbOperation.insertToSQL(ItemLabel, *labelListStr):
            dbOperation.commitRollback()
            return False
    # if not dbOperation.commitToSQL():
    #     dbOperation.commitRollback()
    #     return False
    return True


# 更新
@app.route("/updateItem", methods=["POST"])
@jwt_required
def updateItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "item_id"
    intColumnClinetNameList = (u'itemId', u'levelCode', u'itemType', u'itemSort', u'isTop', u'isLock', u'isService', u'isContentJson',
    u'isClose', u'isSecular', "mediaType")
    infoList = []
    idList = dataDict.get("ids", None)
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        itemTable = Item.query.filter(Item.item_id == id).first()
        if itemTable.is_lock != "1":
            if dataDict.get("itemIndustryIds"):
                itemIndustryIds = dataDict["itemIndustryIds"]
                if not updateItemIndustry(itemIndustryIds, id, dbOperation):
                    resultDict = returnErrorMsg("update industryIds failed")
                    return jsonify(resultDict)
                dataDict.pop("itemIndustryIds")
            if dataDict.get("itemLabelIds"):
                itemLableIds = dataDict["itemLableIds"]
                if not updateItemLable(itemLableIds, id, dbOperation):
                    resultDict = returnErrorMsg("update labelIds failed")
                    return jsonify(resultDict)
                dataDict.pop("itemLableIds")
            # if dataDict.get("isContentJson") == 2:
            if dataDict.has_key("itemContent"):
                if dataDict.get("isContentJson") == 2:
                    itemContentSql = "DELETE FROM data_item_content WHERE item_id = {} ".format(id)
                    table = dbOperation.executeTheSQLStatement(itemContentSql)
                    if not table:
                        dbOperation.commitRollback()
                        resultDict = returnErrorMsg(errorCode["system_error"])
                        return jsonify(resultDict)
                item_content = dataDict.get("itemContent", "")
                resContent = addItemContent(id, item_content, dbOperation)
                if not resContent:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg(errorCode["system_error"])
                    return jsonify(resultDict)
                dataDict.pop("itemContent")
            tempItemUp = dbOperation.updateThis(Item, Item.item_id, id, dataDict, tableChangeDic,
                                                intColumnClinetNameList)
            # tempItemUp = updataById(Item, dataDict, columnId, id, tableChangeDic, intColumnClinetNameList)
            if not tempItemUp:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("upate fail")
                return jsonify(resultDict)
            if dbOperation.commitToSQL():
                resultDict = returnMsg({})
            else:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("upate fail")
            return jsonify(resultDict)

            # if tempItemUp == None:
            #     resultDict = returnErrorMsg()
            # elif tempItemUp == 0:
            #     resultDict = returnErrorMsg("the itemId not exit!")
            # else:
            #     infoDic = infoDictSort(tempItemUp)
            #     infoList.append(infoDic)
            #     resultDict = returnMsg(infoList)

        else:
            resultDict = returnErrorMsg("item already online!")
            return jsonify(resultDict)


# 删除
@app.route("/deleteItem", methods=["POST"])
@jwt_required
def deleteItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("idArray", [])
    intColumnClinetNameList = ("itemId", "deptId", "itemSort", "isClose",
                               "isLock", "isTop", "isService")

    # for id in idList:
    #     itemTable = Item.query.filter(Item.item_id==id).first()
    #     if itemTable.is_lock == "1" :
    #         resultDict = returnErrorMsg("item already online!")
    #         return jsonify(resultDict)
    # resultDict = deleteById(Item, idList, "item_id")
    deleteDict = {"isLock": 0}
    columnId = "item_id"
    for id in idList:
        tempItemUp = updataById(Item, deleteDict, columnId, id, tableChangeDic, intColumnClinetNameList)
        if tempItemUp == None:
            resultDict = returnErrorMsg()
        elif tempItemUp == 0:
            resultDict = returnErrorMsg(errorCode["param_error"])
        else:
            infoList = {}
            resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 开发区域 数据根据条件查询
@app.route("/findAreaItemByCondition", methods=["POST"])
@jwt_required
def findAreaItemByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("itemId", "itemSort",
                               "isLock", "isTop", "isService", "levelCode")
    tableName = Item.__tablename__
    orderByStr = " order by item_sort asc ,item_pulishdate desc "
    from models.Boss.Area import Area
    areaList = Area.query.filter(Area.area_status == 1).all()
    areaCodes = [ str(area.area_code) for area in areaList]
    if len(areaCodes) == 1:
        areaCodes = str(tuple(areaCodes)).replace(",","")
    elif len(areaCodes) > 1:
        areaCodes = str(tuple(areaCodes))
    else:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [{
        "field":"areaCode",
        "op":"in",
        "value":areaCodes
    }]
    for newDict in newList:
        condition.append(newDict)
    itemList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName,
                                            orderByStr=orderByStr)
    if itemList:
        InfoList = []
        for itemTable in itemList:
            infoDict = returnInformation(itemTable)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 根据条件查询
@app.route("/findItemByCondition", methods=["POST"])
@jwt_required
def findItemByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("itemId", "itemSort",
                               "isLock", "isTop", "isService", "levelCode")
    tableName = Item.__tablename__
    orderByStr = " order by item_sort asc ,item_pulishdate desc "

    itemList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tableName,
                                            orderByStr=orderByStr)
    if itemList:
        InfoList = []
        for itemTable in itemList:
            infoDict = returnInformation(itemTable)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)

# 根据条件查询 普通
@app.route("/findItemSourceByCondition", methods=["POST"])
@jwt_required
def findItemSourceByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = ("itemId", "deptId", "itemSort",
                               "isLock", "isTop", "isService", "levelCode")
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
                                            orderByStr=orderByStr)
    if itemList:
        InfoList = []
        for itemTable in itemList:
            infoDict = returnInformation(itemTable)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情
@app.route("/findItemById", methods=["POST"])
@jwt_required
def findItemById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('itemId', None)
    if id == None:
        resultDict = returnErrorMsg("not find menuId!")
        return jsonify(resultDict)
    itemTable = findById(Item, "item_id", id)
    if itemTable:
        infoDict = returnInformation(itemTable)
        resultDict = returnMsg(infoDict)
    elif itemTable == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 提取条件查询与详情信息
def returnInformation(itemTable):
    # deptId = itemTable.dept_id
    #
    # # 关联部门以及分类信息
    # deptTable = Department.query.filter(Department.dept_id == deptId).first()
    # try:
    #     deptName = deptTable.dept_name
    #     levelCode = deptTable.level_code
    # except:
    #     deptName = None
    #     levelCode = None
    # try:
    #     categoryInfo = findById(Category, "category_id", deptTable.category_id)
    #     categoryName = categoryInfo.category_name
    #     # categoryName = deptTable.category.category_name
    # except:
    #     categoryName = None
    itemId = itemTable.item_id
    # 获取行业信息
    industryItemTableList = ItemIndustry.query.filter(ItemIndustry.item_id == itemId).all()
    industryNameList = []
    for industryItemTable in industryItemTableList:
        try:
            industrtInfo = findById(Industry, "industry_id", industryItemTable.industry_id)
            industryName = industrtInfo.industry_name
            # industryName = industryItemTable.industry.industry_name
        except:
            industryName = "None"
        industryNameList.append(industryName)
    industryName = ",".join(industryNameList)
    # 标签信息
    labelItemTableList = ItemLabel.query.filter(ItemLabel.item_id == itemId).all()
    labelNameList = []
    for labelItemTable in labelItemTableList:
        try:
            labelInfo = findById(Label, "label_id", labelItemTable.label_id)
            labelName = labelInfo.label_name
            # labelName = labelItemTable.label.label_name
        except:
            labelName = "None"
        labelNameList.append(labelName)
    labelName = ",".join(labelNameList)
    # 获取内容
    itemContentList = ItemContent.query.filter(ItemContent.item_id == itemId).order_by(
        ItemContent.chapter_index.asc()).all()
    itemContent = []
    for itemContentTable in itemContentList:
        itemContentDict = {
            "id": itemContentTable.id,
            "isChapterTitle": itemContentTable.is_chapter_title,
            "titleItem": itemContentTable.chapter_title,
            "contactItem": itemContentTable.chapter_content,
            "storItem": itemContentTable.chapter_index,
        }
        itemContentDict = dictRemoveNone(itemContentDict)
        itemContent.append(itemContentDict)
    if itemContent == []:
        itemContent = ""
    else:
        itemContent = json.dumps(itemContent)
        itemContent = itemContent
    # 获取附件信息

    itemContentAttchTableList = ItemContentAttach.query.filter(ItemContentAttach.item_id == itemId).all()
    itemContentAttch = []
    for itemContentAttchTable in itemContentAttchTableList:
        if itemContentAttchTable.attach_path:
            itemContentAttachDict = {
                "id": itemContentAttchTable.id,
                "title": itemContentAttchTable.attach_title,
                "content": itemContentAttchTable.attach_path,
            }
            itemContentAttachDict = dictRemoveNone(itemContentAttachDict)
            itemContentAttch.append(itemContentAttachDict)
    # 获取相册
    itemAlbumList = Album.query.filter(Album.item_id == itemId).order_by(
        Album.album_index.asc()).all()
    itemAlbum = []
    for itemAlbumTable in itemAlbumList:
        albumPath = url_for("static",filename=itemAlbumTable.album_path,_external=True)
        itemAlbumDict = {
            "id": itemAlbumTable.id,
            "albumIndex": itemAlbumTable.album_index,
            "albumPath": itemAlbumTable.album_path,
            "forumPath": albumPath,
        }
        itemAlbumDict = dictRemoveNone(itemAlbumDict)
        itemAlbum.append(itemAlbumDict)
    deptName = itemTable.dept_name
    levelCode = itemTable.level_code
    categoryName = itemTable.category_name
    areaCode = itemTable.area_code
    infoDict = {
        "itemAlbum": itemAlbum,
        "itemContentAttach": itemContentAttch,
        "itemContent": itemContent,
        "deptName": deptName,
        "levelCode": levelCode,
        "industryName": industryName,
        "labelName": labelName,
        "categoryName": categoryName,
        "itemId": itemTable.item_id,
        # "deptId": itemTable.dept_id,
        "itemUrl": itemTable.item_url,
        "itemTitle": itemTable.item_title,
        "itemImgurl": itemTable.item_imgurl,
        "itemPulishdate": itemTable.item_pulishdate,
        "itemType": itemTable.item_type,
        "itemSort": itemTable.item_sort,
        "isTop": itemTable.is_top,
        "isLock": itemTable.is_lock,
        "isService": itemTable.is_service,
        "isContentJson": itemTable.is_content_json,
        "createTime": itemTable.create_time,
        "isClose": itemTable.is_close,
        "itemDeadline": itemTable.item_deadline,
        "isSecular": itemTable.is_secular,
        "mediaType": itemTable.media_type,
        "mediaUrl": itemTable.media_url,
        # "itemContact": itemTable.item_contact,
        # "itemPricerange": itemTable.item_pricerange,
        # "itemDeadline": str(itemTable.item_deadline),
        # "itemSubmitAddress": itemTable.item_submit_address,
        # "isClose": itemTable.is_close,
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict


# 添加
@app.route("/addItem", methods=["POST"])
@jwt_required
def addItem():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.has_key("itemDeadline") :
        if dataDict.get("itemDeadline") == "":
            dataDict.pop("itemDeadline")
            itemDeadline = None
        else:
            itemDeadline = dataDict.get("itemDeadline")
    else:
        itemDeadline = None
    itemType = dataDict.get("itemType")
    mediaType = findItemTypeMedia(itemType)
    if not mediaType:
        mediaType = dataDict.get("mediaType",None)
    columnsStr = (dataDict.get("deptId", None),
                  dataDict.get("itemUrl", None),
                  dataDict.get("itemTitle", None),
                  dataDict.get("itemImgurl", None),
                  dataDict.get("itemPulishdate", None),
                  dataDict.get("itemType", None),
                  dataDict.get("itemSort", 0),
                  dataDict.get("isTop", 0),
                  dataDict.get("isLock", 0),
                  dataDict.get("isService", 0),
                  dataDict.get("isContentJson", 2),
                  dataDict.get("createTime", None),
                 dataDict.get("isClose", 0),
                  itemDeadline,
                 dataDict.get("isSecular", 0),
                  mediaType,
                 dataDict.get("mediaUrl", None),
    )
    itemTable = insertToSQL(Item, *columnsStr)
    if itemTable:
        infoDict = infoDictSort(itemTable)
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def infoDictSort(table):
    infoDict = {
        "itemId": table.item_id,
        "deptId": table.dept_id,
        "itemUrl": table.item_url,
        "itemTitle": table.item_title,
        "itemImgurl": table.item_imgurl,
        "itemPulishdate": table.item_pulishdate,
        "itemType": table.item_type,
        "itemSort": table.item_sort,
        "isTop": table.is_top,
        "isLock": table.is_lock,
        "isService": table.is_service,
        "isContentJson": table.is_content_json,
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict
