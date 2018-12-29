# -*- coding: utf-8 -*-
import json
import os

from flask import request, json, jsonify, url_for
from flask_jwt_extended import jwt_required

from common.Log import queryLog
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Data.Category import Category
from models.Data.Department import Department
from version.v3.bossConfig import app


@app.route("/getDeptImgList", methods=["POST"])
@jwt_required
@queryLog("data_department")
def getDeptImgList():
    jsonData = request.get_data()
    dataDict = json.loads(jsonData)
    deptId = dataDict.get("deptId")
    if deptId:
        deptTable = Department.query.filter(Department.dept_id == deptId).first()
        if deptTable:
            try:
                table = Category.query.filter(Category.category_id == deptTable.category_id).first()
                categoryCode = table.category_code
                # categoryCode = deptTable.category.category_code
            except:
                categoryCode = None
            if categoryCode:
                categoryClass = str(categoryCode)[0]
                imgPath = r"./static/dept_img/%s00/%s" %(categoryClass,categoryCode)
                infoList = []
                for pathStr, dirList, fileList in os.walk(imgPath):
                    for imgFile in fileList:
                        pathFile = "dept_img/%s00/%s" %(categoryClass,categoryCode) + "/" + imgFile
                        resultFile = url_for("static",filename=pathFile, _external=True)
                        infoList.append(resultFile)
                resultDict = returnMsg(infoList)
            else:
                resultDict = returnErrorMsg(errorCode["param_error"])
        else:
            resultDict = returnErrorMsg(errorCode["param_error"])
    else:
        resultDict = returnErrorMsg(errorCode["param_error"])
    return jsonify(resultDict)