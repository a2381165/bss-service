# coding:utf-8
import random

from common.DatatimeNow import getTimeStampNow
from models.Order.UserOrder import UserOrder


def addDeclareStatus(orderNo, dbOperation, declareStatus):
    orderTable = UserOrder.query.filter(UserOrder.order_no == orderNo).first()
    # if "2" in declareStatus:
    #     orderTable.order_status = 1
    orderTable.declare_status = declareStatus
    table = dbOperation.addTokenToSql(orderTable)
    return table


# 创建服务Code
def createServiceNo(orderNo):
    """订单号+6位随机数+时间戳后四位（4位）"""

    tiemStamp = str(getTimeStampNow().date()).replace("-", "")
    tiemStamp = tiemStamp[4:]
    intCode = getRandomIntCode(6)
    if orderNo:
        return orderNo + tiemStamp + intCode
    else:
        return None


# 生成长度为codeLen的随机数字字符串
def getRandomIntCode(codeLen):
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    myslice = random.sample(code_list, codeLen)
    intCodeStr = "".join(myslice)
    return intCodeStr
