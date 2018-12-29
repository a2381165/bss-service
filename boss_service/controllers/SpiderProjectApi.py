# coding:utf-8
import datetime, os
import time
from shutil import move, copy, rmtree
from os.path import join, exists
from flask import jsonify, json, request
from sqlalchemy import text
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from scrapyd_api import ScrapydAPI
from common.SpiderUtils import scrapyd_url
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.SpiderUtils import build_egg, find_egg, build_project
from config import PROJECTS_FOLDER, db
from common.DatatimeNow import getTimeToStrfdate
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteById, insertToSQL, updataById
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, returnErrorMsg,errorCode
from version.v3.bossConfig import app
from models.Boss.SpiderProject import SpiderProject, tableChangeDic
from models.Boss.SpiderNode import SpiderNode, tableChangeDic as NodetableChangeDic
from models.Boss.SpiderDeploy import SpiderDeploy, tableChangeDic as deployTableChangeDic
from common.Log import queryLog, addLog, deleteLog, updateLog


# 获取爬虫项目列表
@app.route("/findSpiderProjectByCondition", methods=["POST"])
# @jwt_required
# @queryLog('spider_project')
def findSpiderProjectBycondition():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    if dataDict.get('condition', None) == None:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    tablename = SpiderProject.__tablename__
    intColumnClinetNameList = [u'projectId', u'configurable']
    tableList, count = conditionDataListFind(dataDict, tableChangeDic, intColumnClinetNameList, tablename)
    if tableList:
        InfoList = []
        for tableData in tableList:
            infoDict = {"projectId": tableData[0],
                        "projectDesc": tableData[1],
                        "projectName": tableData[2],
                        "spiderEgg": tableData[3],
                        "configurable": tableData[4],
                        "builtAt": str(tableData[5]),
                        "createdAt": str(tableData[6]),
                        "updatedAt": str(tableData[7]), }
            infoDict = dictRemoveNone(infoDict)
            InfoList.append(infoDict)
        resultDict = returnMsg(InfoList)
        resultDict["total"] = count
    else:
        resultDict = returnErrorMsg()
    return jsonify(resultDict)


# 获取爬虫项目详情
@app.route("/getSpiderProjectDetail", methods=["POST"])
@jwt_required
@queryLog('spider_project')
def getSpiderProjectDetail():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("projectId", [])
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)

    table = findById(SpiderProject, "project_id", id)
    if not table:
        resultDict = returnMsg("not find table")
        return jsonify(resultDict)
    infoDict = {"projectId": table.project_id,
                "projectDesc": table.project_desc,
                "projectName": table.project_name,
                "spiderEgg": table.spider_egg,
                "configurable": table.configurable,
                "builtAt": table.built_at,
                "createdAt": table.created_at,
                "updatedAt": table.updated_at, }
    infoDict = dictRemoveNone(infoDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 删除爬虫项目
@app.route("/deleteSpiderProject", methods=["POST"])
# @jwt_required
# @deleteLog('spider_project')
def deleteSpiderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    ids = dataDict.get("idArray", [])
    if not ids:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    path = PROJECTS_FOLDER
    for id in ids:
        spiderProjectList = SpiderProject.query.filter_by(project_id=id).first()
        try:
            project_name = spiderProjectList.spider_egg
            project_path = join(path, project_name)
            if not project_path:
                continue
            else:
                os.remove(project_path)
        except:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
    table = deleteById(SpiderProject, ids, "project_id")
    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)


# 添加爬虫项目
@app.route("/addSpiderProject", methods=["POST"])
# @jwt_required
# @addLog('spider_project')
def addSpiderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    columsStr = (dataDict.get("projectDesc", None), dataDict.get("projectName", None), dataDict.get("spiderEgg", None),
                 dataDict.get("configurable", None), dataDict.get("builtAt", None), dataDict.get("createdAt", None),
                 dataDict.get("updatedAt", None))
    table = insertToSQL(SpiderProject, *columsStr)
    if not table:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)
    resultDict = returnMsg({})
    return jsonify(resultDict)


# 更新爬虫项目
@app.route("/updataSpiderProject", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def updataSpiderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    id = dataDict.get("projectId", "")
    if not id:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    intColumnClinetNameList = [u'projectId', u'configurable']
    table = updataById(SpiderProject, dataDict, "project_id", id, tableChangeDic, intColumnClinetNameList)

    if table:
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        resultDict = returnErrorMsg(errorCode["system_error"])
        return jsonify(resultDict)


# 删除爬虫项目
@app.route("/removeSpiderProject", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def removeSpiderProject():
    PROJECTS_FOLDER = "projects"
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    project_name = dataDict.get("projectName", "")
    if not project_name:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    path = join(os.path.abspath(os.getcwd()), PROJECTS_FOLDER)
    project_path = join(path, project_name)
    if not project_path:
        # delete project file tree
        rmtree(project_path)
        # delete project
        result = SpiderProject.objects.filter(project_name=project_name).delete()
        return jsonify({'result': result})
    else:
        rmtree(project_path)
        result = SpiderProject.objects.filter(project_name=project_name).delete()
        return jsonify({'result': result})


# 打包爬虫项目
@app.route("/buildSpiderProject", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def buildSpiderProject():
    # path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    project_name = dataDict.get("projectName", "")
    if not project_name:
        resultDict = returnErrorMsg(errorCode["param_error"])
        return jsonify(resultDict)
    path = PROJECTS_FOLDER
    project_path = join(path, project_name)
    build_project(project_name)
    egg = find_egg(project_path)
    # update built_at info
    built_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # if project exists, update egg, description, built_at info
    SpiderProjectList = SpiderProject.query.filter_by(project_name=project_name).first()
    if SpiderProjectList:
        id = SpiderProjectList.project_id
        dataDict = {
            "builtAt": built_at,
            "spiderEgg": egg,
            "updatedAt": built_at
        }
        dataDict = json.loads(json.dumps(dataDict))
        intColumnClinetNameList = [u'projectId', u'configurable']
        table = updataById(SpiderProject, dataDict, "project_id", id, tableChangeDic, intColumnClinetNameList)
        if table:
            resultDict = returnMsg({})
            return jsonify(resultDict)
        else:
            resultDict = returnErrorMsg("insert fail")
            return jsonify(resultDict)
    # if project does not exists in db, create it
    else:
        dataDict = {
            "projectName": project_name,
            "builtAt": built_at,
            "spiderEgg": egg,
            "updatedAt": built_at
        }
        dataDict = json.loads(json.dumps(dataDict))
        columsStr = (
            dataDict.get("projectDesc", None), dataDict.get("projectName", None), dataDict.get("spiderEgg", None),
            dataDict.get("configurable", None), dataDict.get("builtAt", None), dataDict.get("createdAt", None),
            dataDict.get("updatedAt", None))
        table = insertToSQL(SpiderProject, *columsStr)
        if not table:
            resultDict = returnErrorMsg("insert fail")
            return jsonify(resultDict)
        resultDict = returnMsg({})
        return jsonify(resultDict)


# 部署爬虫项目
@app.route("/deploySpiderProject", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def deploySpiderProject():
    # path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    project_name = dataDict.get("projectName", "")
    node_id = dataDict.get("nodeId", "")
    if not project_name:
        resultDict = returnErrorMsg("not find project")
        return jsonify(resultDict)
    path = PROJECTS_FOLDER
    project_path = join(path,project_name)
    # find egg file
    egg = find_egg(project_path)
    egg_file = open(join(project_path, egg), 'rb')
    # get node and project model
    node = SpiderNode.query.filter_by(node_id=node_id).first()
    project = SpiderProject.query.filter_by(project_name=project_name).first()
    # execute deploy operation
    scrapyd = ScrapydAPI(scrapyd_url(node.node_ip, node.node_port))
    try:
        scrapyd.add_version(project_name, int(time.time()), egg_file.read())
        # update deploy info
        deployed_at = datetime.datetime.now()
        deployed_at = deployed_at.strftime("%Y-%m-%d %H:%M:%S")
        SpiderNodeList = SpiderNode.query.filter_by(node_id=node_id).first()

        description = SpiderNodeList.node_ip
        SpiderDeploy.query.filter_by(description=description).delete()
        deployDataDict = {
            "description": description,
            "deployedAt": deployed_at,
            "updatedAt": deployed_at,
            "createdAt": deployed_at
        }
        deployDataDict = json.loads(json.dumps(deployDataDict))
        columsStr = (deployDataDict.get("description", None), deployDataDict.get("deployedAt", None),
                     deployDataDict.get("createdAt", None), deployDataDict.get("updatedAt", None))
        table = insertToSQL(SpiderDeploy, *columsStr)
        dataDict = {'projectName':project_name}
        intColumnClinetNameList = [u'nodeId', u'nodePort', u'nodeStatus', u'deployStatus']
        updataById(SpiderNode, dataDict, "node_id", node_id,NodetableChangeDic, intColumnClinetNameList)
        if not table:
            resultDict = returnErrorMsg("insert fail")
            return jsonify(resultDict)
        resultDict = returnMsg({'result': 1})
        return jsonify(resultDict)
    except Exception:
        resultDict = returnErrorMsg()
        return jsonify(resultDict)




# 启动爬虫项目
@app.route("/startSpiderProject", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def startSpiderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    project_name = dataDict.get("projectName", "")
    node_id = dataDict.get("nodeId", "")
    spider_name = dataDict.get("spiderName", "")
    if not (project_name and node_id and spider_name):
        resultDict = returnErrorMsg("not find project")
        return jsonify(resultDict)
    node = SpiderNode.query.filter_by(node_id=node_id).first()
    scrapyd = ScrapydAPI(scrapyd_url(node.node_ip, node.node_port))
    try:
        job = scrapyd.schedule(project_name, spider_name)
        dataDict = {'deployStatus':1}
        intColumnClinetNameList = [u'nodeId', u'nodePort', u'nodeStatus', u'deployStatus']
        updataById(SpiderNode, dataDict, "node_id", node_id, NodetableChangeDic, intColumnClinetNameList)
        resultDict = returnMsg({'job': job, "result": 1})
        return jsonify(resultDict)
    except:
        resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 爬虫工作列表
@app.route("/jobSpiderProject", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def jobSpiderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    project_name = dataDict.get("projectName", "")
    node_id = dataDict.get("nodeId", "")
    if not (project_name and node_id):
        resultDict = returnErrorMsg("not find project")
        return jsonify(resultDict)
    node = SpiderNode.query.filter_by(node_id=node_id).first()
    scrapyd = ScrapydAPI(scrapyd_url(node.node_ip, node.node_port))
    try:
        result = scrapyd.list_jobs(project_name)
        jobs = []
        statuses = ['pending', 'running', 'finished']
        for status in statuses:
            for job in result.get(status):
                job['status'] = status
                job['node_id'] = node_id
                job['project_name'] = project_name
                jobs.append(job)
        resultDict = returnMsg({'job': jobs, "result": 1})
        return jsonify(resultDict)
    except:
        resultDict = returnErrorMsg()
        return jsonify(resultDict)

# 爬虫项目列表
@app.route("/SpiderProjectList", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def SpiderProjectList():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    node_id = dataDict.get("nodeId", "")
    if not node_id:
        resultDict = returnErrorMsg("not find node_id")
        return jsonify(resultDict)
    node = SpiderNode.query.filter_by(node_id=node_id).first()
    if node:
        scrapyd = ScrapydAPI(scrapyd_url(node.node_ip, node.node_port))
    else:
        resultDict = returnErrorMsg("not data")
        return jsonify(resultDict)
    try:
        projects = scrapyd.list_projects()
        lis = []
        for project in projects:
            lis.append({'projectName': project})
        resultDict = returnMsg({'result': 1, "project_list": lis})
        return jsonify(resultDict)
    except:
        resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 爬虫项目列表
@app.route("/SpiderList", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def SpiderList():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    node_id = dataDict.get("nodeId", "")
    # project_name = dataDict.get("projectName","")
    if not node_id:
        resultDict = returnErrorMsg("not find node_id")
        return jsonify(resultDict)
    node = SpiderNode.query.filter_by(node_id=node_id).first()
    if node:
        scrapyd = ScrapydAPI(scrapyd_url(node.node_ip, node.node_port))
    else:
        resultDict = returnErrorMsg("not data")
        return jsonify(resultDict)
    try:
        projects = scrapyd.list_projects()
        for project in projects:
            spiders = scrapyd.list_spiders(project)
            spiders = [{'name': spider, 'id': index + 1,"project_name":project,"node_id":node_id} for index, spider in enumerate(spiders)]
            resultDict = returnMsg({'result': 1, "project_list": spiders})
            return jsonify(resultDict)
    except:
        resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 停止工作爬虫
@app.route("/stopSpiderProject", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def stopSpiderProject():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    project_name = dataDict.get("projectName", "")
    node_id = dataDict.get("nodeId", "")
    job_id = dataDict.get("jobId", "")
    if not (project_name and node_id and job_id):
        resultDict = returnErrorMsg("not find project")
        return jsonify(resultDict)
    node = SpiderNode.query.filter_by(node_id=node_id).first()
    try:
        scrapyd = ScrapydAPI(scrapyd_url(node.node_ip, node.node_port))
        res = scrapyd.cancel(project_name, job_id)
        dataDict = {'deployStatus':0}
        intColumnClinetNameList = [u'nodeId', u'nodePort', u'nodeStatus', u'deployStatus']
        updataById(SpiderNode, dataDict, "node_id", node_id, NodetableChangeDic, intColumnClinetNameList)
        resultDict = returnMsg({'res': res, "result": 1})
        return jsonify(resultDict)
    except:
        resultDict = returnErrorMsg()
        return jsonify(resultDict)


#上传爬虫项目
@app.route("/uploadSpiderProject", methods=["POST"])
# @jwt_required
# @updateLog('spider_project')
def uploadSpiderProject():
    # jsonData = request.get_data()
    # dataDict = json.loads(jsonData)
    # typeFile = dataDict.get("typeFile", "")
    path = PROJECTS_FOLDER
    file = request.files['file']  # 从表单的file字段获取文件，file为该表单的name值
    if file and allowed_file(file.filename):  # 判断是否是允许上传的文件类型
        fname = file.filename
        # filename = secure_filename(file.filename)
        egg_name = fname.split('.')[0]
        file_dir = os.path.join(path,egg_name.split('-')[0])
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        ext = fname.rsplit('.', 1)[1]  # 获取文件后缀
        unix_time = int(time.time())
        new_filename = str(unix_time)+'.'+ext  # 修改了上传的文件名
        # new_filename = '12' + '.' + ext  # 修改了上传的文件名
        file.save(os.path.join(file_dir, new_filename))  # 保存文件到upload目录
        dataDict = {
            "projectName":egg_name.split('-')[0],
            "spiderEgg":new_filename,
            "createdAt":getTimeStrfTimeStampNow(),
            "builtAt":getTimeStrfTimeStampNow(),
            "updatedAt":getTimeStrfTimeStampNow()
        }
        columsStr = (
        dataDict.get("projectDesc", None), dataDict.get("projectName", None), dataDict.get("spiderEgg", None),
        dataDict.get("configurable", None), dataDict.get("builtAt", None), dataDict.get("createdAt", None),
        dataDict.get("updatedAt", None))
        table = insertToSQL(SpiderProject, *columsStr)
        if not table:
            resultDict = returnErrorMsg("insert fail")
            return jsonify(resultDict)
        resultDict = returnMsg({})
        return jsonify(resultDict)
    else:
        return jsonify({"error": -1, "errmsg": "failed"})


def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['egg'])
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS