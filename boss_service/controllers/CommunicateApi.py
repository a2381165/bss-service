# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss, \
    executeSql
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Boss.Communicate import Communicate, CommunicateChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
import Res
from models.Data.SingleService import SingleService
from models.Data.WholeService import WholeService
from models.Data.MemberTempContract import MemberTempContract
from models.Member.EnterpriseInformation import EnterpriseInformation, EnterpriseInformationChangeDic
from common.OpenExcelData import main
from models.Member.MemberContract import MemberContract
from models.Order.UserInternalOrder import UserInternalOrder

# 获取 列表 已执行人
@app.route("/findCommunicateByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_communicate')
def findCommunicateByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [
        {
            "field": "executePerson",
            "op": "equal",
            "value": current_user.admin_name
        }
    ]
    for con in newList:
        condition.append(con)
    tablename = Communicate.__tablename__
    intColumnClinetNameList = intList
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = tableSortDict(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 删除
@app.route("/deleteCommunicate", methods=["POST"])
@jwt_required
@deleteLog('boss_communicate')
def deleteCommunicate():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(Communicate, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 商务经理 添加
@app.route("/addCommunicate", methods=["POST"])
@jwt_required
@addLog('boss_communicate')
def addCommunicate():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    orderNo = dataDict.get("orderNo", None)
    serviceNo = dataDict.get("serviceNo", None)
    productName = dataDict.get("productName", None)
    require = dataDict.get("require", None)
    projectPath = dataDict.get("projectPath", None)
    projectType = dataDict.get("projectType", 1)
    customerName = dataDict.get("customerName", None)
    executePerson = current_user.admin_name
    createPerson = current_user.admin_name
    executeTime = getTimeStrfTimeStampNow()
    createTime = getTimeStrfTimeStampNow()
    isDone = 0
    isSend = 2  # 自创
    chosoType = 0
    sourceType = 5
    serviceId = dataDict.get("serviceId", None)
    remark = dataDict.get("remark", None)
    if not customerName:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    columsStr = (serviceId,
                 orderNo, serviceNo, productName, require, projectPath, projectType, customerName, executePerson,
                 executeTime,
                 createPerson, createTime,
                 isSend, isDone, remark, chosoType, sourceType)
    dbOperation = OperationOfDB()
    table = dbOperation.insertToSQL(Communicate, *columsStr)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 更新
@app.route("/updataCommunicate", methods=["POST"])
@jwt_required
@updateLog('boss_communicate')
def updataCommunicate():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    chooseType = dataDict.get("addType", "")
    remark = dataDict.get("remark", None)
    if not (id and chooseType):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if not remark:
        resultDict = returnErrorMsg(errorCode["not_remark"])
        return jsonify(resultDict)
    dataDict["isDone"] = 1
    if dataDict.has_key("addType"):
        dataDict["chooseType"] = chooseType
    # 查询 Communicate
    table = findById(Communicate, "id", id)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if table.is_done == 1:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.has_key("addType"):
        dataDict.pop("addType")
    LocalProjectType = table.project_type
    dbOperation = OperationOfDB()
    """方案类型 
    1 开拓沟通、2 战略服务方案、3 单项服务方案、4战略合同、5 单项合同、6 单项立项沟通、7 单项结算"""
    now = getTimeStrfTimeStampNow()
    if chooseType != 1:
        if LocalProjectType == Res.projectType["ktgt"]:
            # 开拓沟通
            if chooseType == 2:
                # 任务 创建整理服务方案
                WholeServiceSTr = createWhole(table)
                WholeTable = dbOperation.insertToSQL(WholeService, *WholeServiceSTr)
                if not WholeTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg(errorCode["system_error"])
                    return jsonify(resultDict)
                # 创建沟通表
                projectType = 2
            elif chooseType == 3:
                # 任务 创建单项服务方案
                SingleServiceSTr = createSingle(table)
                singleTable = dbOperation.insertToSQL(SingleService, *SingleServiceSTr)
                if not singleTable:
                    dbOperation.commitRollback()
                    resultDict = returnErrorMsg(errorCode["system_error"])
                    return jsonify(resultDict)
                projectType = 3
            else:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["param_error"])
                return jsonify(resultDict)
        elif LocalProjectType == Res.projectType["zlfwfa"]:
            # 创建 战略合同草稿记录
            columsStr = createHt(table, 1)
            ContractTable = dbOperation.insertToSQL(MemberTempContract, *columsStr)
            if not ContractTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["param_error"])
                return jsonify(resultDict)
            projectType = 4
        elif LocalProjectType == Res.projectType["dxfwfa"]:
            # 创建 单项合同草稿记录
            columsStr = createHt(table, 2)
            ContractTable = dbOperation.insertToSQL(MemberTempContract, *columsStr)
            if not ContractTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["param_error"])
                return jsonify(resultDict)
            projectType = 5
        elif LocalProjectType == Res.projectType["zlht"]:
            # 创建 正式战略合同 and 生成资质待归档记录，待后续综合部归档操作
            projectType = None
            pass
        elif LocalProjectType == Res.projectType["dxht"]:
            # 生成正式单项合同并生成资质待归档记录，待后续综合部归档操作 以及生成订单
            tempContractInfo = MemberTempContract.query.filter(MemberTempContract.order_no==table.order_no).first()
            orderNo = tempContractInfo.order_no
            serviceNo = tempContractInfo.service_no
            itemTitle = tempContractInfo.item_title
            contractNo = tempContractInfo.contract_no
            contractAnnex = tempContractInfo.contract_annex
            contractRemark = tempContractInfo.contract_remark
            contractType = tempContractInfo.contract_type
            contractPrice = tempContractInfo.contract_price
            startFee = tempContractInfo.start_fee
            projectFee = tempContractInfo.project_fee
            projectRate = tempContractInfo.project_rate
            isGenerate = tempContractInfo.is_generate
            startTime = tempContractInfo.start_time
            endTime = tempContractInfo.end_time
            signingPerson = current_user.admin_name
            createPerson = current_user.admin_name
            createTime = now
            MemberContractStr = (
            orderNo, serviceNo, itemTitle, contractNo, contractAnnex, contractRemark, contractType, contractPrice,
            startFee, projectFee, projectRate, isGenerate, startTime, endTime, signingPerson, createPerson, createTime)
            MemberContractStr = dbOperation.insertToSQL(MemberContract, *MemberContractStr)
            if not MemberContractStr:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["param_error"])
                return jsonify(resultDict)
            # 内部订单
            task_id = None
            internal_order_no = table.order_no
            order_no = table.order_no
            internal_declare_status = 1
            internal_order_type = 1
            create_person = current_user.admin_name
            create_time = now
            execute_person = None
            execute_time = None
            is_done = 0
            close_time = None
            close_person = None
            close_reason = None
            close_type = None
            UserInternalOrderStr = (
                task_id, internal_order_no, order_no, internal_declare_status, internal_order_type, create_person,
                create_time, execute_person, execute_time, is_done, close_time, close_person, close_reason, close_type)
            InternalOrder = dbOperation.insertToSQL(UserInternalOrder, *UserInternalOrderStr)
            if not InternalOrder:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["insert_fail"])
                return jsonify(resultDict)
            projectType = None
        elif LocalProjectType == Res.projectType["dxlxgt"]:
            # 处理操作有两项A结束（生成单项结算沟通）B继续跟进并记录告诉客户立项及后续跟进（生成下次单项立项沟通）
            projectType = None
            pass
        elif LocalProjectType == Res.projectType["dxjs"]:
            projectType = None
            # 处理操作有两项A单项结束（更新客户单项结算状态）B继续跟进并记录结算沟通情况（生成下次单项结算沟通）
            pass
        else:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        # 创建 新沟通表
        if projectType:
            executePerson = current_user.admin_name
            createPerson = current_user.admin_name
            executeTime = now
            createTime = now
            isDone = 0
            isSend = 2
            remark = None
            chooseType = 0
            sourceType = table.source_type
            communicateStr = (table.service_id,
                              table.order_no, table.service_no, table.product_name, table.require, table.project_path,
                              projectType,
                              table.customer_name, executePerson, executeTime, createPerson,
                              createTime, isSend, isDone, remark, chooseType, sourceType)
            NextTable = dbOperation.insertToSQL(Communicate, *communicateStr)
            if not NextTable:
                dbOperation.commitRollback()
                resultDict = returnErrorMsg(errorCode["insert_fail"])
                return jsonify(resultDict)
    elif chooseType == 1:
        # 更新沟通表
        pass
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = dbOperation.updateThis(Communicate, Communicate.id, id, dataDict, tableChangeDic,
                                   intColumnClinetNameList=intColumnClinetNameList)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 获取 列表
@app.route("/findEnterpriseInformationByCondition", methods=["POST"])
@jwt_required
@queryLog('zzh_enterprise_information')
def findEnterpriseInformationByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = EnterpriseInformation.__tablename__
    intColumnClinetNameList = [u'id']
    tableList, count = conditionDataListFind(dataDict, EnterpriseInformationChangeDic, intColumnClinetNameList,
                                             tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "memberName": tableData[1],
                        "memberCreditCode": tableData[2],
                        "memberRegisteredAccount": tableData[3],
                        "memberOrganizationCode": tableData[4],
                        "memberProvince": tableData[5],
                        "memberUnitType": tableData[6],
                        "memberIndustry": tableData[7],
                        "memberLegalPerson": tableData[8],
                        "memberRegisteredCapital": tableData[9],
                        "memberRegisteredTime": tableData[10],
                        "memberBusinessStart": tableData[11],
                        "memberBusinessEnd": tableData[12],
                        "approvalAuthority": tableData[13],
                        "approvalDate": tableData[14],
                        "memberBusinessScope": tableData[15],
                        "memberMailingAddress": tableData[16],
                        "memberPhone": tableData[17],
                        "memberEmail": tableData[18],
                        "memberWebsite": tableData[19],
                        "memberStatus": tableData[20], }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


"""商务副部长"""


# 获取 列表 已创建人
@app.route("/findCreateCommunicateByCondition", methods=["POST"])
@jwt_required
@queryLog('boss_communicate')
def findCreateCommunicateByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [
        {
            "field": "createPerson",
            "op": "equal",
            "value": current_user.admin_name
        }
    ]
    for con in newList:
        condition.append(con)
    tablename = Communicate.__tablename__
    intColumnClinetNameList = intList
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = tableSortDict(tableData)
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务副部长 添加
@app.route("/addSwfbzCommunicate", methods=["POST"])
@jwt_required
def addSwfbzCommunicate():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    serviceId = dataDict.get("serviceId", None)
    orderNo = dataDict.get("orderNo", None)
    serviceNo = dataDict.get("serviceNo", None)
    productName = dataDict.get("productName", None)
    require = dataDict.get("require", None)
    projectPath = dataDict.get("projectPath", None)
    projectType = dataDict.get("projectType", 1)
    customerName = dataDict.get("customerName", None)
    executePerson = current_user.admin_name
    createPerson = current_user.admin_name
    executeTime = getTimeStrfTimeStampNow()
    createTime = getTimeStrfTimeStampNow()
    isDone = 0
    isSend = 0  # 自创
    chosoType = 0
    sourceType = 6  # 商务副部长自创
    remark = dataDict.get("remark", None)
    if not customerName:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    columsStr = (
        serviceId, orderNo, serviceNo, productName, require, projectPath, projectType, customerName, executePerson,
        executeTime,
        createPerson, createTime,
        isSend, isDone, remark, chosoType, sourceType)
    dbOperation = OperationOfDB()
    table = dbOperation.insertToSQL(Communicate, *columsStr)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 商务副部长 修改
@app.route("/updataSwfbzCommunicate", methods=["POST"])
@jwt_required
def updataSwfbzCommunicate():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = updataById(Communicate, dataDict, "id", id, tableChangeDic, intList)
    if table:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["update_fail"])
    return jsonify(resultDict)


# 商务副部长 分派
@app.route("/assignSwfbzCommunicate", methods=["POST"])
@jwt_required
def assignSwfbzCommunicate():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    executePerson = dataDict.get("executePerson", "")
    if not (id and executePerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    newDict = {"executePerson": executePerson, "executeTime": getTimeStrfTimeStampNow(), "isSend": 1}
    table = updataById(Communicate, newDict, "id", id, tableChangeDic, intList)
    if table:
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["update_fail"])
    return jsonify(resultDict)


# 商务副部长 真删除
@app.route("/deleteSwfbzCommunicate", methods=["POST"])
@jwt_required
def deleteSwfbzCommunicate():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss(Communicate, idList, "id")
    if count == len(idList):
        resultDict = returnMsg({})
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 商务副部长  假删除
@app.route("/deleteLocalCommunicate", methods=["POST"])
@jwt_required
def deleteLocalCommunicate():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    newDict = {"isSend": 3}
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.updateThis(Communicate, Communicate.id, id, newDict, tableChangeDic)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg({})
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)


# 商务副部长 导入
@app.route("/exportExcelCommunicate", methods=["POST"])
@jwt_required
def exportExcelCommunicate():
    file = request.files.get('file', None)
    if not (file):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    infoList = main(file)
    dbOperation = OperationOfDB()
    for info in infoList:
        pass
    return jsonify(infoList)


def createHt(table, contractType):
    now = getTimeStrfTimeStampNow()
    # 创建 战略合同草稿记录
    taskId = 0
    orderNo = table.order_no
    serviceNo = table.service_no
    contractNo = None
    contractName = table.require
    contractRemark = None
    productName = table.product_name
    contractPrice = None
    startFee = None
    projectFee = None
    projectRate = None
    # contractType = contractType  # 1 战略 2 单项
    startTime = None
    endTime = None
    createPerson = current_user.admin_name
    createTime = now
    executePerson = None
    executeTime = None
    isDone = 0
    columsStr = (
        taskId, orderNo, serviceNo, contractNo, contractName, contractRemark, productName, contractPrice, startFee,
        projectFee, projectRate, contractType, startTime, endTime, createPerson, createTime, executePerson,
        executeTime, isDone)
    return columsStr


def createWhole(table):
    now = getTimeStrfTimeStampNow()
    serviceAgency = Res.serviceAgency
    servicePerson = Res.servicePerson
    WholeServiceSTr = [None, table.service_id, table.customer_name, None, serviceAgency, servicePerson]  # 18+3
    WholeServiceSTr.extend([None, ] * 16)
    WholeServiceSTr[14] = 1
    WholeServiceSTr[17] = current_user.admin_name
    WholeServiceSTr[18] = now
    WholeServiceSTr[21] = 0
    return WholeServiceSTr


def createSingle(table):
    now = getTimeStrfTimeStampNow()
    serviceAgency = Res.serviceAgency
    servicePerson = Res.servicePerson
    SingleServiceSTr = [None, table.service_id, table.customer_name, serviceAgency, servicePerson]  # 18+3
    SingleServiceSTr.extend([None, ] * 17)
    SingleServiceSTr[14] = 1
    SingleServiceSTr[17] = current_user.admin_name
    SingleServiceSTr[18] = now
    SingleServiceSTr[21] = 0
    return SingleServiceSTr


def tableSort(table):
    infoDict = {
        "id": table.id,
        "orderNo": table.order_no,
        "serviceNo": table.service_no,
        "productName": table.product_name,
        "require": table.require,
        "projectPath": table.project_path,
        "projectType": table.project_type,
        "customerName": table.customer_name,
        "createPerson": table.create_person,
        "createTime": table.create_time,
        "isDone": table.is_done,
        "remark": table.remark,
        "chooseType": table.choose_type,
    }
    infoDict = dictRemoveNone(infoDict)
    return infoDict


def tableSortDict(tableData):
    _infoDict = {
        "id": tableData[0],
        "serviceId": tableData[1],
        "orderNo": tableData[2],
        "serviceNo": tableData[3],
        "productName": tableData[4],
        "require": tableData[5],
        "projectPath": tableData[6],
        "projectType": tableData[7],
        "customerName": tableData[8],
        "executePerson": tableData[9],
        "executeTime": tableData[10],
        "createPerson": tableData[11],
        "createTime": tableData[12],
        "isSend": tableData[13],
        "isDone": tableData[14],
        "remark": tableData[15],
        "chooseType": tableData[16],
        "sourceType": tableData[17],
    }
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict
