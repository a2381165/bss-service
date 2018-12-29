# -*- coding: utf-8 -*-
from config import db, logger, app
from sqlalchemy import text
from flask_jwt_extended import get_jwt_identity
from flask import request


class OperationOfDB:
    def __init__(self):
        self.idInt = True
        self.classDB = db

    def __repr__(self):
        return "this is operation of db class"

    def setIdType(self, idIsInt):
        self.idInt = idIsInt

    # 添加数据到数据库
    # table：类名 ,columnsStr数据元组
    def insertToSQL(self, table, *columnsStr):
        try:
            stu = table(*columnsStr)
            # 将新增项目插入数据库
            self.classDB.session.add(stu)
            self.classDB.session.flush()
            logger.info("add %s by:%s" % (table.__tablename__, request.remote_addr))
            logger.info(stu.__repr__())
            return stu
        except Exception, e:
            self.classDB.session.rollback()
            logger.error("insertToSQL")
            logger.error(e)
            return None

    def commitToSQL(self):
        try:
            self.classDB.session.commit()
            return True
        except Exception, e:
            logger.error("commitToSQL")
            logger.error(e)
            return False

    def commitRollback(self):
        """手动回滚"""
        self.classDB.session.rollback()

    # 按id删除数据
    # admin：类名，idList id数组 ,columnId id名称（如：admin_id），其他条件（如：“and role_id = 1 and menu_id = 10”）
    def deleteById(self, table, idList, columnId, otherCondition=None):
        count = 0
        try:
            for id in idList:
                if self.idInt:
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
                    self.classDB.session.delete(admins)
                    count += 1
            resultDict = {"message": {"code": 1, "status": "success"}, "info": {"count": count}}
        except Exception, e:
            logger.error("deleteById")
            logger.error(e)
            resultDict = {"code": 0, "status": "error"}
        return resultDict
    # 按id删除数据
    # admin：类名，idList id数组 ,columnId id名称（如：admin_id），其他条件（如：“and role_id = 1 and menu_id = 10”）
    def deleteByIdBoss(self, table, id, columnId, otherCondition=None):
        count = 0
        try:
            if self.idInt:
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
                self.classDB.session.delete(admins)
                count += 1
            return True
        except Exception, e:
            logger.error("deleteByIdBoss")
            logger.error(e)
            return False

    # 条件查询
    # adminChangeDic：客户端对应数据库表格列名表，intColumnClinetNameList：整型列元组，tableName：表名
    # condMsg查询条件，及客户端传入的jason转换为的字典
    def conditionDataListFind(self, condMsg, adminChangeDic, intColumnClinetNameList, tableName, sqlStr=None):
        opDic = {"equal": "=", "notequal": "!=", "less": "<", "greater": ">", "contains": "like", "null": ""}
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
                if op == "null":
                    sqlStr = sqlStr + adminChangeDic[field] + " is " + value + " and "
                elif op != "contains":
                    if field in intColumnClinetNameList:
                        sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + str(value) + " and "
                    else:
                        sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + "'" + value + "' and "
                else:
                    sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '%" + value + r"%'" + " and "
            sqlStr = sqlStr[:-5]
        sqlCount = "select count(*) from (" + sqlStr + ") num"
        sqlStr = sqlStr + " " + orderByStr + " " + limitStr
        try:
            sqlStrquery = text(sqlStr)
            sqlCount = text(sqlCount)
            adminsList = self.classDB.engine.execute(sqlStrquery)
            countObj = self.classDB.engine.execute(sqlCount)
            count = 0
            for countList in countObj:
                count = countList[0]
            return adminsList, count
        except Exception, e:
            logger.error("conditionDataListFind")
            logger.error(e)
            return [], 0

    def addTokenToSql(self, table):
        try:
            # 将新增项目插入数据库
            self.classDB.session.add(table)
            self.classDB.session.flush()
            logger.info("update %s by:%s" % (table.__tablename__, request.remote_addr))
            logger.info(table.__repr__())
            return table
        except Exception, e:
            logger.error("addTokenToSql")
            logger.error(e)
            self.classDB.session.rollback()
            return None

    def sqlFunctionCall(self, sqlStr):
        try:
            sqlStr = text(sqlStr)
            logger.info("update by:%s" % request.remote_addr)
            logger.info(sqlStr)
            adminsList = self.classDB.engine.execute(sqlStr)
            resualtList = adminsList.first()
            return list(resualtList)
        except Exception, e:
            logger.error("sqlFunctionCall")
            logger.error(e)
            return None

    def commitToSQL(self):
        try:
            self.classDB.session.flush()
            self.classDB.session.commit()
            logger.info("%s commit" % request.remote_addr)
            return True
        except Exception, e:
            self.classDB.session.rollback()
            logger.error("commitToSQL")
            logger.error(e)
            return False

    def sqlOrderPayDo(self, sqlStr):
        try:
            sqlStr = text(sqlStr)
            logger.info("payment info by:%s" % request.remote_addr)
            logger.info(sqlStr)
            self.classDB.engine.execute(sqlStr)
            return True
        except Exception, e:
            logger.error("sqlOrderPayDo")
            logger.error(e)
            return False

    def insertOrderMethodExecute(self, sqlStr):
        try:
            sqlStr = text(sqlStr)
            logger.info("insert by:%s" % request.remote_addr)
            logger.info(sqlStr)
            adminsList = self.classDB.engine.execute(sqlStr)
            if adminsList:
                return True
            return False
        except Exception, e:
            logger.error("insertOrderMethodExecute")
            logger.error(e)
            return False

    # findByThis
    def findByThis(self, table, columnId, id):
        try:
            tables = table.query.filter(columnId == id).first()
            if tables == None:
                return 0
            return tables
        except Exception, e:
            logger.error("findById")
            logger.error(e)
            return None

    # db.session.query(hostAssets).filter(hostAssets.business_id == ids).update({"business_id": None},synchronize_session=False)
    def updateThis(self, table, columnId, id, dataDict, adminChangeDic, isInt=True,intColumnClinetNameList=[]):
        try:
            dict1 = {}
            # print dataDict
            for columnName in dataDict.keys():
                if columnName == "ids":
                    continue
                if columnName == "id":
                    continue
                dict1[adminChangeDic[columnName]] = dataDict[columnName]
                # print dict1
                # # conditionStr = conditionStr + adminChangeDic[columnName] + "=" + str(dict1[columnName]) + ","
                # # else:
                # #     dict1[adminChangeDic[columnName]] = dict1[columnName]
                # # conditionStr = conditionStr + adminChangeDic[columnName] + "= '" + dict1[columnName] + "',"
            # print dict1
            if isInt:
                hasTrue = self.classDB.session.query(table).filter(columnId == int(id)).update(dict1,
                                                                                               synchronize_session=False)
            else:
                hasTrue = self.classDB.session.query(table).filter(columnId == id).update(dict1,
                                                                                          synchronize_session=False)
            if hasTrue == None:
                return 0
            tables = self.findByThis(table, columnId, id)
            logger.info("update by:%s" % request.remote_addr)
            return tables
        except Exception, e:
            logger.error("updateThis")
            logger.error(e)
            return False

    # 跟新数据
    # table 类名,dict1 要跟新的数据字典 ,columnId 表id名（如：admin_id）
    # id id值 ,adminChangeDic 客户端与数据库表头对应字典
    # intColumnClinetNameList 对应整型列的在客户端的名称元组
    def updatauserOrderById(self, table, dict1, columnId, id, adminChangeDic, intColumnClinetNameList=[], ids="ids",
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
            self.classDB.engine.execute(sqlStrquery)
            # self.classDB.session.add(sqlStrquery)
            # self.classDB.session.flush()

            admin = self.findById(table, columnId, id,
                                  isStrcheck=True)
            return admin
        except Exception, e:
            logger.error("updatauserOrderById")
            logger.error(e)
            return None

    # 通过对应表的id查询数据（此方法已舍弃不要使用）
    # table：类名 ,idName数据库中表的id名称（如：admin_id）, id ：要查的id值
    def findById(self, table, idName, id, isStrcheck=False):
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

    # 3304数据库条件查询
    # adminChangeDic：客户端对应数据库表格列名表，intColumnClinetNameList：整型列元组，tableName：表名
    # condMsg查询条件，及客户端传入的jason转换为的字典
    def conditionDataListFind3304(self, condMsg, adminChangeDic, intColumnClinetNameList, tableName, sqlStr=None):
        opDic = {"equal": "=", "notequal": "!=", "less": "<", "greater": ">", "contains": "like", "null": ""}
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
                if op == "null":
                    sqlStr = sqlStr + adminChangeDic[field] + " is " + value + " and "
                elif op != "contains":
                    if field in intColumnClinetNameList:
                        sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + str(value) + " and "
                    else:
                        sqlStr = sqlStr + adminChangeDic[field] + opDic[op] + "'" + value + "' and "
                else:
                    sqlStr = sqlStr + adminChangeDic[field] + " like" + r" '%" + value + r"%'" + " and "
            sqlStr = sqlStr[:-5]
        sqlCount = "select count(*) from (" + sqlStr + ") num"
        sqlStr = sqlStr + " " + orderByStr + " " + limitStr
        try:
            sqlStrquery = text(sqlStr)
            sqlCount = text(sqlCount)
            adminsList = self.classDB.session.execute(sqlStrquery,
                                                      bind=self.classDB.get_engine(app, bind="crawler")).fetchall()
            countObj = self.classDB.session.execute(sqlCount,
                                                    bind=self.classDB.get_engine(app, bind="crawler")).fetchall()
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
    def updataByWhereStr(self, table, upDict, wherStr, tableChangeDic, intColumnClinetNameList):
        try:
            sqlStr = "update %s set " % table.__tablename__
            conditionStr = ""
            for columnName in upDict.keys():
                if columnName == "idArray":
                    continue
                if columnName == "ids":
                    continue
                if columnName in intColumnClinetNameList:
                    conditionStr = conditionStr + tableChangeDic[columnName] + "=" + str(upDict[columnName]) + ","
                else:
                    conditionStr = conditionStr + tableChangeDic[columnName] + "= '" + upDict[columnName] + "',"
            sqlStr = sqlStr + conditionStr[:-1] + wherStr
            sqlStrquery = text(sqlStr)
            logger.info("update by:%s" % request.remote_addr)
            logger.info(sqlStrquery)
            self.classDB.engine.execute(sqlStrquery)
            return True
        except Exception, e:
            logger.error("updataByWhereStr")
            logger.error(e)
            return False

    # 执行sqlStr传入的查询、更新、添加sql语句，返回对应结果
    def executeTheSQLStatement(self, sqlStr):
        try:
            sqlStrquery = text(sqlStr)
            logger.info("update by:%s" % request.remote_addr)
            logger.info(sqlStrquery)
            adminsList = self.classDB.engine.execute(sqlStrquery)
            return adminsList
        except Exception, e:
            logger.error("executeTheSQLStatement")
            logger.error(e)
            return []

    def deleteByColumn(self, Table, idList, columnId, otherCondition=None, isInt=True):
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
                    self.classDB.session.delete(table)
                    count += 1
            resultDict = {"message": {"code": 1, "status": "success"}, "info": {"count": count}}
        except Exception, e:
            logger.error("deleteByColumn")
            logger.error(e)
            resultDict = {"code": 0, "status": "error"}
        return resultDict

    def deleteByColumnBoss(self, Table, idList, columnId, otherCondition=None, isInt=True):
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
                    self.classDB.session.delete(table)
                    count += 1
            resultDict = {"message": {"code": 1, "status": "success"}, "info": {"count": count}}
        except Exception, e:
            logger.error("deleteByColumnBoss")
            logger.error(e)
            resultDict = {"code": 0, "status": "error"}
        return resultDict
    def updataByWhereStrClass(self, table, upDict, wherStr, tableChangeDic, intColumnClinetNameList):
        try:
            sqlStr = "update %s set " % table.__tablename__
            conditionStr = ""
            for columnName in upDict.keys():
                if columnName == "idArray":
                    continue
                if columnName == "ids":
                    continue
                if columnName in intColumnClinetNameList:
                    conditionStr = conditionStr + tableChangeDic[columnName] + "=" + str(upDict[columnName]) + ","
                else:
                    conditionStr = conditionStr + tableChangeDic[columnName] + "= '" + upDict[columnName] + "',"
            sqlStr = sqlStr + conditionStr[:-1] + wherStr
            sqlStrquery = text(sqlStr)
            logger.info("update by:%s" % request.remote_addr)
            logger.info(sqlStrquery)
            # self.classDB.engine.execute(sqlStrquery)
            self.classDB.engine.execute(sqlStrquery)
            return True
        except Exception, e:
            logger.error("updataByWhereStr")
            logger.error(e)
            return False
