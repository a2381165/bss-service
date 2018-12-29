# coding:utf-8

from urllib import quote

from flask import request, jsonify, json,url_for
from flask_jwt_extended import jwt_required

from common.FormatStr import dictRemoveNone
from common.Log import queryLog
from common.OperationOfDB import findById
from common.ReturnMessage import returnMsg, returnErrorMsg
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
from models.Data.TempItem import TempItem
from version.v3.bossConfig import app


# 模板item 预览
@app.route("/findAppTempItemById", methods=["POST"])
# @jwt_required
# @queryLog("data_temp_item")
def findAppTempItemById():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get('itemId', None)
    if id == None:
        resultDict = returnErrorMsg("not find menuId!")
        return jsonify(resultDict)
    itemTable = findById(TempItem, "item_id", id)
    if itemTable:
        infoDict = tempItemInfoDictSort(itemTable)
        resultDict = returnMsg(infoDict)
    elif itemTable == 0:
        infoDict = {}
        resultDict = returnMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 正式app预览
@app.route("/findAppItemById", methods=["POST"])
@jwt_required
@queryLog("data_item")
def findAppItemById():
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
        resultDict = returnErrorMsg(infoDict)
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取附件内容
@app.route("/getItemContentAttachByTempItemId", methods=["POST"])
@jwt_required
def getItemContentAttachByTempItemId():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    itemId = dataDict.get("itemId")
    if not itemId:
        resultDict = returnErrorMsg("not find itemId")
        return jsonify(resultDict)
    itemContentAttachList = getItemContentAttachList(itemId)
    resultDict = returnMsg(itemContentAttachList)
    return jsonify(resultDict)


# 模板项目
def tempItemInfoDictSort(table):
    deptId = table.dept_id
    deptName = ""
    levelCode = ""
    categoryName = ""
    deptTable = Department.query.filter(Department.dept_id == deptId).first()
    if deptTable:
        deptName = deptTable.dept_name
        levelCode = deptTable.level_code
        try:
            categoryInfo = Category.query.filter(Category.category_id == deptTable.category_id).first()
            categoryName = categoryInfo.category_name
        except:
            categoryName = ""
    itemIndustryIds = table.item_industry_ids
    if itemIndustryIds:
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
    else:
        industryNames = ""
    itemLableIds = table.item_label_ids
    if itemLableIds:
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
    else:
        labelNames = ""
    infoDict = {
        "itemId": table.item_id,
        "deptId": table.dept_id,
        "itemUrl": table.item_url,
        "itemTitle": table.item_title,
        "itemImgurl": table.item_imgurl,
        "itemPulishdate": table.item_pulishdate,
        "itemAlbum": table.item_album,
        "itemContent": table.item_content,
        # "itemIndustryIds": table.item_industry_ids,
        # "itemLabelIds": table.item_label_ids,
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
        "meidaType": table.media_type,
        "mediaUrl": table.media_url,

        "itemIndustryIds": itemIndustryIds,
        "itemLabelIds": itemLableIds,
        "labelNames": labelNames,
        "deptName": deptName,
        "categoryName": categoryName,
        "levelCode": levelCode,
        "industryNames": industryNames
    }
    infoDict = dictRemoveNone(infoDict)

    return infoDict


# 正式项目 提取条件查询与详情信息
def returnInformation(itemTable):
    # deptId = itemTable.dept_id

    # # 关联部门以及分类信息
    # deptTable = Department.query.filter(Department.dept_id == deptId).first()
    # try:
    #     deptName = deptTable.dept_name
    #     levelCode = deptTable.level_code
    # except:
    #     deptName = ""
    #     levelCode = ""
    # try:
    #     categoryName = deptTable.category.category_name
    # except:
    #     categoryName = ""
    itemId = itemTable.item_id
    # 获取行业信息
    industryItemTableList = ItemIndustry.query.filter(ItemIndustry.item_id == itemId).all()
    industryNameList = []
    for industryItemTable in industryItemTableList:
        try:
            industryName = industryItemTable.industry.industry_name
        except:
            industryName = ""
        industryNameList.append(industryName)
    industryName = ",".join(industryNameList)
    # 标签信息
    labelItemTableList = ItemLabel.query.filter(ItemLabel.item_id == itemId).all()
    labelNameList = []
    for labelItemTable in labelItemTableList:
        try:
            labelName = labelItemTable.label.label_name
        except:
            labelName = ""
        labelNameList.append(labelName)
    labelName = ",".join(labelNameList)
    # 获取内容
    itemContentList = ItemContent.query.filter(ItemContent.item_id == itemId).order_by(
        ItemContent.chapter_index.asc()).all()
    itemContent = []
    for itemContentTable in itemContentList:
        itemContentDict = {
            "id":itemContentTable.id,
            "isChapterTitle": itemContentTable.is_chapter_title,
            "titleItem": itemContentTable.chapter_title,
            "contactItem": itemContentTable.chapter_content,
            "chapterIndex": itemContentTable.chapter_index
        }

        itemContent.append(itemContentDict)
    # itemContent = json.dumps(itemContent)
    itemContent = quote(json.dumps(itemContent),safe=":, /")
    # 获取附件信息
    itemContentAttchTableList = ItemContentAttach.query.filter(ItemContentAttach.item_id == itemId).all()
    itemContentAttch = []
    for itemContentAttchTable in itemContentAttchTableList:
        if itemContentAttchTable.attach_path:
            itemContentDict = {
                "title": itemContentAttchTable.attach_title,
                "content": itemContentAttchTable.attach_path,
            }
            itemContentAttch.append(itemContentDict)
    itemContentAttch = json.dumps(itemContentAttch)
    # 获取相册
    itemAlbumList = Album.query.filter(Album.item_id == itemId).order_by(
        Album.album_index.asc()).all()
    itemAlbum = []
    for itemAlbumTable in itemAlbumList:
        albumPath = url_for("static",filename=itemAlbumTable.album_path,_external=True)
        itemContentDict = {
            "albumIndex": itemAlbumTable.album_index,
            "albumPath": itemAlbumTable.album_path,
            "forumPath": albumPath,
        }
        itemAlbum.append(itemContentDict)
    itemAlbum = json.dumps(itemAlbum)
    deptName =itemTable.dept_name
    levelCode = itemTable.level_code
    categoryName = itemTable.category_name
    infoDict = {
        "itemAlbum": itemAlbum,
        "itemContentAttach": itemContentAttch,
        "itemContent": itemContent,
        "deptName": deptName,
        "levelCode": levelCode,
        "industryName": industryName,
        "labelName": labelName,
        "categoryName": categoryName,
        "itemId": itemId,
        # "deptId": deptId,
        "itemTitle": itemTable.item_title,
        "itemPulishdate": itemTable.item_pulishdate,
        # "itemContact": itemTable.item_contact,
        # "itemPricerange": itemTable.item_pricerange,
        # "itemDeadline": str(itemTable.item_deadline),
        # "itemSubmitAddress": itemTable.item_submit_address,
        "itemUrl": itemTable.item_url,
        "itemImgurl": itemTable.item_imgurl,
        "itemSort": itemTable.item_sort,
        # "isClose": itemTable.is_close,
        "isLock": itemTable.is_lock,
        "isTop": itemTable.is_top,
        "itemType": itemTable.item_type,
        "isService": itemTable.is_service,
        "isContentJson": itemTable.is_content_json,
        "isClose": itemTable.is_close,
        "itemDeadline": itemTable.item_deadline,
        "isSecular": itemTable.is_secular,
        "meidaType":itemTable.media_type,
        "mediaUrl":itemTable.media_url,
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict


def getItemContentAttachList(item_id):
    itemContentAttachList = []
    itemContentAttachTableList = ItemContentAttach.query.filter(ItemContentAttach.item_id == item_id).all()
    for itemContentAttachTable in itemContentAttachTableList:
        tableDict = {
            "id": itemContentAttachTable.id,
            "itemId": itemContentAttachTable.item_id,
            "attachExtensionName": itemContentAttachTable.attach_extension_name,
            "attachSize": itemContentAttachTable.attach_size,
            "attachTitle": itemContentAttachTable.attach_title,
            "attachPath": itemContentAttachTable.attach_path,
            "createTime": itemContentAttachTable.create_time,
        }
        tableDict = dictRemoveNone(tableDict)
        itemContentAttachList.append(tableDict)
    return itemContentAttachList
