# coding:utf-8
import os
import time

from openpyxl import Workbook
from sqlalchemy import text

from common.OperationOfDB import conditionDataListFind
from config import db, logger


def outToExcel(ids, tablename, queryDict, tableChangeDic):
    try:
        wb = Workbook()
        sheet = wb.active
        sheet.title = 'Sheet1'
        sqlStr = """select column_name,column_comment from information_schema.`columns` WHERE TABLE_NAME='{}'""".format(
            tablename)
        sqlStrquery = text(sqlStr)
        adminsList = db.engine.execute(sqlStrquery)
        nameList = []
        columnList = []
        for name in adminsList:
            nameList.append(name[1])
            columnList.append(name[0])
        columnStr = ",".join(columnList)
        nameList[0] = "序号"
        sheet.append(nameList)
        if queryDict:
            intColumnClinetNameList = []
            if ids:
                sqlStr = "SELECT %s FROM %s WHERE id in %s WHERE " % (columnStr, tablename, tuple(ids))
            else:
                sqlStr = "SELECT %s FROM %s WHERE " % (columnStr, tablename)
                print sqlStr
            dataList, count = conditionDataListFind(queryDict, tableChangeDic, intColumnClinetNameList, tablename,
                                                    sqlStr)
        else:
            if ids:
                dataSql = "select {} from {} WHERE id in {}".format(columnStr, tablename, tuple(ids))
            else:
                dataSql = "select {} from {} limit {}".format(columnStr, tablename, 10)
            sqlStrquery = text(dataSql)
            dataList = db.engine.execute(sqlStrquery)
        n = 0
        for table in dataList:
            infoList = []
            n += 1
            for column in columnList:
                infoList.append(table[column])
            infoList[0] = n
            sheet.append(infoList)
        filename = "export/" + "file" + str(int(time.time())) + ".xlsx"
        filepath = os.path.join("static/", filename)
        wb.save(filepath)
        return filename
    except Exception as e:
        logger.info(e)
        return None
