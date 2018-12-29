# coding:utf-8
import os

data2 = """# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate, getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg, errorCode
from version.v3.bossConfig import app
from models.Channel.{ModelName} import {ModelName}, {ModelName}ChangeDic as tableChangeDic, intList
from common.Log import queryLog, addLog, deleteLog, updateLog
import Res
from models.Data.SubFlow import SubFlow
from common.FlowCommon import sendUp, returnUp
from models.Data.Aidance import Aidance
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic, intList as aidanceCheckIntList
from common.FlowCommon import getFlowSort
# 添加 
@app.route("/add{ModelName}", methods=["POST"])
@jwt_required
@addLog('{tablename}')
def add{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
{dateDict}
    columsStr = ({ldateDict})
    table = insertToSQL({ModelName}, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg(\b\a)
    return jsonify(resultDict)


# 获取详情
@app.route("/get{ModelName}Detail", methods=["POST"])
@jwt_required
@queryLog('data_single_service')
def get{ModelName}Detail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById({ModelName}, "id", id)
    if not table:
        resultDict =  returnErrorMsg(errorCode["query_fail"])
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 商务经理 渠道商列表 待上报 已上报 已成功
@app.route("/find{ModelName}ByCondition", methods=["POST"])
@jwt_required
@queryLog('channel_user_task')
def find{ModelName}ByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [\b
        "field": "createPerson",
        "op": "equal",
        "value": current_user.admin_name
    \a]
    for newDict in newList:
        condition.append(newDict)
    tablename = {ModelName}.__tablename__
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename,
                                             orderByStr=orderByStr)
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


# 商务经理 被退回 列表
@app.route("/findViewInner{ModelName}ByCondition", methods=["POST"])
@jwt_required
def findViewInner{ModelName}ByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    newList = [\b
        "field": "createPerson",
        "op": "equal",
        "value": current_user.admin_name
    \a]
    for newDict in newList:
        condition.append(newDict)
    tablename = "{view_table_name}" # view_aidance_check_channel_user
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc "
    tableList, count = conditionDataListFind(dataDict, {view_table_name}_change, intColumnClinetNameList,
                                             tablename,
                                             orderByStr=orderByStr)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {view_table_name}_fun(tableData)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 合同中间人 列表
@app.route("/findView{ModelName}ByCondition", methods=["POST"])
@jwt_required
def findView{ModelName}ByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    roleId = dataDict.get("roleId", None)
    if not ((dataDict.has_key("condition")) and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    condition = dataDict.get("condition")
    flowId = Res.workFlow["{flowId}"]
    sort = getFlowSort(flowId,roleId)
    if not sort:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    # 传入 flowId and checkStatus
    newDictList = [\b
        "field": "checkPerson",
        "op": "equal",
        "value": current_user.admin_name
    \a, \b
        "field": "sort",
        "op": "equal",
        "value": sort
    \a]
    for newDict in newDictList:
        condition.append(newDict)
    tableName = "{view_table_name}"
    intColumnClinetNameList = ["sort", u'id', u'flowId', u'checkId', u'fromId', u'serviceId', u'flowStep',
                               u'acceptStatus',
                               u'isDone', u'aidanceCheckId', u'aidanceId', u'checkType', u'checkStatus', u'isCheck',
                               "taskType"]

    orderByStr = " order by create_time desc"
    resultList, count = conditionDataListFind(dataDict, {view_table_name}_change,
                                              intColumnClinetNameList=intColumnClinetNameList,
                                              tableName=tableName, orderByStr=orderByStr)
    if resultList:
        infoList = []
        for tableData in resultList:
            _infoDict = {view_table_name}_fun(tableData)
            infoList.append(_infoDict)
        resultDict = returnMsg(infoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 商务经理送审  # 上报
@app.route("/updataUp{ModelName}CheckStatus", methods=["POST"])
@jwt_required
def updataUp{ModelName}CheckStatus():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")  # 单项服务id
    roleId = dataDict.get("roleId", "")
    choicePerson = dataDict.get("choicePerson", "")
    if not (idList and roleId):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = findById({ModelName}, "id", id)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        reslut = sendUp(table, choicePerson, dbOperation, flowId=Res.workFlow["{flowId}"], taskType=None)
        if not reslut:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(\b\a)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 更新 完善 并上报
@app.route("/updata{ModelName}", methods=["POST"])
@jwt_required
def updata{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get('checkStatus', "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    dbOperation = OperationOfDB()
    table = dbOperation.updateThis({ModelName}, {ModelName}.id, id, dataDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if checkStatus == 2:
        reslut = sendUp(table, None, dbOperation, flowId=Res.workFlow["{flowId}"], taskType=None)
        if not reslut:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(\b\a)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)

# 退回 重新上报
@app.route("/updataUpReturn{ModelName}", methods=["POST"])
@jwt_required
def updataUpReturn{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus")
    choicePerson = dataDict.get("choicePerson", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    dbOperation = OperationOfDB()
    aidanceTable = findById(Aidance, "id", id)
    if not aidanceTable:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    serviceId = aidanceTable.service_id
    table = dbOperation.updateThis({ModelName}, {ModelName}.id, serviceId, dataDict, tableChangeDic)
    if not table:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["update_fail"])
        return jsonify(resultDict)
    if checkStatus == 2:
        result = returnUp(aidanceTable,table, dbOperation, choicePerson)
        if not result:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(\b\a)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 退回 上报
@app.route("/sendUpReturn{ModelName}", methods=["POST"])
@jwt_required
def sendUpReturn{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    choicePerson = dataDict.get("choicePerson", "")
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    popList = ["choicePerson", "checkStatus"]
    for popStr in popList:
        if dataDict.has_key(popStr):
            dataDict.pop(popStr)
    dbOperation = OperationOfDB()
    for id in idList:
        aidanceTable = findById(Aidance, "id", id)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceId = aidanceTable.service_id
        table = findById({ModelName}, "id", serviceId)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        result = returnUp(aidanceTable,table, dbOperation, choicePerson)
        if not result:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(\b\a)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)



#  商务合同 转移给其他商务经理
@app.route("/{ModelName}TransferOtherPerson", methods=["POST"])
@jwt_required
def {ModelName}TransferOtherPerson():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", "")
    createPerson = dataDict.get("createPerson", "")
    if not (idList and createPerson):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    for id in idList:
        table = dbOperation.updateThis({ModelName}, {ModelName}.id, id, dataDict,
                                       tableChangeDic)
        if not table:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(\b\a)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)


# 删除 
@app.route("/delete{ModelName}", methods=["POST"])
@jwt_required
@deleteLog('{tablename}')
def delete{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss({ModelName}, idList, "id")
    if count == len(idList):
        resultDict = returnMsg(\b\a)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)




# 总经理同意
@app.route("/finallyCheck{ModelName}", methods=["POST"])
@jwt_required
def finallyCheck{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    checkStatus = dataDict.get("checkStatus", "")
    if not (id and checkStatus):
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    if dataDict.has_key("roleId"):
        dataDict.pop("roleId")
    aidanceTable = findById(Aidance, "id", id)
    if not aidanceTable:
        resultDict = returnErrorMsg(errorCode["query_fail"])
        return jsonify(resultDict)
    dbOperation = OperationOfDB()
    now = getTimeStrfTimeStampNow()
    if checkStatus == Res.AuditCode["pass"]:
        # 更新 aidance
        aidanceTable.accept_status = 1
        aidanceTable.execute_person = current_user.admin_name
        aidanceTable.is_done = 2
        aidanceTable.complete_time = now
        aidanceTable.flow_step += 1
        aidanceTable = dbOperation.addTokenToSql(aidanceTable)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)
        serviceId = aidanceTable.service_id
        # 更新 明细
        serviceTable = dbOperation.findById({ModelName}, "id", serviceId)
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
        serviceTable.is_done = 2
        if not serviceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["update_fail"])
            return jsonify(resultDict)

        # communicateInfo = dbOperation.insertToSQL(Communicate, *CommunicateStr)
        # if not communicateInfo:
        #     dbOperation.commitRollback()
        #     resultDict = returnErrorMsg(errorCode["param_error"])
        #     return jsonify(resultDict)
    elif checkStatus == Res.AuditCode["fail"]:
        aidanceTable.flow_step = 1
        aidanceTable = dbOperation.addTokenToSql(aidanceTable)
        if not aidanceTable:
            dbOperation.commitRollback()
            resultDict = returnErrorMsg(errorCode["query_fail"])
            return jsonify(resultDict)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    checkId = aidanceTable.check_id
    intColumnClinetNameList = aidanceCheckIntList
    checkInfo = dbOperation.updateThis(AidanceCheck, AidanceCheck.id, checkId, dataDict, AidanceCheckChangeDic,
                                       intColumnClinetNameList=intColumnClinetNameList)
    if not checkInfo:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["update_fail"])
        return jsonify(resultDict)
    if dbOperation.commitToSQL():
        resultDict = returnMsg(\b\a)
    else:
        dbOperation.commitRollback()
        resultDict = returnErrorMsg(errorCode["commit_fail"])
    return jsonify(resultDict)

# NewAidanceApi.py checkAidanceCheck

def tableSort(table):
    _infoDict = \b{tableDict}\a
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = \b{tableData}\a
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def {view_table_name}_fun(tableData):
    _infoDict = \b\a
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


{view_table_name}_change = \b\a"""

# ModelName,ModelName,ModelName,ModelName,ModelName,IntFiled,infoDict,ModelName,ModelName,ModelName,tableDict,ModelName,ModelName,ModelName
data = """# coding:utf-8
from flask import jsonify, json, request
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from common.DatatimeNow import getTimeToStrfdate,getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById,deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.{Boss}.{ModelName} import {ModelName}, tableChangeDic,intList
from common.Log import queryLog,addLog,deleteLog,updateLog



# 获取 列表 
@app.route("/find{ModelName}ByCondition", methods=["POST"])
@jwt_required
@queryLog('{tablename}')
def find{ModelName}ByCondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = {ModelName}.__tablename__
    intColumnClinetNameList = intList
    orderByStr = " order by create_time desc " 
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename,orderByStr=orderByStr)
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


# 获取详情 
@app.route("/get{ModelName}Detail", methods=["POST"])
@jwt_required
@queryLog('{tablename}')
def get{ModelName}Detail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("{Aid}", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById({ModelName}, "{id}", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = tableSort(table)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除 
@app.route("/delete{ModelName}", methods=["POST"])
@jwt_required
@deleteLog('{tablename}')
def delete{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    idList = dataDict.get("ids", [])
    if not idList:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    count = deleteByIdBoss({ModelName}, idList, "id")
    if count == len(idList):
        resultDict = returnMsg(\b\a)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)



# 添加 
@app.route("/add{ModelName}", methods=["POST"])
@jwt_required
@addLog('{tablename}')
def add{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
{dateDict}
    columsStr = ({ldateDict})
    table = insertToSQL({ModelName}, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    resultDict = returnMsg(\b\a)
    return jsonify(resultDict)



# 更新 
@app.route("/updata{ModelName}", methods=["POST"])
@jwt_required
@updateLog('{tablename}')
def updata{ModelName}():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("{Aid}", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = intList
    table = updataById({ModelName}, dataDict, "{id}", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg(\b\a)
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

def tableSort(table):
    _infoDict = \b{tableDict}\a
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict


def tableSortDict(tableData):
    _infoDict = \b{tableData}\a
    _infoDict = dictRemoveNone(_infoDict)
    return _infoDict

"""


class CreateApi:
    def __init__(self, db, dbname):
        self.db = db
        self.dbname = dbname
        self.integer = ["int", "bigint", "tinyint"]
        self.intList = []
        self.first = True
        self.id = None

    # 查询所有字段
    def list_col(self, table_name):
        fieldsList = self.db.engine.execute(
            "select column_name,data_type,character_maximum_length from information_schema.columns where  table_schema='{}' and table_name='{}'".format(
                self.dbname, table_name))
        col_name_dict = {}
        col_name_list = []
        col_name_num = {}
        for tuple in fieldsList:
            col_name_list.append(tuple[0])
            col_name_dict[tuple[0]] = tuple[1]
            col_name_num[tuple[0]] = tuple[2]
        return col_name_dict, col_name_num, col_name_list

    # 列出所有的表
    def list_table(self):
        " SELECT  *  FROM  information_schema.views"
        "information_schema.tables"
        tableList = self.db.engine.execute(
            "select TABLE_NAME,row_format from information_schema.tables where TABLE_TYPE='BASE TABLE' and table_schema='{}'".format(
                self.dbname))
        table_list = []
        for tuple in tableList:
            table_list.append(tuple[0])
        return table_list

    # 大写
    def normalize(self, name):
        return name.capitalize()

    # 大写模型名
    def getName(self, tablename):
        if self.dataType in tablename:
            modelName = tablename.replace(self.dataType, "")
            list_k = modelName.split('_')
            try:
                z = map(self.normalize, list_k)
                modelName = ''.join(z)
                # modelName = ''.join([list_k[0], z])
            except:
                modelName = ''
        elif "_" in tablename:
            list_k = tablename.split('_')
            try:
                # z = map(self.normalize, list_k[1:])
                z = map(self.normalize, list_k)
                modelName = ''.join(z)
                # modelName = ''.join([list_k[0], z])
            except:
                modelName = ''
        else:
            modelName = self.normalize(tablename)
        return modelName

    def creatModel(self, table, models):
        self.intList = []
        self.first = True
        dirpath = os.getcwd()
        tablename = table
        modelName = self.getName(tablename)
        file = "{}Api.py".format(modelName)
        filepath = os.path.join(dirpath, file)
        try:
            with open(filepath, "w+") as f:
                f.write(models)
            f.close()
            return True
        except Exception as e:
            print (e)
            return False

    def datafl(self):
        dataDict = []
        tableDict = []
        tableData = []
        ldateDict = []
        fileds = ",".join(self.col_name_list)
        q = 0
        for x in self.col_name_list:
            # changeDict
            list_k = x.split('_')
            try:
                z = map(self.normalize, list_k[1:])
                z = ''.join(z)
            except:
                z = ''
            z = ''.join([list_k[0], z])
            ldateDict.append(z)
            if self.first:
                tableDict.append('"{}":table.{},'.format(z, x))  # "id": table.id,
                tableData.append('"{}":tableData[{}],'.format(z, q))  # "id": tableData[0],
                self.first = False
            else:
                dataDict.append('    {} = dataDict.get("{}", None)'.format(z, z))  # dataDict.get("xx", None)
                tableDict.append('                "{}":table.{},'.format(z, x))  # "id": table.id,
                tableData.append('                "{}":tableData[{}],'.format(z, q))  # "id": tableData[0],
            q += 1
            if 'id' == x:
                self.intList.append(z)
                self.id = x
            elif x == self.col_name_list[0]:
                self.intList.append(z)
                self.id = x
            elif self.col_name_dict[x] in self.integer:
                self.intList.append(z)
            idList = self.id.split('_')
            try:
                id = map(self.normalize, idList[1:])
                id = ''.join(id)
            except:
                id = ''
            self.Aid = ''.join([idList[0], id])
        dataDict = "\n".join(dataDict)
        tableDict = "\n".join(tableDict)
        tableData = "\n".join(tableData)
        ldateDict = ",".join(ldateDict)

        return dataDict, tableDict, tableData, ldateDict

    def main(self, tablename=[], dataType="data_", dataModel=1,flowId=None):
        table_list = self.list_table()
        self.dataType = dataType
        dataType = self.normalize(dataType.replace("_", ""))
        if tablename:
            for table in tablename:
                if table in table_list:
                    if dataModel == 1:
                        models = data
                    elif dataModel == 2:
                        models = data2
                    else:
                        models = data

                    self.col_name_dict, self.col_name_num, self.col_name_list = self.list_col(table)
                    try:
                        dataDict, tableDict, tableData, ldateDict = self.datafl()
                        tablename = table
                        ModelName = self.getName(tablename)
                        view_table_name = "view_aidance_check_" + tablename.replace(self.dataType, "")
                        models = models.format(Boss=dataType, ModelName=ModelName, IntFiled=self.intList,
                                               dateDict=dataDict,
                                               tableData=tableData, tableDict=tableDict, id=self.id,
                                               Aid=self.Aid, tablename=tablename, ldateDict=ldateDict,
                                               view_table_name=view_table_name,flowId=flowId).replace("\b",
                                                                                        "{").replace(
                            "\a", "}")
                        if self.creatModel(table, models):
                            print ("success", table)
                        else:
                            print("fail", table)

                    except Exception as e:
                        print (e)
                        print (table)
        else:
            for table in table_list:
                models = data
                self.col_name_dict, self.col_name_num, self.col_name_list = self.list_col(table)
                try:
                    dataDict, tableDict, tableData, ldateDict = self.datafl()
                    tablename = table
                    ModelName = self.getName(tablename)
                    models = models.format(Boss=dataType, ModelName=ModelName, IntFiled=self.intList, dateDict=dataDict,
                                           tableData=tableData, tableDict=tableDict, id=self.id, Aid=self.Aid,
                                           tablename=tablename, ldateDict=ldateDict).replace(
                        "\b", "{").replace("\a", "}")
                    if self.creatModel(table, models):
                        print ("success", table)
                    else:
                        print("fail", table)

                except Exception as e:
                    print (e)
                    print (table)

# if __name__ == '__main__':
