# coding:utf-8
import datetime
import redis
import time
from flask import jsonify, json, request
from config import db,logger,app
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from config import redisHost,redisPort,redisDb,redisTaskDb
from common.DatatimeNow import getTimeToStrfdate
from common.OperationOfDB import executeTheSQLStatement
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.Boss.SpiderScript import SpiderScript, tableChangeDic
from models.Boss.Area import Area as DataArea
from models.Boss.SpiderScriptSchedule import SpiderScriptSchedule
from models.Boss.SpiderSchedule import SpiderSchedule,tableChangeDic as schTableChangeDic
from controllers.SpiderScheduleApi import updataSpiderSchedule
from common.Log import queryLog, addLog, deleteLog, updateLog
from common.SpiderUtils import schedul


# 分页获取获取爬虫脚本信息
@app.route("/findSpiderScriptByCondition", methods=["POST"])
# @jwt_required
# @queryLog('spider_script')
def findSpiderScriptBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SpiderScript.__tablename__
    intColumnClinetNameList = [u'id', u'deptId', u'priority', u'nextFilter', u'isLock']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"id": tableData[0],
                        "deptNameKey": tableData[1],
                        "deptId": tableData[2],
                        "url": tableData[3],
                        "scriptText": tableData[4],
                        "priority": tableData[5],
                        "nextFilter": tableData[6],
                        "isLock":tableData[7],
                        "remark": tableData[8],
                        "projectName":tableData[9],
                        "spiderName": tableData[10],
                        "contentXpath":tableData[11],
                        }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取爬虫脚本信息
@app.route("/getSpiderScriptDetail", methods=["POST"])
# @jwt_required
# @queryLog('spider_script')
def getSpiderScriptDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = findById(SpiderScript, "id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"id": table.script_id,
                "remark": table.remark,
                "projectName": table.project_name,
                "spiderName": table.spider_name,
                "deptNameKey": table.dept_name_key,
                "deptId": table.dept_id,
                "url": table.url,
                "scriptText": table.scriptText,
                "priority": table.priority,
                "nextFilter": table.next_filter,
                "isLock": table.is_lock,
                "contentXpath":table.content_xpath
                }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除爬虫脚本
@app.route("/deleteSpiderScript", methods=["POST"])
# @jwt_required
# @deleteLog('spider_script')
def deleteSpiderScript():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    table = deleteById(SpiderScript, ids, "id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加爬虫脚本
@app.route("/addSpiderScript", methods=["POST"])
# @jwt_required
# @addLog('spider_script')
def addSpiderScript():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("remark", None), dataDict.get("projectName", None), dataDict.get("spiderName", None),
                 dataDict.get("deptNameKey", None), dataDict.get("deptId", None), dataDict.get("url", None),
                 dataDict.get("scriptText", None), dataDict.get("priority", 1), dataDict.get("nextFilter", 0),
                 dataDict.get("isLock", 1),dataDict.get("contentXpath"),'')
    table = insertToSQL(SpiderScript, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新爬虫脚本信息
@app.route("/updataSpiderScript", methods=["POST"])
# @jwt_required
# @updateLog('spider_script')
def updataSpiderScript():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("id", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'id', u'deptId', u'priority', u'nextFilter', u'isLock']
    table = updataById(SpiderScript, dataDict, "id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


def spiderScriptToRedis(InfoList):
    for data in InfoList:
        reminder_str = json.dumps(data)
        r = redis.StrictRedis(host=redisHost, port=redisPort, db=redisDb)
        r.lpush('basescrawler:rules', reminder_str)


@app.route("/deploySpiderScriptRedis", methods=["POST"])
# @jwt_required
# @updateLog('spider_script')
# @addLog('lpush_redis')
def deploySpiderScriptRedis():
    """
    # 添加脚本到redis队列
    :return:
    """
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    schedule_id = dataDict.get("scheduleId", "")
    areaCodeList = []
    scriptIdList = []
    InfoList = []
    running_job_ids = set([job.id for job in schedul.get_jobs()])
    print ('[running_job_ids] %s' % ','.join(running_job_ids))
    available_job_ids = set()
    dataAreaList = DataArea.query.filter(DataArea.area_status==1).all()
    spiderScriptScheduleList = SpiderScriptSchedule.query.filter_by(schedule_id=schedule_id).all()
    for area, sch in zip(dataAreaList, spiderScriptScheduleList):
        areaCodeList.append(str(area.area_code))
        scriptIdList.append(int(sch.script_id))
    areaCodeList.append(0),scriptIdList.append(0)
    tablename = SpiderScript.__tablename__
    sqlStr = "SELECT script_text,project_name,spider_name,dept_name_key,dept_id,url,next_filter,content_xpath FROM %s  \
             WHERE LEFT(dept_name_key,6) in %s and id in %s " % \
             (tablename, tuple(areaCodeList), tuple(scriptIdList))
    tableList = executeTheSQLStatement(sqlStr)
    if tableList:
        for tableData in tableList:
            infoDict = {
                "script_text": tableData[0],
                "project_name": tableData[1],
                "spider_name": tableData[2],
                "dept_name_key": tableData[3],
                "dept_id": tableData[4],
                "url": tableData[5],
                "next_filter": tableData[6],
                "content_xpath":tableData[7],
            }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
    intColumnClinetNameList = [u'scheduleId', u'isLock']
    dataDict = {'isLock': 1}
    updataById(SpiderSchedule, dataDict, "schedule_id", schedule_id, schTableChangeDic,
               intColumnClinetNameList)
    job_instance = SpiderSchedule.query.filter_by(schedule_id=schedule_id).first()
    job_id = "spider_job_%s" % (job_instance.schedule_id)
    available_job_ids.add(job_id)
    r = redis.StrictRedis(host=redisHost, port=redisPort, db=redisTaskDb)
    redis_tasks = r.zrange('apscheduler.run_times',0,-1)
    # add new job to schedule
    if job_id not in running_job_ids and job_id not in redis_tasks:
        try:
            schedul.add_job(spiderScriptToRedis,
                            args=(InfoList,),
                            trigger='cron',
                            jobstore='redis',
                            id=job_id,
                            minute=job_instance.cron_minutes,
                            hour=job_instance.cron_hour,
                            day=job_instance.cron_day_of_month,
                            day_of_week=job_instance.cron_day_of_week,
                            month=job_instance.cron_month,
                            second='*/30',
                            max_instances=999,
                            misfire_grace_time=60 * 60,
                            coalesce=True)
            schedul.start()
            resultDict = returnMsg({'result': 1})
            return jsonify(resultDict)
        except Exception as e:
            resultDict = returnMsg({'result': 1})
            return jsonify(resultDict)
    elif job_id not in running_job_ids and job_id in redis_tasks:
        schedul.start()
        resultDict = returnMsg({'result': 1})
        return jsonify(resultDict)
    else:
        resultDict = {'message':{"code":-1,"status":"Task already exists"}}
        return jsonify(resultDict)


# 添加脚本到redis队列
@app.route("/closeSchedule", methods=["POST"])
# @jwt_required
# @updateLog('spider_script')
# @addLog('lpush_redis')
def closeSchedule():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    schedule_id = dataDict.get("scheduleId", "")
    running_job_ids = set([job.id for job in schedul.get_jobs()])
    # print ('[running_job_ids] %s' % ','.join(running_job_ids))
    job_instance = SpiderSchedule.query.filter_by(schedule_id=schedule_id).first()
    job_id = "spider_job_%s" % (job_instance.schedule_id)
    if running_job_ids:
        if job_id in running_job_ids:
            print job_id
            schedul.remove_job(job_id)
            # schedul.shutdown()
            intColumnClinetNameList = [u'scheduleId', u'isLock']
            dataDict = {'isLock': 0}
            updataById(SpiderSchedule, dataDict, "schedule_id", job_instance.schedule_id, schTableChangeDic,
                       intColumnClinetNameList)
            resultDict = returnMsg({'result': 1,'status':'stop schedule success'})
            return jsonify(resultDict)
        else:
            resultDict = {"message":{'code': -1,'status':'not run schedule_job '}}
            return jsonify(resultDict)
    else:
        intColumnClinetNameList = [u'scheduleId', u'isLock']
        dataDict = {'isLock': 0}
        updataById(SpiderSchedule, dataDict, "schedule_id",job_instance.schedule_id, schTableChangeDic,
                   intColumnClinetNameList)
        resultDict = returnMsg({'result': 1, 'status': 'close all schedule success'})
        return jsonify(resultDict)


