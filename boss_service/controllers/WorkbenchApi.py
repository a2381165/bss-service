# coding:utf-8
import datetime
from flask import jsonify, request, json
from flask_jwt_extended import jwt_required, get_jwt_identity, current_user

from version.v3.bossConfig import app
from common.OperationOfDB import querySql, findById, sqlFunctionCall, sqlFunctionCallOther
from common.ReturnMessage import returnMsg, returnErrorMsg,errorCode
from models.Boss.User import User
from common.Log import queryLog
from controllers.CrawlerApi import getAllReleaseDept
from models.Boss.UserRole import UserRole
from models.Boss.RoleMenu import RoleMenu
from models.Boss.Menu import Menu


@app.route("/getWorkList", methods=["POST"])
# @jwt_required
# @queryLog("data_source")
def getWorkList():
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
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
        return jsonify(resultDict)
    departRole = ["200201", "200202"]
    dataRole = ["200501", "200502", "200503"]
    sourceRole = ["200601", "200602"]
    roleId =None
    adminName = adminTable.admin_name
    releaseDeptIdList = getAllReleaseDept(adminId,roleId )
    if len(releaseDeptIdList) == 0:
        releaseConditionStr = ""
    else:
        if len(releaseDeptIdList) == 1:
            releaseConditionStr = " and (dept_id in " + str(tuple(releaseDeptIdList)).replace("L", "").replace(",",
                                                                                                               "") + ")"
        else:
            releaseConditionStr = " and (dept_id in " + str(tuple(releaseDeptIdList)).replace("L", "") + ")"
    # print releaseConditionStr
    sqlOtherStrs = "call getTEE('{}',@b,@test)".format(releaseConditionStr)
    otherLists = sqlFunctionCall(sqlOtherStrs)
    if otherLists:
        print otherLists[0]
        print otherLists[1]
    # 部门录入数量
    # towork = "SELECT count(*) FROM data_source where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(check_time) and check_status=2" # 近七天
    # tomonth = "SELECT count(*) FROM data_source where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(check_time)  and check_status=2" # 近30天
    today = "select count(*) from data_source where to_days(check_time) = to_days(now()) and check_status=2"  # 今天
    towork = "SELECT count(*) FROM data_source WHERE YEARWEEK(date_format(check_time,'%Y-%m-%d')) = YEARWEEK(now())  and check_status=2"  # 本周
    tomonth = "SELECT count(*) FROM data_source WHERE DATE_FORMAT(check_time, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' ) and check_status=2"  # 本月
    waitCheckSource = "select count(*) from data_source WHERE check_status=1"  # 待审核部门
    # 数据
    waitMaintainItem = "select count(*) from zzh_source_data WHERE url_status=0 and item_type=1" + releaseConditionStr  # 申报待维护数据
    waitMaintainNotice = "select count(*) from zzh_source_data WHERE url_status=0 and item_type=2" + releaseConditionStr  # 公示公告待维护数据
    waitMaintainStatute = "select count(*) from zzh_source_data WHERE url_status=0 and item_type=3" + releaseConditionStr  # 政策法规待维护数据
    alsoMaintainItem = "select count(*) from data_temp_item WHERE create_person='{}' and item_type=1 and check_status=0".format(
        adminName)  # 申报已经维护
    alsoMaintainNotice = "select count(*) from data_temp_item WHERE create_person='{}' and item_type=2 and check_status=0".format(
        adminName)  # 公示公告已经维护
    alsoMaintainStatute = "select count(*) from data_temp_item WHERE create_person='{}' and item_type=3 and check_status=0".format(
        adminName)  # 政策法规已经维护
    waitCheckDataItem = "select count(*) from data_temp_item WHERE create_person='{}' and item_type=1 and check_status=1".format(
        adminName)  # 申报待审核
    waitCheckDataNotice = "select count(*) from data_temp_item WHERE create_person='{}' and item_type=2 and check_status=1".format(
        adminName)  # 公示公告待审核
    waitCheckDataStatute = "select count(*) from data_temp_item WHERE create_person='{}' and item_type=3 and check_status=1".format(
        adminName)  # 政策法规待审核
    sourceDict = {}
    deptDict = {}
    dataDict = {}
    for key in menukeys:
        if key in departRole:
            todayNum = querySql(today)
            toworkNum = querySql(towork)
            tomonthNum = querySql(tomonth)
            deptDict = {
                "todayNum": todayNum,
                "toworkNum": toworkNum,
                "tomonthNum": tomonthNum,
            }
        elif key in sourceRole:
            waitCheckSourceNum = querySql(waitCheckSource)
            waitMaintainItemNum = querySql(waitMaintainItem, isOther=True)
            waitMaintainNoticeNum = querySql(waitMaintainNotice, isOther=True)
            waitMaintainStatuteNum = querySql(waitMaintainStatute, isOther=True)
            sourceDict = {
                "waitCheckSourceNum": waitCheckSourceNum,
                "waitMaintainItemNum": waitMaintainItemNum,
                "waitMaintainNoticeNum": waitMaintainNoticeNum,
                "waitMaintainStatuteNum": waitMaintainStatuteNum,
            }
        elif key in dataRole:
            alsoMaintainItemNum = querySql(alsoMaintainItem)
            alsoMaintainNoticeNum = querySql(alsoMaintainNotice)
            alsoMaintainStatuteNum = querySql(alsoMaintainStatute)
            waitCheckDataItemNum = querySql(waitCheckDataItem)
            waitCheckDataNoticeNum = querySql(waitCheckDataNotice)
            waitCheckDataStatuteNum = querySql(waitCheckDataStatute)
            dataDict = {
                "alsoMaintainItemNum": alsoMaintainItemNum,
                "alsoMaintainNoticeNum": alsoMaintainNoticeNum,
                "alsoMaintainStatuteNum": alsoMaintainStatuteNum,
                "waitCheckDataItemNum": waitCheckDataItemNum,
                "waitCheckDataNoticeNum": waitCheckDataNoticeNum,
                "waitCheckDataStatuteNum": waitCheckDataStatuteNum,
            }
    infoDict = dict(deptDict=deptDict, sourceDict=sourceDict, dataDict=dataDict)
    # departmentNum = {
    #     "todayNum": todayNum,
    #     "toworkNum": toworkNum,
    #     "tomonthNum": tomonthNum,
    #     "waitCheckSourceNum": waitCheckSourceNum,
    #     "waitMaintainItemNum": waitMaintainItemNum,
    #     "waitMaintainNoticeNum": waitMaintainNoticeNum,
    #     "waitMaintainStatuteNum": waitMaintainStatuteNum,
    #     "alsoMaintainItemNum": alsoMaintainItemNum,
    #     "alsoMaintainNoticeNum": alsoMaintainNoticeNum,
    #     "alsoMaintainStatuteNum": alsoMaintainStatuteNum,
    #     "waitCheckDataItemNum": waitCheckDataItemNum,
    #     "waitCheckDataNoticeNum": waitCheckDataNoticeNum,
    #     "waitCheckDataStatuteNum": waitCheckDataStatuteNum,
    # }
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


@app.route("/getFunWorkList", methods=["POST"])
def getFunWorkList():
    """
     toDayNum                   今日部门数据
     toWorkNum                  本周 部门数
     toMonthNum                 本月 部门数
     waitCheckSourceNum         部门待审核数
     waitMaintainItemNum        待维护申报通知数
     waitMaintainNoticeNum      待维护公示公告数
     waitMaintainStatuteNum     待维护政策法规数
     alsoMaintainItemNum        申报通知已经维护
     alsoMaintainNoticeNum      公示公告已经维护
     alsoMaintainStatuteNum     政策法规已经维护
     waitCheckDataItemNum       申报通知待审核
     waitCheckDataNoticeNum     公示公告待审核
     waitCheckDataStatuteNum    政策法规待审核
     :return:
     """
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
    adminName = adminTable.admin_name
    releaseDeptIdList = getAllReleaseDept(adminId)
    if len(releaseDeptIdList) == 0:
        releaseConditionStr = ""
    else:
        if len(releaseDeptIdList) == 1:
            releaseConditionStr = str(tuple(releaseDeptIdList)).replace("L", "").replace(",", "")
        else:
            releaseConditionStr = str(tuple(releaseDeptIdList)).replace("L", "")
    sqlCountStr = "call getWorkBenchNum('{}',@todayNum,@toweekNum,@tomonthNum,@waitCheckSourceNum,@alsoMaintainItemNum,@alsoMaintainNoticeNum,@alsoMaintainStatuteNum,@waitCheckDataItemNum,@waitCheckDataNoticeNum,@waitCheckDataStatuteNum)".format(
        adminName)
    resualtList = sqlFunctionCall(sqlCountStr)
    sqlOtherStr = "call getWorkBenchNumOther('{}',@waitMaintainItemNum,@waitMaintainNoticeNum,@waitMaintainStatuteNum)".format(
        releaseConditionStr)
    otherList = sqlFunctionCallOther(sqlOtherStr)
    if otherList:
        waitMaintainItemNum = otherList[0]
        waitMaintainNoticeNum = otherList[1]
        waitMaintainStatuteNum = otherList[2]
        otherDict = {
            "waitMaintainItemNum": waitMaintainItemNum,
            "waitMaintainNoticeNum": waitMaintainNoticeNum,
            "waitMaintainStatuteNum": waitMaintainStatuteNum,
        }
    else:
        otherDict = dict(waitMaintainItemNum=0, waitMaintainNoticeNum=0, waitMaintainStatuteNum=0)
    if resualtList:
        todayNum = resualtList[0]
        toworkNum = resualtList[1]
        tomonthNum = resualtList[2]
        waitCheckSourceNum = resualtList[3]
        alsoMaintainItemNum = resualtList[4]
        alsoMaintainNoticeNum = resualtList[5]
        alsoMaintainStatuteNum = resualtList[6]
        waitCheckDataItemNum = resualtList[7]
        waitCheckDataNoticeNum = resualtList[8]
        waitCheckDataStatuteNum = resualtList[9]
        infoDict = {
            "todayNum": todayNum,
            "toworkNum": toworkNum,
            "tomonthNum": tomonthNum,
            "waitCheckSourceNum": waitCheckSourceNum,
            "alsoMaintainItemNum": alsoMaintainItemNum,
            "alsoMaintainNoticeNum": alsoMaintainNoticeNum,
            "alsoMaintainStatuteNum": alsoMaintainStatuteNum,
            "waitCheckDataItemNum": waitCheckDataItemNum,
            "waitCheckDataNoticeNum": waitCheckDataNoticeNum,
            "waitCheckDataStatuteNum": waitCheckDataStatuteNum,
        }
    else:
        infoDict = dict(todayNum=0, toworkNum=0, tomonthNum=0, waitCheckSourceNum=0, alsoMaintainItemNum=0,
                        alsoMaintainNoticeNum=0,
                        alsoMaintainStatuteNum=0, waitCheckDataItemNum=0, waitCheckDataNoticeNum=0,
                        waitCheckDataStatuteNum=0)
    infoDict = dict(infoDict, **otherDict)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 部门数据权限
@app.route("/getDeptRoleData", methods=["POST"])
def getDeptRoleData():
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
    adminName = adminTable.admin_name
    # sqlOtherStr = "call getDeptDataNum(@todayNum,@toweekNum,@tomonthNum,@waitCheckSourceNum)"
    sqlOtherStr = "call getDeptDataNum('{}',@todayNum,@toweekNum,@tomonthNum,@waitCheckSourceNum)".format(adminName)
    resualtList = sqlFunctionCall(sqlOtherStr)
    if resualtList:
        todayNum = resualtList[0]
        toworkNum = resualtList[1]
        tomonthNum = resualtList[2]
        waitCheckSourceNum = resualtList[3]
        infoDict = {
            "todayNum": todayNum,
            "toworkNum": toworkNum,
            "tomonthNum": tomonthNum,
            "waitCheckSourceNum": waitCheckSourceNum,
        }
    else:
        infoDict = {}
    resualtList = returnMsg(infoDict)
    return jsonify(resualtList)


# 数据待维护数量
@app.route("/getWaitCLData", methods=["POST"])
def getWaitCLData():
    adminId = get_jwt_identity()
    adminId = 11
    releaseDeptIdList = getAllReleaseDept(adminId)
    if len(releaseDeptIdList) == 0:
        releaseConditionStr = ""
    else:
        if len(releaseDeptIdList) == 1:
            releaseConditionStr = str(tuple(releaseDeptIdList)).replace("L", "").replace(",", "")
        else:
            releaseConditionStr = str(tuple(releaseDeptIdList)).replace("L", "")
    sqlOtherStr = "call getWorkBenchNumOther('{}',@waitMaintainItemNum,@waitMaintainNoticeNum,@waitMaintainStatuteNum)".format(
        releaseConditionStr)
    otherList = sqlFunctionCallOther(sqlOtherStr)
    if otherList:
        waitMaintainItemNum = otherList[0]
        waitMaintainNoticeNum = otherList[1]
        waitMaintainStatuteNum = otherList[2]
        otherDict = {
            "waitMaintainItemNum": waitMaintainItemNum,
            "waitMaintainNoticeNum": waitMaintainNoticeNum,
            "waitMaintainStatuteNum": waitMaintainStatuteNum,
        }
    else:
        otherDict = dict(waitMaintainItemNum=0, waitMaintainNoticeNum=0, waitMaintainStatuteNum=0)
    resualtList = returnMsg(otherDict)
    return jsonify(resualtList)


# 数据已维护数量
@app.route("/getAlsoCLData", methods=["POST"])
def getAlsoCLData():
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
    adminName = adminTable.admin_name
    sqlCountStr = "call getWorkBenchNum('{}',@alsoMaintainItemNum,@alsoMaintainNoticeNum,@alsoMaintainStatuteNum)".format(
        adminName)
    resualtList = sqlFunctionCall(sqlCountStr)
    if resualtList:
        alsoMaintainItemNum = resualtList[4]
        alsoMaintainNoticeNum = resualtList[5]
        alsoMaintainStatuteNum = resualtList[6]
        infoDict = {
            "alsoMaintainItemNum": alsoMaintainItemNum,
            "alsoMaintainNoticeNum": alsoMaintainNoticeNum,
            "alsoMaintainStatuteNum": alsoMaintainStatuteNum,
        }
    else:
        infoDict = dict(alsoMaintainItemNum=0,
                        alsoMaintainNoticeNum=0,
                        alsoMaintainStatuteNum=0)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 待审核数据
@app.route("/getWaitCheckData", methods=["POST"])
def getWaitCheckData():
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
    adminName = adminTable.admin_name
    sqlCountStr = "call getWorkBenchNum('{}',@waitCheckDataItemNum,@waitCheckDataNoticeNum,@waitCheckDataStatuteNum)".format(
        adminName)
    resualtList = sqlFunctionCall(sqlCountStr)
    if resualtList:
        waitCheckDataItemNum = resualtList[7]
        waitCheckDataNoticeNum = resualtList[8]
        waitCheckDataStatuteNum = resualtList[9]
        infoDict = {
            "waitCheckDataItemNum": waitCheckDataItemNum,
            "waitCheckDataNoticeNum": waitCheckDataNoticeNum,
            "waitCheckDataStatuteNum": waitCheckDataStatuteNum,
        }
    else:
        infoDict = dict(waitCheckDataItemNum=0, waitCheckDataNoticeNum=0,
                        waitCheckDataStatuteNum=0)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


"""new"""


# 爬虫维护员
@app.route("/getSpiderList", methods=["POST"])
@jwt_required
def getSpiderList():
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
    adminName = adminTable.admin_name
    sqlCountStr = "call getWorkBenchNum('{}',@waitCheckDataItemNum,@waitCheckDataNoticeNum,@waitCheckDataStatuteNum)".format(
        adminName)
    resualtList = sqlFunctionCall(sqlCountStr)
    if resualtList:
        waitCheckDataItemNum = resualtList[7]
        waitCheckDataNoticeNum = resualtList[8]
        waitCheckDataStatuteNum = resualtList[9]
        infoDict = {
            "waitCheckDataItemNum": waitCheckDataItemNum,
            "waitCheckDataNoticeNum": waitCheckDataNoticeNum,
            "waitCheckDataStatuteNum": waitCheckDataStatuteNum,
        }
    else:
        infoDict = dict(waitCheckDataItemNum=0, waitCheckDataNoticeNum=0,
                        waitCheckDataStatuteNum=0)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)


# 数据维护员
@app.route("/getDataMaintainList", methods=["POST"])
@jwt_required
def getDataMaintainList():
    adminId = get_jwt_identity()
    adminId = 11
    adminTable = findById(User, "admin_id", adminId)
    # adminTable = current_user
    adminName = adminTable.admin_name
    departRole = ["200201", "200202"]
    dataRole = ["200501", "200502", "200503"]
    sourceRole = ["200601", "200602"]
    roleInfo = getRole(dataRole,adminId)
    if roleInfo.get("code") == 0:
        return jsonify(roleInfo)
    sqlCountStr = "call getWorkBenchNum('{}',@waitCheckDataItemNum,@waitCheckDataNoticeNum,@waitCheckDataStatuteNum)".format(
        adminName)
    resualtList = sqlFunctionCall(sqlCountStr)
    if resualtList:
        waitCheckDataItemNum = resualtList[7]
        waitCheckDataNoticeNum = resualtList[8]
        waitCheckDataStatuteNum = resualtList[9]
        infoDict = {
            "waitCheckDataItemNum": waitCheckDataItemNum,
            "waitCheckDataNoticeNum": waitCheckDataNoticeNum,
            "waitCheckDataStatuteNum": waitCheckDataStatuteNum,
        }
    else:
        infoDict = dict(waitCheckDataItemNum=0, waitCheckDataNoticeNum=0,
                        waitCheckDataStatuteNum=0)
    resultDict = returnMsg(infoDict)
    return jsonify(resultDict)

def getRole(dataRole,adminId):
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