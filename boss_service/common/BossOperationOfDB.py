# -*- coding: utf-8 -*-
from config import db, logger, app
from sqlalchemy import text
from flask import request
from flask_jwt_extended import get_jwt_identity


# 执行sql 获取条数
def executeSqlCount(sqlStr, isOther=True, bind=""):
    try:
        sqlStr = text(sqlStr)
        logger.info("query info by:%s" % request.remote_addr)
        logger.info(sqlStr)
        if isOther:
            queryList = db.engine.execute(sqlStr)
        else:
            queryList = db.session.execute(sqlStr, bind=db.get_engine(app, bind=bind)).fetchall()
        count = 0
        for countList in queryList:
            count = countList[0]
        return count
    except Exception, e:
        logger.error("executeSql")
        logger.error(e)
        return False


# 执行sql 获取list
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


# 执行函数 过程
def sqlFunctionCall(sqlStr, isOther=True, bind=""):
    try:
        sqlStr = text(sqlStr)
        logger.info("update by:%s" % request.remote_addr)
        logger.info(sqlStr)
        if isOther:
            adminsList = db.engine.execute(sqlStr)
        else:
            adminsList = db.session.execute(sqlStr, bind=db.get_engine(app, bind=bind))
        resualtList = adminsList.first()
        return list(resualtList)
    except Exception, e:
        logger.error("sqlFunctionCall")
        logger.error(e)
        return None


# 通过对应表的id查询数据（此方法已舍弃不要使用）
# table：类名 ,idName数据库中表的id名称（如：admin_id）, id ：要查的id值
def findById(table, idName, id, isStrcheck=False, bind=""):
    """此方法已舍弃不要使用"""
    try:
        sqlStr = "SELECT * FROM %s WHERE " % table
        if isStrcheck:
            whereStr = " %s = '%s' " % (idName, id)
        else:
            whereStr = " %s = %s " % (idName, int(id))
        sqlStr = sqlStr + whereStr
        sqlStrquery = text(sqlStr)
        if not bind:
            adminsList = db.engine.execute(sqlStrquery)
        else:
            adminsList = db.session.execute(sqlStrquery, bind=db.get_engine(app, bind=bind))
        return adminsList
    except Exception, e:
        logger.error("findById")
        logger.error(e)
        return None


# 条件查询
# adminChangeDic：客户端对应数据库表格列名表，intColumnClinetNameList：整型列元组，tableName：表名
# condMsg查询条件，及客户端传入的jason转换为的字典
def conditionDataListFind(condMsg, adminChangeDic, intColumnClinetNameList, tableName, sqlStr=None, groupBy="",
                          orderByStr="", bind=""):
    opDic = {"in": "in", "equal": "=", "notequal": "!=", "less": "<", "greater": ">", "contains": "like",
             "like": "like", "null": ""}
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
            elif op != "contains":
                if field in intColumnClinetNameList:
                    sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + str(value) + " and "
                else:
                    sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + "'" + value + "' and "
            else:
                sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '%" + value + r"%'" + " and "
        sqlStr = sqlStr[:-5]
    sqlCount = "select count(*) from (" + sqlStr + ") num"
    sqlStr = sqlStr + " " + groupBy + orderByStr + " " + limitStr
    try:
        sqlStrquery = text(sqlStr)
        sqlCount = text(sqlCount)
        if not bind:
            adminsList = db.engine.execute(sqlStrquery)
            countObj = db.engine.execute(sqlCount)
        else:
            adminsList = db.session.execute(sqlStrquery, bind=db.get_engine(app, bind=bind))
            countObj = db.session.execute(sqlCount, bind=db.get_engine(app, bind=bind))
        count = 0
        for countList in countObj:
            count = countList[0]
        return adminsList, count
    except Exception, e:
        logger.error("conditionDataListFind")
        logger.error(e)
        return [], 0


# 跟新数据
# table 类名,dict1 要跟新的数据字典 ,columnId 表id名（如：admin_id）
# id id值 ,adminChangeDic 客户端与数据库表头对应字典
# intColumnClinetNameList 对应整型列的在客户端的名称元组
def updatauserOrderById(table, dict1, columnId, id, adminChangeDic, intColumnClinetNameList=[], ids="ids",
                        isIsInt=True, bind=""):
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
        if not bind:
            db.engine.execute(sqlStrquery)
        else:
            db.session.execute(sqlStrquery, bind=db.get_engine(app, bind=bind))
        admin = findById(table, columnId, id, isStrcheck=True)
        return admin
    except Exception, e:
        logger.error("updatauserOrderById")
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
                logger.info("delete %s by:%s,%s" % (table.__tablename__, request.remote_addr, str(get_jwt_identity())))
                logger.info(admins.__repr__())
                db.session.delete(admins)
                db.session.commit()
                count += 1
        resultDict = {"message": {"code": 1, "status": "success"}, "info": {"count": count}}
    except Exception, e:
        logger.error("deleteById")
        logger.error(e)
        resultDict = {"code": 0, "status": "error"}
    return resultDict


# 跟新数据
# table 类名,dict1 要跟新的数据字典 ,columnId 表id名（如：admin_id）
# id id值 ,adminChangeDic 客户端与数据库表头对应字典
# intColumnClinetNameList 对应整型列的在客户端的名称元组
def updataById(table, dict1, columnId, id, adminChangeDic, intColumnClinetNameList=[], ids="ids", isIsInt=True):
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
        logger.info("update %s by:%s,%s" % (table.__tablename__, request.remote_addr, str(get_jwt_identity())))
        logger.info(sqlStrquery)
        db.engine.execute(sqlStrquery)
        admin = findById(table, columnId, id)
        return admin
    except Exception, e:
        logger.error("updataById")
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
