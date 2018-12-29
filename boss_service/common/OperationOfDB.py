# -*- coding: utf-8 -*-
from config import db, logger, app
from sqlalchemy import text
from flask import request
from flask_jwt_extended import get_jwt_identity


def querySql(sqlStr, isOther=False):
    try:
        sqlStr = text(sqlStr)
        logger.info("query info by:%s" % request.remote_addr)
        logger.info(sqlStr)
        if not isOther:
            queryList = db.engine.execute(sqlStr)
        else:
            queryList = db.session.execute(sqlStr, bind=db.get_engine(app, bind="crawler")).fetchall()
        count = 0
        for countList in queryList:
            count = countList[0]
        return count
    except Exception, e:
        logger.error("querySql")
        logger.error(e)
        return False


def executeSql(sqlStr, isOther=True, bind=""):
    try:
        sqlStr = text(sqlStr)
        logger.info("query info by:%s" % request.remote_addr)
        logger.info(sqlStr)
        if isOther:
            queryList = db.engine.execute(sqlStr)
        else:
            queryList = db.session.execute(sqlStr, bind=db.get_engine(app, bind=bind)).fetchall()
        return queryList
    except Exception, e:
        logger.error("executeSql")
        logger.error(e)
        return False


def executeSqlFirst(sqlStr, isOther=True, bind=""):
    try:
        sqlStr = text(sqlStr)
        logger.info("query info by:%s" % request.remote_addr)
        logger.info(sqlStr)
        if isOther:
            queryList = db.engine.execute(sqlStr).first()
        else:
            queryList = db.session.execute(sqlStr, bind=db.get_engine(app, bind=bind)).first()
        return queryList
    except Exception, e:
        logger.error("executeSql")
        logger.error(e)
        return False


def sqlFunctionCallOther(sqlStr):
    try:
        sqlStr = text(sqlStr)
        logger.info("update by:%s" % request.remote_addr)
        logger.info(sqlStr)
        adminsList = db.session.execute(sqlStr, bind=db.get_engine(app, bind="crawler"))
        resualtList = adminsList.first()
        return list(resualtList)
    except Exception, e:
        logger.error("sqlFunctionCallOther")
        logger.error(e)
        return None


def sqlOrderPayDo(sqlStr):
    try:
        sqlStr = text(sqlStr)
        logger.info("payment info by:%s" % request.remote_addr)
        logger.info(sqlStr)
        db.engine.execute(sqlStr)
        return True
    except Exception, e:
        logger.error("sqlOrderPayDo")
        logger.error(e)
        return False


def insertOrderMethodExecute(sqlStr):
    try:
        sqlStr = text(sqlStr)
        logger.info("insert by:%s" % request.remote_addr)
        logger.info(sqlStr)
        adminsList = db.engine.execute(sqlStr)
        if adminsList:
            return True
        return False
    except Exception, e:
        logger.error("insertOrderMethodExecute")
        logger.error(e)
        return False


# 跟新数据
# table 类名,dict1 要跟新的数据字典 ,columnId 表id名（如：admin_id）
# id id值 ,adminChangeDic 客户端与数据库表头对应字典
# intColumnClinetNameList 对应整型列的在客户端的名称元组
def updatauserOrderById(table, dict1, columnId, id, adminChangeDic, intColumnClinetNameList=[], ids="ids",
                        isIsInt=True):
    # 因为订单号为字符串所以findById报错，重写此方法
    try:
        sqlStr = "update %s set " % table.__tablename__
        if isIsInt:
            wherStr = " where %s= %s" % (columnId, id)
        else:
            wherStr = " where %s= '%s'" % (columnId, id)
        conditionStr = ""
        for columnName in dict1.keys():
            if columnName == ids:
                continue
            if columnName in intColumnClinetNameList:
                conditionStr = conditionStr + adminChangeDic[columnName] + "=" + str(dict1[columnName]) + ","
            else:
                conditionStr = conditionStr + adminChangeDic[columnName] + "= '" + dict1[columnName] + "',"
        sqlStr = sqlStr + conditionStr[:-1] + wherStr
        sqlStrquery = text(sqlStr)
        logger.info("update by:%s" % request.remote_addr)
        logger.info(sqlStrquery)
        db.engine.execute(sqlStrquery)
        admin = findById(table, columnId, id, isStrcheck=True)
        return admin
    except Exception, e:
        logger.error("updatauserOrderById")
        logger.error(e)
        return None


# 3304数据库条件查询
# adminChangeDic：客户端对应数据库表格列名表，intColumnClinetNameList：整型列元组，tableName：表名
# condMsg查询条件，及客户端传入的jason转换为的字典
def conditionDataListFind3304(condMsg, adminChangeDic, intColumnClinetNameList, tableName, sqlStr=None,
                              deptIdConditonStr=""):
    opDic = {"equal": "=", "notequal": "!=", "less": "<", "greater": ">", "contains": "like", "like": "like"}
    if not sqlStr:
        sqlStr = "SELECT * FROM %s WHERE " % tableName
    # 排序编辑
    multiSort = condMsg.get("multiSort", [])
    orderByStr = ""
    if len(multiSort) != 0:
        orderByStr = "order by "
        fieldList = multiSort.get("field", None)
        sortList = multiSort.get("sort", None)
        for field in fieldList:
            orderByStr = orderByStr + adminChangeDic[field] + " " + sortList[fieldList.index(field)] + ","
        orderByStr = orderByStr[:-1]

    # 分页编辑
    pageDic = condMsg.get("page", {})
    limitStr = ""
    if len(pageDic) != 0:
        pageIndex = pageDic.get("pageIndex", None)
        pageSize = pageDic.get("pageSize", 20)
        if pageIndex != None and pageSize != None:
            limitStr = limitStr + "limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)

    # 条件编辑
    if len(condMsg["condition"]) == 0:
        sqlStr = sqlStr[:-7]
    else:
        for cond in condMsg["condition"]:
            field = cond["field"]
            op = cond["op"]
            value = cond["value"]
            if op == "like":
                sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '" + value + r"'" + " and "
            elif op != "contains":
                if field in intColumnClinetNameList:
                    sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + str(value) + " and "
                else:
                    sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + "'" + value + "' and "
            else:
                sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '%" + value + r"%'" + " and "
        sqlStr = sqlStr[:-5]
    sqlCount = "select count(*) from (" + sqlStr + deptIdConditonStr + ") num"
    sqlStr = sqlStr + deptIdConditonStr + " " + orderByStr + " " + limitStr
    print sqlStr
    try:
        sqlStrquery = text(sqlStr)
        sqlCount = text(sqlCount)
        adminsList = db.session.execute(sqlStrquery, bind=db.get_engine(app, bind="crawler")).fetchall()
        countObj = db.session.execute(sqlCount, bind=db.get_engine(app, bind="crawler")).fetchall()
        count = 0
        for countList in countObj:
            count = countList[0]
        return adminsList, count
    except Exception, e:
        logger.error("conditionDataListFind3304")
        logger.error(e)
        return [], 0


# 根据条件返回跟新数据
# table 类名,upDict 要跟新的数据字典 ,wherStr 跟新条件
# adminChangeDic 客户端与数据库表头对应字典
# intColumnClinetNameList 对应整型列的在客户端的名称元组
# 成功返回True，失败返回False
def updataByWhereStr(table, upDict, wherStr, tableChangeDic, intColumnClinetNameList):
    try:
        sqlStr = "update %s set " % table.__tablename__
        conditionStr = ""
        for columnName in upDict.keys():
            if columnName == "idArray":
                continue
            if columnName in intColumnClinetNameList:
                conditionStr = conditionStr + tableChangeDic[columnName] + "=" + str(upDict[columnName]) + ","
            else:
                conditionStr = conditionStr + tableChangeDic[columnName] + "= '" + upDict[columnName] + "',"
        sqlStr = sqlStr + conditionStr[:-1] + wherStr
        sqlStrquery = text(sqlStr)
        logger.info("update by:%s" % request.remote_addr)
        logger.info(sqlStrquery)
        db.engine.execute(sqlStrquery)
        return True
    except Exception, e:
        logger.error("updataByWhereStr")
        logger.error(e)
        return False


# 执行sqlStr传入的查询、更新、添加sql语句，返回对应结果
def executeTheSQLStatement(sqlStr):
    try:
        sqlStrquery = text(sqlStr)
        logger.info("update by:%s" % request.remote_addr)
        logger.info(sqlStrquery)
        adminsList = db.engine.execute(sqlStrquery)
        return adminsList
    except Exception, e:
        logger.error("executeTheSQLStatement")
        logger.error(e)
        return []


def deleteByColumn(Table, idList, columnId, otherCondition=None, isInt=True):
    count = 0
    try:
        for id in idList:
            if isInt:
                conditionStr = "%s = %s" % (columnId, int(id))
            else:
                conditionStr = "%s = '%s'" % (columnId, id)
            if otherCondition:
                conditionStr = conditionStr + otherCondition
            tables = Table.query.filter(conditionStr).all()
            for table in tables:
                logger.info("delete %s by:%s" % (Table.__tablename__, request.remote_addr))
                logger.info(table.__repr__())
                db.session.delete(table)
                db.session.commit()
                count += 1
        resultDict = {"message": {"code": 1, "status": "success"}, "info": {"count": count}}
    except Exception, e:
        logger.error("deleteByColumn")
        logger.error(e)
        resultDict = {"code": 0, "status": "error"}
    return resultDict


# 订单表查询
# def checkOrderItem(condMsg, adminChangeDic, intColumnClinetNameList, tableName, sqlStr = None):
#     opDic = {"equal": "=", "notequal": "!=", "less": "<", "greater": ">", "contains": "like"}
#     if not sqlStr:
#         sqlStr = "SELECT * FROM %s WHERE " % tableName
#
#     # 排序编辑
#     multiSort = condMsg.get("multiSort", [])
#     orderByStr = ""
#     if len(multiSort) != 0:
#         orderByStr = "order by "
#         fieldList = multiSort.get("field", None)
#         sortList = multiSort.get("sort", None)
#         for field in fieldList:
#             orderByStr = orderByStr + adminChangeDic[field] + " " + sortList[fieldList.index(field)] + ","
#         orderByStr = orderByStr[:-1]
#
#     # 分页编辑
#     pageDic = condMsg.get("page", {})
#     limitStr = ""
#     if len(pageDic) != 0:
#         pageIndex = pageDic.get("pageIndex", None)
#         pageSize = pageDic.get("pageSize", 20)
#         if pageIndex != None and pageSize != None:
#             limitStr = limitStr + "limit " + str((pageIndex-1) * pageSize) + "," + str(pageSize)
#
#     # 条件编辑
#     if len(condMsg["condition"]) == 0:
#         sqlStr = sqlStr[:-7]
#     else:
#         for cond in condMsg["condition"]:
#             field = cond["field"]
#             op = cond["op"]
#             value = cond["value"]
#             if op != "contains":
#                 if field in intColumnClinetNameList:
#                     sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + str(value) + " and "
#                 else:
#                     sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + "'" + value + "' and "
#             else:
#                 sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '%" + value + r"%'" + " and "
#         sqlStr = sqlStr[:-5]
#     sqlCount = "select count(*) from (" + sqlStr + ") num"
#     sqlStr = sqlStr + " " + orderByStr + " " + limitStr
#
#     try:
#         sqlStrquery = text(sqlStr)
#         sqlCount = text(sqlCount)
#         adminsList = db.engine.execute(sqlStrquery)
#         countObj = db.engine.execute(sqlCount)
#         count = 0
#         for countList in countObj:
#             count = countList[0]
#         return adminsList, count
#     except Exception,e:
#         logger.error(e)
#         return [], 0

def sqlFunctionCall(sqlStr):
    try:
        sqlStr = text(sqlStr)
        logger.info("update by:%s" % request.remote_addr)
        logger.info(sqlStr)
        adminsList = db.engine.execute(sqlStr)
        resualtList = adminsList.first()
        return list(resualtList)
    except Exception, e:
        logger.error("sqlFunctionCall")
        logger.error(e)
        return None


def sqlFunctionCallBoss(sqlStr):
    try:
        sqlStr = text(sqlStr)
        logger.info("update by:%s" % request.remote_addr)
        logger.info(sqlStr)
        adminsList = db.engine.execute(sqlStr)
        resualtList = adminsList.fetchall()
        return list(resualtList)
    except Exception, e:
        logger.error("sqlFunctionCall")
        logger.error(e)
        return None


def addTokenToSql(table):
    try:
        # 将新增项目插入数据库
        db.session.add(table)
        # 提交修改
        db.session.flush()
        db.session.commit()
        logger.info("update %s by:%s" % (table.__tablename__, request.remote_addr))
        logger.info(table.__repr__())
        return table
    except Exception, e:
        logger.error("addTokenToSql")
        logger.error(e)
        return None


# 通过用户名(手机号、邮箱等)和密码查询
# admin_name可以是用户名、手机号、邮箱 该方法用于登录端口
def findByNameAndPassword(table, admin_name, adminName, admin_password, adminPassword):
    try:
        conditionStr = text("%s = '%s' and %s = '%s'" % (admin_name, adminName, admin_password, adminPassword))
        tables = table.query.filter(conditionStr).first()
        if tables == None:
            return 0
        return tables
    except Exception, e:
        logger.error("findByNameAndPassword")
        logger.error(e)
        return None


# 跟新数据
# table 类名,dict1 要跟新的数据字典 ,columnId 表id名（如：admin_id）
# id id值 ,adminChangeDic 客户端与数据库表头对应字典
# intColumnClinetNameList 对应整型列的在客户端的名称元组
def updataById(table, dict1, columnId, id, adminChangeDic, intColumnClinetNameList=[], ids="ids", isIsInt=True,
               otherCondition=""):
    try:
        sqlStr = "update %s set " % table.__tablename__
        if isIsInt:
            wherStr = " where %s= %s" % (columnId, id)
        else:
            wherStr = " where %s= '%s'" % (columnId, id)
        if otherCondition:
            wherStr += otherCondition
        conditionStr = ""
        for columnName in dict1.keys():
            if columnName == ids:
                continue
            if columnName == columnId:
                continue
            if columnName in intColumnClinetNameList:
                conditionStr = conditionStr + adminChangeDic[columnName] + "=" + str(dict1[columnName]) + ","
            else:
                conditionStr = conditionStr + table.__tablename__ + "." + adminChangeDic[columnName] + "= '" + dict1[
                    columnName] + "',"
        sqlStr = sqlStr + conditionStr[:-1] + wherStr
        sqlStrquery = text(sqlStr)
        logger.info("update %s by:%s,%s" % (table.__tablename__, request.remote_addr, str(get_jwt_identity())))
        logger.info(sqlStrquery)
        db.engine.execute(sqlStrquery)
        admin = findById(table, columnId, id)
        return admin
    except Exception, e:
        logger.error("updataById")
        logger.error(e)
        return None


# 条件查询
# adminChangeDic：客户端对应数据库表格列名表，intColumnClinetNameList：整型列元组，tableName：表名
# condMsg查询条件，及客户端传入的jason转换为的字典
def conditionDataListFind(condMsg, adminChangeDic, intColumnClinetNameList, tableName, sqlStr=None, groupBy="",
                          orderByStr="", deptIdConditonStr=""):
    opDic = {"in": "in", "equal": "=", "notequal": "!=", "less": "<", "greater": ">", "contains": "like",
             "like": "like", "null": "", "not in": "not in", "is": "is"}
    if not sqlStr:
        sqlStr = "SELECT * FROM %s WHERE " % tableName

    # 排序编辑
    multiSort = condMsg.get("multiSort", [])
    # orderByStr = ""
    if len(multiSort) != 0:
        orderByStr = "order by "
        fieldList = multiSort.get("field", None)
        sortList = multiSort.get("sort", None)
        for field in fieldList:
            orderByStr = orderByStr + adminChangeDic[field] + " " + sortList[fieldList.index(field)] + ","
        orderByStr = orderByStr[:-1]

    # 分页编辑
    pageDic = condMsg.get("page", {})
    limitStr = ""
    if len(pageDic) != 0:
        pageIndex = pageDic.get("pageIndex", 1)
        if pageIndex <= 0:
            pageIndex = 1
        pageSize = pageDic.get("pageSize", 20)
        if pageIndex != None and pageSize != None:
            limitStr = limitStr + "limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)
    # 条件编辑
    if len(condMsg["condition"]) == 0:
        sqlStr = sqlStr[:-7]
    else:
        for cond in condMsg["condition"]:
            field = cond["field"]
            op = cond["op"]
            value = cond["value"]
            if op == "like":
                sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '" + value + r"'" + " and "
            elif op == "null":
                sqlStr = sqlStr + adminChangeDic[field] + " is " + value + " and "
            elif op == "in":
                if field in intColumnClinetNameList:
                    sqlStr = sqlStr + adminChangeDic[field] + " in " + str(value) + " and "
                else:
                    # sqlStr = sqlStr + adminChangeDic[field] + " in " + "'" + value + "' and "
                    sqlStr = sqlStr + adminChangeDic[field] + " in " + value + " and "
            elif op == "not in":
                if field in intColumnClinetNameList:
                    sqlStr = sqlStr + adminChangeDic[field] + " not in " + str(value) + " and "
                else:
                    # sqlStr = sqlStr + adminChangeDic[field] + " in " + "'" + value + "' and "
                    sqlStr = sqlStr + adminChangeDic[field] + " not in " + value + " and "
            elif op == "is":
                sqlStr = sqlStr + adminChangeDic[field] + " is " + value + " and "
            elif op != "contains":
                if field in intColumnClinetNameList:
                    sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + str(value) + " and "
                else:
                    sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + "'" + value + "' and "
            else:
                sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '%" + value + r"%'" + " and "
        sqlStr = sqlStr[:-5]
    sqlStrCount = sqlStr + deptIdConditonStr
    sqlCount = "select count(*) from (" + sqlStrCount + ") num"
    sqlStr = sqlStr + deptIdConditonStr + " " + groupBy + orderByStr + " " + limitStr
    print sqlStr
    try:
        sqlStrquery = text(sqlStr)
        sqlCount = text(sqlCount)
        adminsList = db.engine.execute(sqlStrquery)
        countObj = db.engine.execute(sqlCount)
        count = 0
        for countList in countObj:
            count = countList[0]
        return adminsList, count
    except Exception, e:
        logger.error("conditionDataListFind")
        logger.error(e)
        return [], 0


# 通过对应表的id查询数据（此方法已舍弃不要使用）
# table：类名 ,idName数据库中表的id名称（如：admin_id）, id ：要查的id值
def findById(table, idName, id, isStrcheck=False):
    """此方法已舍弃不要使用"""
    try:
        if isStrcheck:
            conditionStr = text("%s = '%s'" % (idName, id))
        else:
            conditionStr = text("%s = %s" % (idName, int(id)))
        tables = table.query.filter(conditionStr).first()
        if tables == None:
            return 0
        return tables
    except Exception, e:
        logger.error("findById")
        logger.error(e)
        return None


# 添加数据到数据库
# table：类名 ,columnsStr数据元组
def insertToSQL(table, *columnsStr):
    try:
        stu = table(*columnsStr)
        # 将新增项目插入数据库
        db.session.add(stu)
        # 提交修改
        db.session.flush()
        db.session.commit()
        logger.info("add %s by:%s" % (table.__tablename__, request.remote_addr))
        logger.info(stu.__repr__())
        return stu
    except Exception, e:
        logger.error("insertToSQL")
        db.session.rollback()
        logger.error(e)
        return None


# 按id删除数据
# admin：类名，idList id数组 ,columnId id名称（如：admin_id），其他条件（如：“and role_id = 1 and menu_id = 10”）
def deleteById(table, idList, columnId, otherCondition=None, isInt=True):
    count = 0
    try:
        for id in idList:
            if isInt:
                conditionStr = "%s = %s" % (columnId, int(id))
            else:
                conditionStr = "%s = '%s'" % (columnId, id)
            if otherCondition:
                conditionStr = conditionStr + otherCondition
            admins = table.query.filter(conditionStr).first()
            if admins:
                logger.info("delet %s by:%s,%s" % (table.__tablename__, request.remote_addr, str(get_jwt_identity())))
                logger.info(admins.__repr__())
                db.session.delete(admins)
                db.session.commit()
                count += 1
        resultDict = {"message": {"code": 1, "status": "success"}, "info": {"count": count}}
    except Exception, e:
        logger.error("deleteById")
        logger.error(e)
        resultDict = {"message": {"code": 0, "msg": "error"}}
    return resultDict


def conditionDataListFindExcel(condMsg, adminChangeDic, intColumnClinetNameList, tableName, sqlStr=None, groupBy=""):
    opDic = {"in": "in", "equal": "=", "notequal": "!=", "less": "<", "greater": ">", "contains": "like",
             "like": "like", "null": ""}
    if not sqlStr:
        sqlStr = "SELECT * FROM %s WHERE " % tableName

    # 排序编辑
    multiSort = condMsg.get("multiSort", [])
    orderByStr = ""
    if len(multiSort) != 0:
        orderByStr = "order by "
        fieldList = multiSort.get("field", None)
        sortList = multiSort.get("sort", None)
        for field in fieldList:
            orderByStr = orderByStr + adminChangeDic[field] + " " + sortList[fieldList.index(field)] + ","
        orderByStr = orderByStr[:-1]

    # 分页编辑
    pageDic = condMsg.get("page", {})
    limitStr = ""
    if len(pageDic) != 0:
        pageIndex = pageDic.get("pageIndex", 1)
        pageSize = pageDic.get("pageSize", 20)
        if pageIndex != None and pageSize != None:
            limitStr = limitStr + "limit " + str((pageIndex - 1) * pageSize) + "," + str(pageSize)

    # 条件编辑
    if len(condMsg["condition"]) == 0:
        sqlStr = sqlStr[:-7]
    else:
        for cond in condMsg["condition"]:
            field = cond["field"]
            op = cond["op"]
            value = cond["value"]
            if op == "like":
                sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '" + value + r"'" + " and "
            elif op == "null":
                sqlStr = sqlStr + adminChangeDic[field] + " is " + value + " and "
            elif op == "in":
                if field in intColumnClinetNameList:
                    sqlStr = sqlStr + adminChangeDic[field] + " in " + str(value) + " and "
                else:
                    sqlStr = sqlStr + adminChangeDic[field] + " in " + "'" + value + "' and "
            elif op != "contains":
                if field in intColumnClinetNameList:
                    sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + str(value) + " and "
                else:
                    sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + "'" + value + "' and "
            else:
                sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '%" + value + r"%'" + " and "
        sqlStr = sqlStr[:-5]
    print sqlStr
    sqlCount = "select count(*) from (" + sqlStr + ") num"
    sqlStr = sqlStr + " " + groupBy + orderByStr + " " + limitStr
    try:
        sqlStrquery = text(sqlStr)
        sqlCount = text(sqlCount)
        adminsList = db.engine.execute(sqlStrquery)
        countObj = db.engine.execute(sqlCount)
        count = 0
        for countList in countObj:
            count = countList[0]
        return adminsList, count
    except Exception, e:
        logger.error("conditionDataListFind")
        logger.error(e)
        return [], 0


# 按id删除数据
# admin：类名，idList id数组 ,columnId id名称（如：admin_id），其他条件（如：“and role_id = 1 and menu_id = 10”）
def deleteByIdBoss(table, idList, columnId, otherCondition=None, isInt=True):
    count = 0
    try:
        for id in idList:
            if isInt:
                conditionStr = "%s = %s" % (columnId, int(id))
            else:
                conditionStr = "%s = '%s'" % (columnId, id)
            if otherCondition:
                conditionStr = conditionStr + otherCondition
            admins = table.query.filter(conditionStr).first()
            if admins:
                logger.info(
                    "delet %s by:%s,%s" % (table.__tablename__, request.remote_addr, str(get_jwt_identity())))
                logger.info(admins.__repr__())
                db.session.delete(admins)
                db.session.commit()
                count += 1
        return count
    except Exception, e:
        logger.error("deleteById")
        logger.error(e)
        resultDict = {"code": 0, "status": "error"}
        return 0

# 条件查询表
# 通过对象查询数据，但是因为1.不等号和模糊查询同时存在是无法执行，2.如果条件仅为关联表中的限制时也无法执行，所有该为使用原声的
# sql查询方式
# def selectTest(condMsg, adminChangeDic, intColumnClinetNameList, table, className):
#     opDic = {"equal": "==", "notequal": "!=", "less": "<", "greater": ">", "contains": "like"}
#     sqlStr = ""
#     changeKeyList = adminChangeDic.keys()
#     if len(condMsg["condition"]) == 0:
#         return None
#     else:
#         # table1 = table.query.filter(table.admin.admin_desc.like('%a%')).order_by(table.id.desc()).paginate(1, 1)
#         # tableqq = db.session.query(table)
#         # tables = tableqq.filter(table.role_id == 1 , table.role_id> 0)
#         # table1 = tables.filter(table.admin.admin_desc.like('%a%'))
#         # table1 = tables.filter(tables.admin.admin_desc.like('%a%')).order_by(tables.id.desc()).paginate(1, 1)
#         return None
#         # try:
#         #     # 查询条件处理
#         for cond in condMsg["condition"]:
#             field = cond["field"]
#             op = cond["op"]
#             value = cond["value"]
#
#             if field not in changeKeyList:
#                     # 如果是关联表中的列的情况
#                     if adminChangeDic.get("other", None):
#                         otherTableDic = adminChangeDic["other"]
#                         for key in otherTableDic:
#                             otherChangeDic = otherTableDic[key]
#                             if field in otherChangeDic.keys():
#                                 if op != "contains":
#                                     if field in intColumnClinetNameList:
#                                         sqlStr = sqlStr + " and %s.%s.%s %s %s" % (className, key, adminChangeDic["other"][key][field], opDic[op], str(value))
#                                     else:
#                                         sqlStr = sqlStr + " and %s.%s.%s %s '%s'" % (className, key, adminChangeDic["other"][key][field], opDic[op], str(value))
#                                 else:
#                                     # sqlStr = sqlStr + " and %s.%s.%s.like('%%s%')" % (tableName,key, adminChangeDic["other"][key][field], str(value))
#                                     sqlStr = sqlStr + " and " + className + "." + key + "." + adminChangeDic["other"][key][field] + ".like" + "('%" + str(value) + "%')"
#                     else:
#                         return None
#             else:
#                 if op != "contains":
#                     if field in intColumnClinetNameList:
#                         sqlStr = sqlStr + " and %s %s %s" % (adminChangeDic[field], opDic[op], str(value))
#                     else:
#                         sqlStr = sqlStr + " and %s %s '%s'" % (adminChangeDic[field], opDic[op], str(value))
#                 else:
#                     # sqlStr = sqlStr + " and %s.%s.like(%'%s'%)" % (tableName, adminChangeDic[field], str(value))
#                     sqlStr = sqlStr + " and " + className + "." + key + "." + adminChangeDic[field] + ".like" + "('%" + str(value) + "%')"
#
#         sqlStr = sqlStr[5:]
#         # 排序处理
#         multiSortLlist = condMsg.get("multiSort", [])
#         orderByStr = ""
#         if len(multiSortLlist) != 0:
#             for multiSort in multiSortLlist:
#                 field = multiSort.get("field", None)
#                 sort = multiSort.get("sort", None)
#                 if field and sort:
#                     orderByStr = orderByStr + "%s.%s.%s() and " % (className, adminChangeDic[field], sort)#orderByStr + adminChangeDic[field] + " " + sort + ","
#             if orderByStr != "":
#                 orderByStr = orderByStr[:-5]
#         # 分页处理，及最后查询
#         pageDic = condMsg.get("page", {})
#         tables = table.query.filter(table.id == 1 and table.role_id > 0 and table.admin.admin_desc.like('%a%')).order_by(table.id.desc()).paginate(1, 1)  # .all()
#         if len(pageDic) != 0:
#             pageIndex = pageDic.get("pageIndex", None)
#             pageSize = pageDic.get("pageSize", None)
#             if pageIndex != None and pageSize != None:
#                 if orderByStr == "":
#                     # 没有排序条件，有分页的情况
#                     tables = table.query.filter(sqlStr).paginate(pageIndex, pageSize).all()
#                 else:
#                     # 有排序条件和分页条件的情况
#                     tables = table.query.filter(sqlStr).order_by(orderByStr).paginate(pageIndex, pageSize).all()
#             else:
#                 if orderByStr == "":
#                     # 没有排序也没有分页的情况
#                     tables = table.query.filter(sqlStr).all()
#                 else:
#                     # 有排序没有分页的情况
#                     tables = table.query.filter(sqlStr).order_by(orderByStr).all()
#         else:
#             if orderByStr == "":
#                 # 没有排序也没有分页的情况
#                 tables = table.query.filter(sqlStr).all()
#             else:
#                 # 有排序没有分页的情况
#                 tables = table.query.filter(sqlStr).order_by(orderByStr).all()
#         return tables
#         # except Exception,e:
#         #     logger.info(e)
#         #     return None
