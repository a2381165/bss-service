# coding:utf-8
from common.OperationOfDB import executeSql
import Res


def getAreaSql(adminId, roleId, areaCode=None):
    if not areaCode:
        if roleId:
            if str(roleId) == Res.all_role["zxbbz"]:
                areaCodeSql = "select area_code from data_area where  data_area.area_status = 1"
            else:
                areaCodeSql = "SELECT t1.area_code FROM data_area as t1 JOIN boss_area_set as t2 join boss_role as t3 ON t1.area_status=1 and t2.user_id={} and  t1.area_code = t2.area_code and t3.role_id={} and t2.oz_id=t3.oz_id;".format(
                    adminId, roleId)
            areaCodeList = []
            areaList = executeSql(areaCodeSql)
            for area in areaList:
                areaCodeList.append(str(area[0]))
            _areaList = []
            _arealike = []
            for areaCode in areaCodeList:
                if areaCode[2:] == "0000":
                    _areaList.append(areaCode)
                else:
                    _arealike.append(areaCode)
            if _areaList:
                if len(_areaList) == 1:
                    sqlStr = " and (area_code in {} ".format(str(tuple(_areaList)).replace(",", ""))
                else:
                    sqlStr = " and (area_code in {} ".format(tuple(_areaList))
            else:
                sqlStr = " and ( "
            if _arealike:
                if len(_arealike) == 1:
                    if sqlStr == " and ( ":
                        sqlStr += " left(area_code,4) in {} ".format(str(tuple([_arealike[0][:4]])).replace(",", ""))
                    else:
                        sqlStr += " or left(area_code,4) in {} ".format(str(tuple([_arealike[0][:4]])).replace(",", ""))
                else:
                    if sqlStr == " and ( ":
                        sqlStr += " left(area_code,4) in {} ".format(tuple([_area[:4] for _area in _arealike]))
                    else:
                        sqlStr += " or left(area_code,4) in {} ".format(tuple([_area[:4] for _area in _arealike]))
            sqlStr += " ) "
        else:
            return None
    else:
        if areaCode[2:] == "0000":
            sqlStr = " and area_code = {}".format(areaCode)
        else:
            sqlStr = " and left(area_code,4) = '{}'".format(areaCode[:4])
    if sqlStr == " and (  ) ":
        return None
    return sqlStr
