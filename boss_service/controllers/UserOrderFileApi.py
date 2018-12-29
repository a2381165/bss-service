# coding:utf-8

from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, current_user

from common.DatatimeNow import returnEmailCodeTime
from common.FormatStr import dictRemoveNone
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.OrderCommon import addDeclareStatus
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Order.UserOrder import UserOrder
from models.Order.UserOrderAssign import UserOrderAssign
from models.Order.UserOrderComment import UserOrderComment
from models.Order.UserOrderFile import UserOrderFile, UserOrderFileChangeDic as tableChangeDic
from version.v3.bossConfig import app


# 获取 列表
@app.route("/findUserOrderFileByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_file')
def findUserOrderFileBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [{
        "field": "counselorId",
        "op": "equal",
        "value": current_user.admin_id
    }]
    for newDict in newList:
        condition.append(newDict)
    tablename = UserOrderFile.__tablename__
    intColumnClinetNameList = [u'id', u'fileStatus', u'projectStatus', u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "specificFund": tableData[4],
                        "fileStatus": tableData[5],
                        "fileDate": tableData[6],
                        "projectStatus": tableData[7],
                        "projectCode": tableData[8],
                        "projectFund": tableData[9],
                        "projectDate": tableData[10],
                        "fileAnnex": tableData[11],
                        "fileRemark": tableData[12],
                        "counselorId": tableData[13],
                        "manageCounselorId": tableData[14],
                        "requireList": tableData[15],
                        "itemContent": itemContent,
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取 列表
@app.route("/findFBUserOrderFileByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_file')
def findFBUserOrderFileByCondition():
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
    tablename = UserOrderFile.__tablename__
    intColumnClinetNameList = [u'id', u'fileStatus', u'projectStatus', u'counselorId', u'manageCounselorId']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            itemContent = "%5B%7B%22titleItem%22:%22%E9%A3%8E%E6%A0%BC%E6%81%A2%E5%A4%8D%E9%AC%BC%E7%94%BB%E7%AC%A6%E4%B8%AA%22,%22storItem%22:1,%22contactItem%22:%22%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%E9%A3%8E%E6%A0%BC%E5%8C%96%22%7D,%7B%22titleItem%22:%22%E4%BD%86%E6%98%AF%E5%8F%91%E5%B0%84%E7%82%B9%E5%8F%91%E5%B0%84%E7%82%B9%22,%22storItem%22:2,%22contactItem%22:%22%E5%9C%B0%E6%96%B9%E9%83%BD%E6%98%AF%E6%B3%95%E5%9B%BD%E5%8F%8C%E9%A3%9E%E7%9A%84%E6%AD%8C%22%7D%5D"
            infoDict = {"id": tableData[0],
                        "orderNo": tableData[1],
                        "serviceNo": tableData[2],
                        "itemTitle": tableData[3],
                        "specificFund": tableData[4],
                        "fileStatus": tableData[5],
                        "fileDate": tableData[6],
                        "projectStatus": tableData[7],
                        "projectCode": tableData[8],
                        "projectFund": tableData[9],
                        "projectDate": tableData[10],
                        "fileAnnex": tableData[11],
                        "fileRemark": tableData[12],
                        "counselorId": tableData[13],
                        "manageCounselorId": tableData[14],
                        "requireList": tableData[15],
                        "itemContent": itemContent,
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取详情
@app.route("/getUserOrderFileDetail", methods=["POST"])
@jwt_required
@queryLog('zzh_user_order_file')
def getUserOrderFileDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(UserOrderFile, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.id,
                "orderNo": table.order_no,
                "serviceNo": table.service_no,
                "itemTitle": table.item_title,
                "specificFund": table.specific_fund,
                "fileStatus": table.file_status,
                "fileDate": table.file_date,
                "projectStatus": table.project_status,
                "projectCode": table.project_code,
                "projectFund": table.project_fund,
                "projectDate": table.project_date,
                "fileAnnex": table.file_annex,
                "fileRemark": table.file_remark,
                "counselorId": table.counselor_id,
                "manageCounselorId": table.manage_counselor_id,
                "requireList": table.require_list, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/deleteUserOrderFile", methods=["POST"])
@jwt_required
@deleteLog('zzh_user_order_file')
def deleteUserOrderFile():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(UserOrderFile, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加 
@app.route("/addUserOrderFile", methods=["POST"])
@jwt_required
@addLog('zzh_user_order_file')
def addUserOrderFile():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("orderNo", None), dataDict.get("serviceNo", None), dataDict.get("itemTitle", None),
                 dataDict.get("specificFund", None), dataDict.get("fileStatus", None), dataDict.get("fileDate", None),
                 dataDict.get("projectStatus", None), dataDict.get("projectCode", None),
                 dataDict.get("projectFund", None), dataDict.get("projectDate", None), dataDict.get("fileAnnex", None),
                 dataDict.get("fileRemark", None), dataDict.get("counselorId", None),
                 dataDict.get("manageCounselorId", None), dataDict.get("requireList", None))
    table = insertToSQL(UserOrderFile, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新 
@app.route("/updataUserOrderFile", methods=["POST"])
@jwt_required
@updateLog('zzh_user_order_file')
def updataUserOrderFile():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'fileStatus', u'projectStatus', u'counselorId', u'manageCounselorId']
    table = updataById(UserOrderFile, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 更新项目归档 并评价 记录表
@app.route("/updateUserOrderFile", methods=["POST"])
@jwt_required
def updateUserOrderFile():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columnId = "id"
    intColumnClinetNameList = ("id", "projectStatus")
    idList = dataDict.get("ids", None)
    attitudeEva = dataDict.get("attitudeEva", 0)
    qualityEva = dataDict.get("qualityEva", 0)
    efficiencyEva = dataDict.get("efficiencyEva", 0)
    commentContent = dataDict.get("commentContent", None)
    isAnonymous = dataDict.get("isAnonymous", 1)
    keys = ["attitudeEva", "qualityEva", "efficiencyEva", "commentContent", "isAnonymous"]
    for key in dataDict.keys():
        if key in keys:
            dataDict.pop(key)
    infoList = []
    if not idList:
        resultDict = returnErrorMsg("not find ids!")
        return jsonify(resultDict)

    adminId = current_user.admin_id
    adminRealName = current_user.admin_real_name
    dbOperation = OperationOfDB()
    for id in idList:
        menuUp = dbOperation.updateThis(UserOrderFile, UserOrderFile.id, id, dataDict, tableChangeDic)
        if not menuUp:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("update fail")
            return jsonify(resultDict)
        serviceNo = menuUp.service_no
        # 派单状态 更改为4  正常 完成
        assignInfo = findById(UserOrderAssign, "service_no", serviceNo, isStrcheck=True)
        if assignInfo:
            assignInfo.assgin_status = 4
            dbOperation.addTokenToSql(assignInfo)

        orderNo = menuUp.order_no
        orderInfo = findById(UserOrder, "order_no", orderNo, isStrcheck=True)
        if not orderInfo:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("not find order")
            return jsonify(resultDict)
        decStatus = orderInfo.declare_status
        if decStatus[4] == "2":
            declareStatus = "0001211111"
        else:
            declareStatus = "0001111111"
        declareTable = addDeclareStatus(orderNo, dbOperation, declareStatus)
        if not declareTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg("not update fail")
            return jsonify(resultDict)
        counselorId = menuUp.counselor_id
        commentTime, exipireTime = returnEmailCodeTime()
        attitudeEvaList = (
        orderNo, 3, adminId, adminRealName, attitudeEva, commentContent, 1, commentTime, isAnonymous, counselorId)
        attitudeEvaTable = dbOperation.insertToSQL(UserOrderComment, *attitudeEvaList)
        efficiencyEvaList = (
            orderNo, 3, adminId, adminRealName, efficiencyEva, commentContent, 2, commentTime, isAnonymous, counselorId)
        efficiencyEvaTable = dbOperation.insertToSQL(UserOrderComment, *efficiencyEvaList)
        qualityEvaList = (
        orderNo, 3, adminId, adminRealName, qualityEva, commentContent, 3, commentTime, isAnonymous, counselorId)
        qualityEvaTable = dbOperation.insertToSQL(UserOrderComment, *qualityEvaList)
        if not (attitudeEvaTable and efficiencyEvaTable and qualityEvaTable):
            dbOperation.commitRollback()
            orderNo = menuUp.order_no
            orderInfo = findById(UserOrder, "order_no", orderNo, isStrcheck=True)
            if not orderInfo:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("not find order")
                return jsonify(resultDict)
            decStatus = orderInfo.declare_status
            if decStatus[4] == "2":
                declareStatus = "0002211111"
            else:
                declareStatus = "0002111111"
            declareTable = addDeclareStatus(orderNo, dbOperation, declareStatus)
            if not declareTable:
                resultDict = returnErrorMsg(" update fail")
                return jsonify(resultDict)
            resultDict = returnErrorMsg("insert comment fail")
            return jsonify(resultDict)
        if dbOperation.commitToSQL():
            infoList.append({})
        else:
            dbOperation.commitRollback()
            orderNo = menuUp.order_no
            orderInfo = findById(UserOrder, "order_no", orderNo, isStrcheck=True)
            if not orderInfo:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg("not find order")
                return jsonify(resultDict)
            decStatus = orderInfo.declare_status
            if decStatus[4] == "2":
                declareStatus = "0002211111"
            else:
                declareStatus = "0002111111"
            declareTable = addDeclareStatus(orderNo, dbOperation, declareStatus)
            if not declareTable:
                resultDict = returnErrorMsg(" update fail")
                return jsonify(resultDict)
            resultDict = returnErrorMsg("update fail")
            return jsonify(resultDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)