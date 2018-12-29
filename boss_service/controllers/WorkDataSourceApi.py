# coding:utf-8
import datetime
from flask import jsonify, request, json
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from version.v3.bossConfig import app
from common.OperationOfDB import querySql, findById, sqlFunctionCall, sqlFunctionCallOther, executeSql
from common.ReturnMessage import returnMsg, returnErrorMsg,errorCode
from models.Boss.User import User
from common.Log import queryLog
from controllers.CrawlerApi import getAllReleaseDept
from models.Boss.UserRole import UserRole
from models.Boss.RoleMenu import RoleMenu
from models.Boss.Menu import Menu


# 数据维护员
@app.route("/getDataMaintainLists", methods=["POST"])
# @jwt_required
def getDataMaintainLists():
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
    adminName = adminTable.admin_name
    dataRole = ["200501", "200502", "200503"]
    roleInfo = getRole(dataRole, adminId)
    if roleInfo.get("code") == 0:
        return jsonify(roleInfo)
    sql = "select check_status ,item_type,IFNULL(count(*), 0) from data_temp_item where create_person='{}' GROUP BY check_status ,item_type ".format(
        adminName)
    resualtList = executeSql(sql)
    infoList = []
    otherList = []
    for x in range(4):
        for y in range(1, 4):
            otherList.append({"itemType": y, "checkStatus": x})
    if resualtList:
        for result in resualtList:
            checkStatus = result[0]
            itemType = result[1]
            count = result[2]
            otherList.remove({"itemType": itemType, "checkStatus": checkStatus})
            infoDict = {
                "checkStatus": checkStatus,
                "itemType": itemType,
                "count": count,
                "adminName": adminName,
            }
            infoList.append(infoDict)
    for otherDict in otherList:
        infoDict = {
            "checkStatus": otherDict["checkStatus"],
            "itemType": otherDict["itemType"],
            "count": 0,
            "adminName": adminName,
        }
        infoList.append(infoDict)
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


# 数据审核员
@app.route("/getWiathDataMaintainLists", methods=["POST"])
# @jwt_required
def getWiathDataMaintainLists():
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
    adminName = adminTable.admin_name
    dataRole = ["200501", "200502", "200503"]
    roleInfo = getRole(dataRole, adminId)
    if roleInfo.get("code") == 0:
        return jsonify(roleInfo)
    sql = "select check_status ,item_type,IFNULL(count(*), 0) from data_temp_item where create_person='{}' and check_status != 0 GROUP BY check_status ,item_type".format(
        adminName)
    resualtList = executeSql(sql)
    infoList = []
    otherList = []
    countList = [0,0,0]
    for x in range(1, 4):
        for y in range(1, 4):
            otherList.append({"itemType": y, "checkStatus": x})
    if resualtList:
        for result in resualtList:
            if result[1] ==1 and result[0] in (2, 3):
                countList[0] += result[2]
            elif result[1] == 2 and result[0] in (2, 3):
                countList[1] += result[2]
            elif result[1] == 3 and result[0] in (2, 3):
                countList[2] += result[2]
            checkStatus = result[0]
            itemType = result[1]
            count = result[2]
            otherList.remove({"itemType": itemType, "checkStatus": checkStatus})
            infoDict = {
                "checkStatus": checkStatus,
                "itemType": itemType,
                "count": count,
                "adminName": adminName,
            }
            infoList.append(infoDict)
    for otherDict in otherList:
        infoDict = {
            "checkStatus": otherDict["checkStatus"],
            "itemType": otherDict["itemType"],
            "count": 0,
            "adminName": adminName,
        }
        infoList.append(infoDict)
    for itemType in range(3):
        infoList.append({
            "checkStatus": (2, 3),
            "itemType": itemType +1,
            "count": countList[itemType],
            "adminName": adminName,
        })
    resultDict = returnMsg(infoList)
    return jsonify(resultDict)


def getRole(dataRole, adminId):
    # 权限获取
    RoleList = UserRole.query.filter(UserRole.user_id == adminId).all()
    RoleIds = [role.role_id for role in RoleList]
    menukeys = []
    if RoleIds:
        menuList = RoleMenu.query.filter(RoleMenu.role_id.in_(RoleIds)).all()
        menuIds = [menu.menu_id for menu in menuList]
        if menuIds:
            menuKeyList = Menu.query.filter(Menu.menu_id.in_(menuIds)).all()
            menukeys = [menukey.menu_key for menukey in menuKeyList]
    if not menukeys:
        resultDict = returnErrorMsg("not find user Role")
        return resultDict
    if dataRole not in menukeys:
        resultDict = returnErrorMsg("No authority ")
        return resultDict
    return True


"""[{'count': 2L, 'checkStatus': 2, 'adminName': u'admin2', 'itemType': 1}, 
{'count': 2L, 'checkStatus': 2, 'adminName': u'admin2', 'itemType': 3}, 
  {'count': 0, 'checkStatus': 2, 'adminName': u'admin2', 'itemType': 2},
{'count': 0, 'checkStatus': 1, 'adminName': u'admin2', 'itemType': 1}, 
{'count': 0, 'checkStatus': 1, 'adminName': u'admin2', 'itemType': 2},
 {'count': 0, 'checkStatus': 1, 'adminName': u'admin2', 'itemType': 3},
   {'count': 0, 'checkStatus': 3, 'adminName': u'admin2', 'itemType': 1},
    {'count': 0, 'checkStatus': 3, 'adminName': u'admin2', 'itemType': 2},
     {'count': 0, 'checkStatus': 3, 'adminName': u'admin2', 'itemType': 3},
      {'count': 4L, 'checkStatus': (2, 3), 'adminName': u'admin2', 'itemType': 1}, 
      {'count': 4L, 'checkStatus': (2, 3), 'adminName': u'admin2', 'itemType': 2}, 
      {'count': 4L, 'checkStatus': (2, 3), 'adminName': u'admin2', 'itemType': 3}]"""
