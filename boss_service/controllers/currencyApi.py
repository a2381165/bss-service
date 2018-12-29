#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 0017 14:19
# @Site    : 
# @File    : currencyApi.py
# @Software: PyCharm
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required

from common.FormatStr import dictRemoveNone
from common.OperationOfDB import findById
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Boss.OrderAidance import OrderAidance
from models.Data.Aidance import Aidance
from models.Data.Item import Item
from models.Member.MemberBases import MemberBases
from models.Order.OrderService import OrderService
from models.Order.UserOrder import UserOrder
from version.v3.bossConfig import app
from common.getAreaCode import getAreaCode


@app.route("/getOrderInfo", methods=["POST"])
@jwt_required
def getOrderInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    orderNo = dataDict.get("orderNo", "")
    if not orderNo:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    orderInfo = findById(UserOrder, "order_no", orderNo, isStrcheck=True)
    if orderInfo:
        _orderDict = {
            "orderId": orderInfo.order_id,
            "orderNo": orderInfo.order_no,
            "orderType": orderInfo.order_type,
            "orderFrom": orderInfo.order_from,
            "orderStatus": orderInfo.order_status,
            "declareStatus": orderInfo.declare_status,
            "orderAddIp": orderInfo.order_add_ip,
            "orderAddTime": orderInfo.order_add_time,
            "serviceId": orderInfo.service_id,
            "contactPerson": orderInfo.contact_person,
            "contactPhone": orderInfo.contact_phone,
            "contactEmail": orderInfo.contact_email,
            "orderMessage": orderInfo.order_message,
            "orderAmount": str(orderInfo.order_amount),
            "payableAmount": str(orderInfo.payable_amount),
            "realAmount": str(orderInfo.real_amount),
            "orderPoint": orderInfo.order_point,
            "isCoupon": orderInfo.is_coupon,
            "isInvoice": orderInfo.is_invoice,
            "isComment": orderInfo.is_comment,
            "userId": orderInfo.user_id,
        }
        _orderDict = dictRemoveNone(_orderDict)
        resultDict = returnMsg(_orderDict)
    else:
        resultDict = returnErrorMsg(errorCode["query_fail"])
    return jsonify(resultDict)


@app.route("/getItemInfo", methods=["POST"])
@jwt_required
def getItemInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    itemId = dataDict.get("itemId", "")
    orderNo = dataDict.get("orderNo", "")
    if not (itemId or orderNo):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if itemId:
        itemInfo = findById(Item, 'item_id', "itemId")
    else:
        serviceInfo = findById(OrderService, "order_no", orderNo, isStrcheck=True)
        if serviceInfo:
            itemInfo = findById(Item, "item_id", serviceInfo.item_id, isStrcheck=True)
        else:
            itemInfo = None
    if itemInfo:
        _orderDict = {
            "itemId": itemInfo.item_id,
            "deptName": itemInfo.dept_name,
            "levelCode": itemInfo.level_code,
            "categoryName": itemInfo.category_name,
            "areaCode": itemInfo.area_code,
            "itemUrl": itemInfo.item_url,
            "itemTitle": itemInfo.item_title,
            "itemImgurl": itemInfo.item_imgurl,
            "itemPulishdate": itemInfo.item_pulishdate,
            "itemType": itemInfo.item_type,
            "itemSort": itemInfo.item_sort,
            "isTop": itemInfo.is_top,
            "isLock": itemInfo.is_lock,
            "isService": itemInfo.is_service,
            "isContentJson": itemInfo.is_content_json,
            # "createTime": itemInfo.create_time,
            "isClose": itemInfo.is_close,
            "itemDeadline": itemInfo.item_deadline,
            "isSecular": itemInfo.is_secular,
            "mediaType": itemInfo.media_type,
            "mediaUrl": itemInfo.media_url
        }
        _orderDict = dictRemoveNone(_orderDict)
        resultDict = returnMsg(_orderDict)
    else:
        resultDict = returnErrorMsg(errorCode["query_fail"])
    return jsonify(resultDict)


@app.route("/getOrderServiceInfo", methods=["POST"])
@jwt_required
def getOrderServiceInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    orderNo = dataDict.get("orderNo", "")
    if not (id or orderNo):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if id:
        serviceInfo = findById(OrderService, "id", id)
    else:
        serviceInfo = findById(OrderService, "order_no", orderNo, isStrcheck=True)
    if serviceInfo:
        _serviceDict = {
            "id": serviceInfo.id,
            # "orderNo": serviceInfo.order_no,
            # "itemId": serviceInfo.item_id,
            "serviceName": serviceInfo.service_name,
            "policySource": serviceInfo.policy_source,
            "servicePrice": str(serviceInfo.service_price),
            "serviceStarttime": serviceInfo.service_starttime,
            "serviceDeadline": serviceInfo.service_deadline,
            "directionName": serviceInfo.direction_name,
            "serviceContent": serviceInfo.service_content,
            "sheetContent": serviceInfo.sheet_content,
            "materialList": serviceInfo.material_list,
            "forecastPath": serviceInfo.forecast_path,
            "serviceContactPerson": serviceInfo.service_contact_person,
            "serviceContactPhone": serviceInfo.service_contact_phone,
            # "isSecular": serviceInfo.is_secular,
            "isEvaluate": serviceInfo.is_evaluate,
            "declareList": serviceInfo.declare_list,
            "createTime": serviceInfo.create_time,
            "categoryType": serviceInfo.category_type,
            "servciceProcess": serviceInfo.servcice_process,
        }
        _serviceDict = dictRemoveNone(_serviceDict)
        resultDict = returnMsg(_serviceDict)
    else:
        resultDict = returnErrorMsg(errorCode["query_fail"])
    return jsonify(resultDict)


@app.route("/getMemberInfo", methods=["POST"])
@jwt_required
def getMemberInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    orderNo = dataDict.get("orderNo", "")
    userId = dataDict.get("userId", "")
    if not (userId or orderNo):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if userId:
        userInfo = findById(MemberBases, "user_id", userId)
    else:
        orderInfo = findById(UserOrder, "order_no", orderNo, isStrcheck=True)
        if orderInfo:
            userInfo = findById(MemberBases, "user_id", orderInfo.user_id)
        else:
            userInfo = None
    if userInfo:
        areaName = ""
        if userInfo.area_code:
            provinceName, cityName, districtName = getAreaCode(userInfo.area_code)
            areaName = provinceName + cityName + districtName
        _memberInfo = {
            "userId": userInfo.user_id,
            "memberName": userInfo.member_name,
            "memberType": userInfo.member_type,
            "memberContactEmail": userInfo.member_contact_email,
            "memberContactPerson": userInfo.member_contact_person,
            "memberContactPhone": userInfo.member_contact_phone,
            "areaCode": userInfo.area_code,
            "areaName": areaName,
            "memberCreditCode": userInfo.member_credit_code,
        }
        _memberInfo = dictRemoveNone(_memberInfo)
        resultDict = returnMsg(_memberInfo)
    else:
        resultDict = returnErrorMsg(errorCode["query_fail"])
    return jsonify(resultDict)


# 订单项目 结合
@app.route("/getOrderItemInfo", methods=["POST"])
@jwt_required
def getOrderItemInfo():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    orderNo = dataDict.get("orderNo", "")
    if not orderNo:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    orderInfo = findById(UserOrder, "order_no", orderNo, isStrcheck=True)
    if not orderInfo:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    serviceInfo = findById(OrderService, "order_no", orderNo, isStrcheck=True)
    if serviceInfo:
        itemInfo = findById(Item, "item_id", serviceInfo.item_id, isStrcheck=True)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    _itemDict = {}
    _orderDict = {
        "orderId": orderInfo.order_id,
        "orderNo": orderInfo.order_no,
        "orderType": orderInfo.order_type,
        "orderFrom": orderInfo.order_from,
        "orderStatus": orderInfo.order_status,
        "declareStatus": orderInfo.declare_status,
        "orderAddIp": orderInfo.order_add_ip,
        "orderAddTime": orderInfo.order_add_time,
        "serviceId": orderInfo.service_id,
        "contactPerson": orderInfo.contact_person,
        "contactPhone": orderInfo.contact_phone,
        "contactEmail": orderInfo.contact_email,
        "orderMessage": orderInfo.order_message,
        "orderAmount": str(orderInfo.order_amount),
        "payableAmount": str(orderInfo.payable_amount),
        "realAmount": str(orderInfo.real_amount),
        "orderPoint": orderInfo.order_point,
        "isCoupon": orderInfo.is_coupon,
        "isInvoice": orderInfo.is_invoice,
        "isComment": orderInfo.is_comment,
        "userId": orderInfo.user_id,
    }
    if itemInfo:
        _itemDict = {
            "itemId": itemInfo.item_id,
            "deptName": itemInfo.dept_name,
            "levelCode": itemInfo.level_code,
            "categoryName": itemInfo.category_name,
            "areaCode": itemInfo.area_code,
            "itemUrl": itemInfo.item_url,
            "itemTitle": itemInfo.item_title,
            "itemImgurl": itemInfo.item_imgurl,
            "itemPulishdate": itemInfo.item_pulishdate,
            "itemType": itemInfo.item_type,
            "itemSort": itemInfo.item_sort,
            "isTop": itemInfo.is_top,
            "isLock": itemInfo.is_lock,
            "isService": itemInfo.is_service,
            "isContentJson": itemInfo.is_content_json,
            # "createTime": itemInfo.create_time,
            "isClose": itemInfo.is_close,
            "itemDeadline": itemInfo.item_deadline,
            "isSecular": itemInfo.is_secular,
            "mediaType": itemInfo.media_type,
            "mediaUrl": itemInfo.media_url
        }
    infoDict = dict(_orderDict, **_itemDict)
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)
