# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, current_user

from common.FormatStr import dictRemoveNone
from common.Log import queryLog
from common.OperationOfDB import conditionDataListFind
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Order.UserOrderEdit import UserOrderEdit
from version.v3.bossConfig import app


# 获取 列表
@app.route("/findUserOrderAndEditByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_edit')
def findUserOrderAndEditByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [{
        "field": "manageCounselorId",
        "op": "equal",
        "value": current_user.admin_id
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = UserOrderEdit.__tablename__
    intColumnClinetNameList = [u'orderId', u'orderType', u'orderStatus', u'orderItemId', u'orderServiceId',
                               u'orderPoint', u'isCoupon',
                               u'isInvoice', u'isComment', u'userId', u'id', u'editStatus', u'auditStatus',
                               u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, newChange, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"
            infoDict = {
                "orderId": tableData[0],
                "orderNo": tableData[1],
                "orderType": tableData[2],
                "orderStatus": tableData[3],
                "declareStatus": tableData[4],
                "orderAddIp": tableData[5],
                "orderAddTime": tableData[6],
                "orderItemId": tableData[7],
                "orderServiceId": tableData[8],
                "contactPerson": tableData[9],
                "contactPhone": tableData[10],
                "contactEmail": tableData[11],
                "orderMessage": tableData[12],
                "orderAmount": tableData[13],
                "payableAmount": tableData[14],
                "realAmount": tableData[15],
                "orderPoint": tableData[16],
                "isCoupon": tableData[17],
                "isInvoice": tableData[18],
                "isComment": tableData[19],
                "userId": tableData[20],
                "serviceNo": tableData[21],
                "itemTitle": tableData[22],
                "specificFund": str(tableData[23]),
                "editStatus": tableData[24],
                "editRemark": tableData[25],
                "auditPerson": tableData[26],
                "auditTime": tableData[27],
                "auditStatus": tableData[28],
                "auditRemark": tableData[29],
                "counselorId": tableData[30],
                "manageCounselorId": tableData[31],
                "requireList": tableData[32],
                "manuscriptTime": tableData[33],
                "declareName": tableData[34],
                "editTime": tableData[35],
                "editAnnex": tableData[36],
                "id": tableData[37],
                "itemContent": itemContent,
            }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


newChange = {
    "orderId": "order_id",
    "orderNo": "order_no",
    "orderType": "order_type",
    "orderStatus": "order_status",
    "declareStatus": "declare_status",
    "orderAddIp": "order_add_ip",
    "orderAddTime": "order_add_time",
    "orderItemId": "order_item_id",
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
    "serviceNo": "service_no",
    "itemTitle": "item_title",
    "specificFund": "specific_fund",
    "editStatus": "edit_status",
    "editRemark": "edit_remark",
    "auditPerson": "audit_person",
    "auditTime": "audit_time",
    "auditStatus": "audit_status",
    "auditRemark": "audit_remark",
    "counselorId": "counselor_id",
    "manageCounselorId": "manage_counselor_id",
    "requireList": "require_list",
    "manuscriptTime": "manuscript_time",
    "declareName": "declare_name",
    "editTime": "edit_time",
    "editAnnex": "edit_annex",
    "id": "id",
}
