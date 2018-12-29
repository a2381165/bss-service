# coding:utf-8
import json
import os
import re
import time

from flask import json
from flask import jsonify, url_for
from flask import request, make_response
from flask_jwt_extended import get_jwt_identity, jwt_required, current_user
from werkzeug.utils import secure_filename

from common.DatatimeNow import getTimeStrfTimeStampNow
from common.OperationOfDB import findById, addTokenToSql, insertToSQL
from common.ReturnMessage import returnMsg, errorCode, returnErrorMsg
from common.Uploader import Uploader
from config import app
from models.Data.ServiceAttach import ServiceAttach
from models.Data.TempItem import TempItem
from models.Data.TempService import TempService
from version.v3.bossConfig import app


# 上传word
@app.route('/uploadContract', methods=['POST'])
@jwt_required
def uploadContract():
    try:
        userId = get_jwt_identity()
        file = request.files.get('file', None)
        if not (file):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        # 获取不到中文
        filename = secure_filename(file.filename)
        # upload_file_size = len(file.read()) # 文件大小
        upload_file_size = request.content_length  # 文件大小
        # 后缀名
        upload_file_ext = filename.split(".")[-1]
        filename = u"{}.{}".format(filename[:-1], upload_file_ext)
        # filename = file.filename
        # 文件类型检验
        allow_type = [
            ".png", ".jpg", ".jpeg", ".gif", ".bmp",
            ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
            ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
            ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
            ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
        ]
        if ".{}".format(upload_file_ext) not in allow_type:
            resultDict = returnErrorMsg("Server does not allow type!")
            return jsonify(resultDict)
        # 文件大小
        fileMaxSize = 20480000
        if upload_file_size > fileMaxSize:
            resultDict = returnErrorMsg("fileSize too big")
            return jsonify(resultDict)

        # 文件路径是否存在
        cwdPath = os.getcwd()
        contractPath = cwdPath + r"/static/user/" + str(userId) + r"/fujian/temp"
        # pdfContractPath = cwdPath + r"/static/user" + "/" + str(userId) + r"/contract"
        if not os.path.exists(contractPath):
            os.makedirs(contractPath)
        try:
            file.save(os.path.join(contractPath, filename))
        except Exception as e:
            print e
            resultDict = returnErrorMsg(e)
            return jsonify(resultDict)
        cuPath = "user/" + str(userId) + r"/fujian/temp"
        cupath = os.path.join(cuPath, filename)
        downloadUrl = url_for("/static", filename=cupath, _external=True)

        # #windows 使用
        # from win32com import client
        #
        # try:
        #     doc_name = os.path.join(contractPath,filename)
        #     pdf_name = os.path.join(pdfContractPath,pdf_name)
        #     word = client.DispatchEx("Word.Application")
        #     # if os.path.exists(pdf_name):
        #     #     os.remove(pdf_name)
        #     worddoc = word.Documents.Open(doc_name, ReadOnly=1)
        #     worddoc.SaveAs(pdf_name, FileFormat=17)
        #     worddoc.Close()
        # except Exception as e:
        #     print e
        #     resultDict = returnErrorMsg()
        #     return jsonify(resultDict)
        # docx2pdf = Docx2PDF()
        # docx2pdf.userDocToPdf(filename, userId)
        return_info = {
            # 保存后的文件名称
            'url': filename,
            # 原始文件名
            'original': file.filename,
            'type': upload_file_ext,
            # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
            # 'state': state,
            'size': upload_file_size,
            'downloadUrl': downloadUrl,
        }

        resultDict = returnMsg(return_info)
        return jsonify(resultDict)
    except Exception as e:
        print e
        resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 上传 excel
@app.route('/uploadServiceFile', methods=['POST'])
@jwt_required
def uploadServiceFile():
    try:
        id = request.form.get("id", None)
        file = request.files.get('file', None)
        if not (file and id):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        # 获取不到中文
        filename = secure_filename(file.filename)
        # upload_file_size = len(file.read()) # 文件大小
        upload_file_size = request.content_length  # 文件大小
        # 后缀名
        upload_file_ext = filename.split(".")[-1]
        filename = "{}".format(id)
        filename = u"{}.{}".format(filename, upload_file_ext)
        # filename = file.filename
        # 文件类型检验
        allow_type = [
            ".xls", ".xlsx"
        ]
        if ".{}".format(upload_file_ext) not in allow_type:
            resultDict = returnErrorMsg(errorCode["upload_only_excel"])
            return jsonify(resultDict)
        # 文件大小
        fileMaxSize = 20480000
        if upload_file_size > fileMaxSize:
            resultDict = returnErrorMsg("fileSize too big")
            return jsonify(resultDict)

        # 文件路径是否存在
        cwdPath = os.getcwd()
        contractPath = cwdPath + r"/static/zxb/service/temp"
        # pdfContractPath = cwdPath + r"/static/user" + "/" + str(userId) + r"/contract"
        if not os.path.exists(contractPath):
            os.makedirs(contractPath)
        try:
            file.save(os.path.join(contractPath, filename))
        except Exception as e:
            print e
            resultDict = returnErrorMsg(e)
            return jsonify(resultDict)
        cuPath = "zxb/service/temp/"
        cupath = os.path.join(cuPath, filename)
        downloadUrl = url_for("static", filename=cupath, _external=True)
        # 更新 tempservice
        is_update = updateTempService(id, cupath,file.filename)
        if not is_update:
            resultDict = returnErrorMsg("update fail")
            return jsonify(resultDict)
        return_info = {
            # 保存后的文件名称
            'url': filename,
            # 原始文件名
            'original': file.filename,
            'type': upload_file_ext,
            # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
            # 'state': state,
            'size': upload_file_size,
            'downloadUrl': downloadUrl,
        }

        resultDict = returnMsg(return_info)
        return jsonify(resultDict)
    except Exception as e:
        print e
        resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 上传 政策来源service 附件
@app.route('/uploadItemServiceFile', methods=['POST'])
@jwt_required
def uploadItemServiceFile():
    try:
        title = request.form.get("attachTitle", None)
        content = request.form.get("attachPath", None)
        file = request.files.get('file', None)
        if not (title):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        if not (file or content):
            resultDict = returnErrorMsg("file and attachPath must has one")
            return jsonify(resultDict)
        adminName = current_user.admin_name
        if not file:
            #  添加 serviceAttach
            is_insert = insertServiceAttach(None, title, content, adminName, 2)  # # type 是 2 自己写的链接附件
            if not is_insert:
                resultDict = returnErrorMsg(errorCode["system_error"])
                return jsonify(resultDict)
            else:
                return_info = {
                    'attachTitle': title,
                    'attachPath': content,
                }
                resultDict = returnMsg(return_info)
                return jsonify(resultDict)
        # 获取不到中文
        filename = secure_filename(file.filename)
        # upload_file_size = len(file.read()) # 文件大小
        upload_file_size = request.content_length  # 文件大小
        # 后缀名
        upload_file_ext = filename.split(".")[-1]
        # filename = "{}".format(id)
        now = time.time()
        filename = u"{}{}.{}".format(now,filename[:-1], upload_file_ext)
        # filename = file.filename
        # 文件类型检验
        allow_type = [
            ".png", ".jpg", ".jpeg", ".gif", ".bmp",
            ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
            ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
            ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
            ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
        ]
        if ".{}".format(upload_file_ext) not in allow_type:
            resultDict = returnErrorMsg("Server does not allow type!")
            return jsonify(resultDict)
        # 文件大小
        fileMaxSize = 20480000
        if upload_file_size > fileMaxSize:
            resultDict = returnErrorMsg("fileSize too big")
            return jsonify(resultDict)

        # 文件路径是否存在
        cwdPath = os.getcwd()
        contractPath = cwdPath + r"/static/zxb/service/temp"
        # pdfContractPath = cwdPath + r"/static/user" + "/" + str(userId) + r"/contract"
        if not os.path.exists(contractPath):
            os.makedirs(contractPath)
        try:
            file.save(os.path.join(contractPath, filename))
        except Exception as e:
            print e
            resultDict = returnErrorMsg(e)
            return jsonify(resultDict)
        cuPath = "zxb/service/temp"
        cupath = os.path.join(cuPath, filename)
        downloadUrl = url_for("static", filename=cupath, _external=True)
        #  添加 serviceAttach
        is_insert = insertServiceAttach(upload_file_size, title, cupath, adminName, 1)  # type 是 1 上传附件
        if not is_insert:
            resultDict = returnErrorMsg(errorCode["system_error"])
            return jsonify(resultDict)
        return_info = {
            # 保存后的文件名称
            'url': filename,
            # 原始文件名
            'original': file.filename,
            'type': upload_file_ext,
            # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
            # 'state': state,
            'size': upload_file_size,
            'downloadUrl': downloadUrl,
            'attachTitle': title,
            'attachPath': downloadUrl,
        }

        resultDict = returnMsg(return_info)
        return jsonify(resultDict)
    except Exception as e:
        print e
        resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 上传 更新政策来源service 附件
@app.route('/uploadUpdateItemServiceFile', methods=['POST'])
@jwt_required
def uploadUpdateItemServiceFile():
    try:
        id = request.form.get("id",None)
        title = request.form.get("attachTitle", None)
        content = request.form.get("attachPath", None)
        file = request.files.get('file', None)
        if not (id and title):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        if not (file or content):
            resultDict = returnErrorMsg("file and attachPath must has one")
            return jsonify(resultDict)
        adminName = current_user.admin_name
        if not file:
            #  添加 serviceAttach
            is_update= updateServiceAttach(id,None, title, content, adminName, 2)  # # type 是 2 自己写的链接附件
            if not is_update:
                resultDict = returnErrorMsg("update fail")
                return jsonify(resultDict)
            elif is_update == "not person":
                resultDict = returnErrorMsg(errorCode["serviceAttach_updata"])
                return jsonify(resultDict)
            else:
                return_info = {
                    'attachTitle': title,
                    'attachPath': content,
                }
                resultDict = returnMsg(return_info)
                return jsonify(resultDict)
        # 获取不到中文
        filename = secure_filename(file.filename)
        # upload_file_size = len(file.read()) # 文件大小
        upload_file_size = request.content_length  # 文件大小
        # 后缀名
        upload_file_ext = filename.split(".")[-1]
        # filename = "{}".format(id)
        filename = u"{}.{}".format(filename[:-1], upload_file_ext)
        # filename = file.filename
        # 文件类型检验
        allow_type = [
            ".png", ".jpg", ".jpeg", ".gif", ".bmp",
            ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
            ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
            ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
            ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
        ]
        if ".{}".format(upload_file_ext) not in allow_type:
            resultDict = returnErrorMsg("Server does not allow type!")
            return jsonify(resultDict)
        # 文件大小
        fileMaxSize = 20480000
        if upload_file_size > fileMaxSize:
            resultDict = returnErrorMsg("fileSize too big")
            return jsonify(resultDict)

        # 文件路径是否存在
        cwdPath = os.getcwd()
        contractPath = cwdPath + r"/static/zxb/service/temp"
        # pdfContractPath = cwdPath + r"/static/user" + "/" + str(userId) + r"/contract"
        if not os.path.exists(contractPath):
            os.makedirs(contractPath)
        try:
            file.save(os.path.join(contractPath, filename))
        except Exception as e:
            print e
            resultDict = returnErrorMsg(e)
            return jsonify(resultDict)
        cuPath = "zxb/service/temp"
        cupath = os.path.join(cuPath, filename)
        downloadUrl = url_for("static", filename=cupath, _external=True)
        #  添加 serviceAttach
        is_update= updateServiceAttach(id,upload_file_size, title, cupath, adminName, 1)  # type 是 1 上传附件
        if not is_update:
            resultDict = returnErrorMsg("update fail")
            return jsonify(resultDict)
        return_info = {
            # 保存后的文件名称
            'url': filename,
            # 原始文件名
            'original': file.filename,
            'type': upload_file_ext,
            # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
            # 'state': state,
            'size': upload_file_size,
            'downloadUrl': downloadUrl,
            'attachTitle': title,
            'attachPath': downloadUrl,
        }

        resultDict = returnMsg(return_info)
        return jsonify(resultDict)
    except Exception as e:
        print e
        resultDict = returnErrorMsg()
        return jsonify(resultDict)


# 上传  图片 item 产品相册图片 多张
@app.route('/uploadUpdateTempItemImage', methods=['POST'])
@jwt_required
def uploadUpdateTempItemImage():
    try:
        itemId = request.form.get("itemId",None)
        files = request.files.get('file', None)
        if not (itemId and files):
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        _infoList = []
        _ifnoList2 = []
        for file in files:
            # 获取不到中文
            filename = secure_filename(file.filename)
            # upload_file_size = len(file.read()) # 文件大小
            upload_file_size = request.content_length  # 文件大小
            # 后缀名
            upload_file_ext = filename.split(".")[-1]
            # filename = "{}".format(id)
            now = getTimeStrfTimeStampNow()
            filename = u"{}{}.{}".format(now,filename[:-1], upload_file_ext)
            # filename = file.filename
            # 文件类型检验
            allow_type = [
                ".png", ".jpg", ".jpeg", ".gif", ".bmp",
                ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
                ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
                ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
                ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
            ]
            if ".{}".format(upload_file_ext) not in allow_type:
                resultDict = returnErrorMsg("Server does not allow type!")
                return jsonify(resultDict)
            # 文件大小
            fileMaxSize = 20480000
            if upload_file_size > fileMaxSize:
                resultDict = returnErrorMsg("fileSize too big")
                return jsonify(resultDict)

            # 文件路径是否存在
            cwdPath = os.getcwd()
            contractPath = cwdPath + r"/static/item/{}/temp/".format(itemId)
            # pdfContractPath = cwdPath + r"/static/user" + "/" + str(userId) + r"/contract"
            if not os.path.exists(contractPath):
                os.makedirs(contractPath)
            try:
                file.save(os.path.join(contractPath, filename))
            except Exception as e:
                print e
                resultDict = returnErrorMsg(e)
                return jsonify(resultDict)
            cuPath = "item/{}/temp/".format(itemId)
            cupath = os.path.join(cuPath, filename)
            downloadUrl = url_for("static", filename=cupath, _external=True)
            return_info = {
                # 保存后的文件名称
                'url': filename,
                # 原始文件名
                'original': file.filename,
                'type': upload_file_ext,
                # 上传状态，成功时返回SUCCESS,其他任何值将原样返回至图片上传框中
                # 'state': state,
                'size': upload_file_size,
                'downloadUrl': downloadUrl,
            }
            _ifnoList2.append(return_info)
            _infoList.append(cupath)
        #  添加 serviceAttach
        is_update= updateTempItemImage(itemId,_infoList)  # type 是 1 上传附件
        if not is_update:
            resultDict = returnErrorMsg("update fail")
            return jsonify(resultDict)


        resultDict = returnMsg(_ifnoList2)
        return jsonify(resultDict)
    except Exception as e:
        print e
        resultDict = returnErrorMsg()
        return jsonify(resultDict)

# 更新内容上传
@app.route("/updateContentInfo", methods=["GET", "POST", "OPTIONS"])
def updateContentInfo():
    mimetype = "application/json"
    result = {}
    action = request.args.get("action")
    # 解析JSON格式的配置文件
    with open(os.path.join("vender", "ueditor","config.json")) as fp:
        try:
            # 删除 `/**/` 之间的注释
            CONFIG = json.loads(re.sub(r"\/\*.*\*\/","", fp.read()))
        except:
            CONFIG = {}
    if action == "config":
        # 初始化时，返回配置文件给客户端
        result = CONFIG

    elif action in ("uploadimage", "uploadfile", "uploadvideo"):
        # 图片、文件、视频上传
        if action == "uploadimage":
            fieldName = CONFIG.get("imageFieldName")
            config = {
                "pathFormat": CONFIG["imagePathFormat"],
                "maxSize": CONFIG["imageMaxSize"],
                "allowFiles": CONFIG["imageAllowFiles"]
            }
        elif action == "uploadvideo":
            fieldName = CONFIG.get("videoFieldName")
            config = {
                "pathFormat": CONFIG["videoPathFormat"],
                "maxSize": CONFIG["videoMaxSize"],
                "allowFiles": CONFIG["videoAllowFiles"]
            }
        else:
            fieldName = CONFIG.get("fileFieldName")
            config = {
                "pathFormat": CONFIG["filePathFormat"],
                "maxSize": CONFIG["fileMaxSize"],
                "allowFiles": CONFIG["fileAllowFiles"]
            }
        if fieldName in request.files:
            field = request.files[fieldName]
            uploader = Uploader(field, config, app.static_folder)
            result = uploader.getFileInfo()
        else:
            result["state"] = "上传接口出错"
    elif action in ("uploadscrawl"):
        # 涂鸦上传
        fieldName = CONFIG.get("scrawlFieldName")
        config = {
            "pathFormat": CONFIG.get("scrawlPathFormat"),
            "maxSize": CONFIG.get("scrawlMaxSize"),
            "allowFiles": CONFIG.get("scrawlAllowFiles"),
            "oriName": "scrawl.png"
        }
        if fieldName in request.form:
            field = request.form[fieldName]
            uploader = Uploader(field, config, app.static_folder, "base64")
            result = uploader.getFileInfo()
        else:
            result["state"] = "上传接口出错"
    elif action in ("catchimage"):
        config = {
            "pathFormat": CONFIG["catcherPathFormat"],
            "maxSize": CONFIG["catcherMaxSize"],
            "allowFiles": CONFIG["catcherAllowFiles"],
            "oriName": "remote.png"
        }
        fieldName = CONFIG["catcherFieldName"]
        if fieldName in request.form:
            # 这里比较奇怪，远程抓图提交的表单名称不是这个
            source = []
        elif "%s[]" % fieldName in request.form:
            # 而是这个
            source = request.form.getlist("%s[]" % fieldName)
        _list = []
        for imgurl in source:
            uploader = Uploader(imgurl, config, app.static_folder, "remote")
            info = uploader.getFileInfo()
            _list.append({
                "state": info["state"],
                "url": info["url"],
                "original": info["original"],
                "source": imgurl,
            })
        result["state"] = "SUCCESS" if len(_list) > 0 else "ERROR"
        result["list"] = _list
    else:
        result["state"] = "请求地址出错"
    result = json.dumps(result)
    if "callback" in request.args:
        callback = request.args.get("callback")
        if re.match(r"^[\w_]+$", callback):
            result = "%s(%s)" % (callback, result)
            mimetype = "application/javascript"
        else:
            result = json.dumps({"state": "callback参数不合法"})
    res = make_response(result)
    res.mimetype = mimetype
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Access-Control-Allow-Headers"] = "X-Requested-With,X_Requested_With"
    return res



def updateTempItemImage(id,urls):
    table = findById(TempItem,"item_id",id)
    table.item_album = urls
    table = addTokenToSql(table)
    if table:
        return True
    else:
        return False

def updateServiceAttach(id, attach_size, title, cupath, adminName, type):
    if type(id) == str:
        try:
            id=int(id)
        except:
            pass
    table = findById(ServiceAttach, "id", id)
    if not table:
        return False
    if table.create_person != adminName:
        return "not person"
    table.attach_size = attach_size
    table.attach_title = title
    table.attach_path = cupath
    table.type = type
    table = addTokenToSql(table)
    if not table:
        return False
    return True


def insertServiceAttach(attach_size, title, cupath, adminName, type):
    now = getTimeStrfTimeStampNow()
    ServiceAttachStr = (None, attach_size, title, cupath, now, type, adminName)
    table = insertToSQL(ServiceAttach, *ServiceAttachStr)
    if not table:
        return False
    return True


def updateTempService(id, cupath,filename):
    table = findById(TempService, "id", id)
    if not table:
        return False
    pathDict = {
        "path":cupath,
        "name":filename
    }
    table.forecast_path = json.dumps(pathDict)
    table = addTokenToSql(table)
    if not table:
        return False
    return True
