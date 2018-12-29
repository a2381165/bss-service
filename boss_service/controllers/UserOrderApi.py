# coding:utf-8
import datetime

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Order.UserOrder import UserOrder, UserOrderChangeDic as tableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog
import Res

from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic
from models.Boss.OrderAidance import OrderAidance
from models.Data.SubFlow import SubFlow
from models.Boss.Role import Role
from models.Boss.User import User


# 获取 列表
@app.route("/findUserOrderByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order')
def findUserOrderBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # tablename = UserOrder.__tablename__
    tablename = "view_order_service_item"
    intColumnClinetNameList = [u'orderId', u'orderType', u'orderStatus', u'orderServiceId', u'orderPoint', u'isCoupon',
                               u'isInvoice', u'isComment', u'userId']
    tableList, count = conditionDataListFind(dataDict, changeDict, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"orderId": tableData[0],
                        "orderNo": tableData[1],
                        "orderType": tableData[2],
                        "orderFrom": tableData[3],
                        "orderStatus": tableData[4],
                        "declareStatus": tableData[5],
                        "orderAddIp": tableData[6],
                        "orderAddTime": tableData[7],
                        "orderServiceId": tableData[8],
                        "contactPerson": tableData[9],
                        "contactPhone": tableData[10],
                        "contactEmail": tableData[11],
                        "orderMessage": tableData[12],
                        "orderAmount": str(tableData[13]),
                        "payableAmount": str(tableData[14]),
                        "realAmount": str(tableData[15]),
                        "orderPoint": tableData[16],
                        "isCoupon": tableData[17],
                        "isInvoice": tableData[18],
                        "isComment": tableData[19],
                        "userId": tableData[20],
                        "id": tableData[21],
                        "serviceName": tableData[22],
                        "policySource": tableData[23],
                        "servicePrice": str(tableData[24]),
                        "serviceStarttime": tableData[25],
                        "serviceDeadline": tableData[26],
                        "directionName": tableData[27],
                        "serviceContent": tableData[28],
                        "sheetContent": tableData[29],
                        "materialList": tableData[30],
                        "forecastPath": tableData[31],
                        "serviceContactPerson": tableData[32],
                        "serviceContactPhone": tableData[33],
                        "isSecular": tableData[34],
                        "isEvaluate": tableData[35],
                        "declareList": tableData[36],
                        "categoryType": tableData[37],
                        "servciceProcess": tableData[38],
                        "itemId": tableData[39],
                        "deptName": tableData[40],
                        "levelCode": tableData[41],
                        "categoryName": tableData[42],
                        "areaCode": tableData[43],
                        "itemUrl": tableData[44],
                        "itemTitle": tableData[45],
                        "itemImgurl": tableData[46],
                        "itemPulishdate": tableData[47],
                        "itemType": tableData[48],
                        "itemSort": tableData[49],
                        "isTop": tableData[50],
                        "isLock": tableData[51],
                        "isService": tableData[52],
                        "isContentJson": tableData[53],
                        "createTime": tableData[54],
                        "isClose": tableData[55],
                        "itemDeadline": tableData[56],
                        "mediaType": tableData[57],
                        "mediaUrl": tableData[58],
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情 
@app.route("/getUserOrderDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order')
def getUserOrderDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("orderId", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserOrder, "order_id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"orderId": table.order_id,
                "orderNo": table.order_no,
                "orderType": table.order_type,
                "orderFrom": table.order_from,
                "orderStatus": table.order_status,
                "declareStatus": table.declare_status,
                "orderAddIp": table.order_add_ip,
                "orderAddTime": table.order_add_time,
                "orderServiceId": table.order_service_id,
                "contactPerson": table.contact_person,
                "contactPhone": table.contact_phone,
                "contactEmail": table.contact_email,
                "orderMessage": table.order_message,
                "orderAmount": table.order_amount,
                "payableAmount": table.payable_amount,
                "realAmount": table.real_amount,
                "orderPoint": table.order_point,
                "isCoupon": table.is_coupon,
                "isInvoice": table.is_invoice,
                "isComment": table.is_comment,
                "userId": table.user_id, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserOrder", methods=["POST"])
@jwt_required
@deleteLog('zzh_user_order')
def deleteUserOrder():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserOrder, ids, "order_id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserOrder", methods=["POST"])
@jwt_required
@addLog('zzh_user_order')
def addUserOrder():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("orderNo", None), dataDict.get("orderType", None), dataDict.get("orderFrom", None),
                 dataDict.get("orderStatus", None), dataDict.get("declareStatus", None),
                 dataDict.get("orderAddIp", None), dataDict.get("orderAddTime", None),
                 dataDict.get("orderServiceId", None), dataDict.get("contactPerson", None),
                 dataDict.get("contactPhone", None), dataDict.get("contactEmail", None),
                 dataDict.get("orderMessage", None), dataDict.get("orderAmount", None),
                 dataDict.get("payableAmount", None), dataDict.get("realAmount", None),
                 dataDict.get("orderPoint", None), dataDict.get("isCoupon", None), dataDict.get("isInvoice", None),
                 dataDict.get("isComment", None), dataDict.get("userId", None))
    table = insertToSQL(UserOrder, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataUserOrder", methods=["POST"])
@jwt_required
@updateLog('zzh_user_order')
def updataUserOrder():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("orderId", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'orderId', u'orderType', u'orderStatus', u'orderServiceId', u'orderPoint', u'isCoupon',
                               u'isInvoice', u'isComment', u'userId']
    table = updataById(UserOrder, dataDict, "order_id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 进行中项目查询
@app.route("/findViewUserOrderByCondition", methods=["POST"])
@jwt_required
def findViewUserOrderByCondition():
    """
    进行中 1,2,3,4
    立项 5,7
    失败 -1,-2,-3,6
    1 派单中
    2 编写中
    3 报送中
    4 立项中
    5 立项成功
    6 立项失败
    7 归档
    -1: 关闭订单（用户关闭）
    -2：关闭订单（编写中）
    -3：关闭订单（报送中）
    :return:
    """
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = "view_internal_order_user_no"
    intColumnClinetNameList = [u'orderId', u'orderType', u'orderStatus', u'orderServiceId', u'orderPoint', u'isCoupon',
                               u'isInvoice', u'isComment', u'userId',"internalDeclareStatus"]
    tableList, count = conditionDataListFind(dataDict, view_internal_order_user_no_change, intColumnClinetNameList,
                                             tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = view_internal_order_user_no_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


def view_internal_order_user_no_fun(tableData):
    _infoDict = {
        "id": tableData[0],
        "taskId": tableData[1],
        "internalOrderNo": tableData[2],
        "orderNo": tableData[3],
        "internalDeclareStatus": tableData[4],
        "internalOrderType": tableData[5],
        "closeTime": tableData[6],
        "closePerson": tableData[7],
        "closeReason": tableData[8],
        "closeType": tableData[9],
        "orderId": tableData[10],
        "orderType": tableData[11],
        "orderFrom": tableData[12],
        "orderStatus": tableData[13],
        "declareStatus": tableData[14],
        "orderAddIp": tableData[15],
        "orderAddTime": tableData[16],
        "serviceId": tableData[17],
        "contactPerson": tableData[18],
        "contactPhone": tableData[19],
        "contactEmail": tableData[20],
        "orderMessage": tableData[21],
        "orderAmount": tableData[22],
        "payableAmount": tableData[23],
        "realAmount": tableData[24],
        "orderPoint": tableData[25],
        "isCoupon": tableData[26],
        "isInvoice": tableData[27],
        "isComment": tableData[28],
        "userId": tableData[29],}
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


view_internal_order_user_no_change = {
    "id": "id",
    "taskId": "task_id",
    "internalOrderNo": "internal_order_no",
    "orderNo": "order_no",
    "internalDeclareStatus": "internal_declare_status",
    "internalOrderType": "internal_order_type",
    "closeTime": "close_time",
    "closePerson": "close_person",
    "closeReason": "close_reason",
    "closeType": "close_type",
    "orderId": "order_id",
    "orderType": "order_type",
    "orderFrom": "order_from",
    "orderStatus": "order_status",
    "declareStatus": "declare_status",
    "orderAddIp": "order_add_ip",
    "orderAddTime": "order_add_time",
    "serviceId": "service_id",
    "contactPerson": "contact_person",
    "contactPhone": "contact_phone",
    "contactEmail": "contact_email",
    "orderMessage": "order_message",
    "orderAmount": "order_amount",
    "payableAmount": "payable_amount",
    "realAmount": "real_amount",
    "orderPoint": "order_point",
    "isCoupon": "is_coupon",
    "isInvoice": "is_invoice",
    "isComment": "is_comment",
    "userId": "user_id",
}

changeDict = {
    "orderId": "order_id",
    "orderNo": "order_no",
    "orderType": "order_type",
    "orderFrom": "order_from",
    "orderStatus": "order_status",
    "declareStatus": "declare_status",
    "orderAddIp": "order_add_ip",
    "orderAddTime": "order_add_time",
    "orderServiceId": "order_service_id",
    "contactPerson": "contact_person",
    "contactPhone": "contact_phone",
    "contactEmail": "contact_email",
    "orderMessage": "order_message",
    "orderAmount": "order_amount",
    "payableAmount": "payable_amount",
    "realAmount": "real_amount",
    "orderPoint": "order_point",
    "isCoupon": "is_coupon",
    "isInvoice": "is_invoice",
    "isComment": "is_comment",
    "userId": "user_id",
    "id": "id",
    "serviceName": "service_name",
    "policySource": "policy_source",
    "servicePrice": "service_price",
    "serviceStarttime": "service_starttime",
    "serviceDeadline": "service_deadline",
    "directionName": "direction_name",
    "serviceContent": "service_content",
    "sheetContent": "sheet_content",
    "materialList": "material_list",
    "forecastPath": "forecast_path",
    "serviceContactPerson": "service_contact_person",
    "serviceContactPhone": "service_contact_phone",
    "isSecular": "is_secular",
    "isEvaluate": "is_evaluate",
    "declareList": "declare_list",
    "categoryType": "category_type",
    "servciceProcess": "servcice_process",
    "itemId": "item_id",
    "deptName": "dept_name",
    "levelCode": "level_code",
    "categoryName": "category_name",
    "areaCode": "area_code",
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
    "createTime": "create_time",
    "isClose": "is_close",
    "itemDeadline": "item_deadline",
    "mediaType": "media_type",
    "mediaUrl": "media_url",
}
