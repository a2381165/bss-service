# coding:utf-8

# 网址路径
Dms_Url_Prefix = "/boss"

start = "start!"
host = "0.0.0.0"
port = 5002

serviceAgency = "四川省政资汇智能科技有限公司"
servicePerson = None

# 添加areaCode
addAreaCode = {
    "province": 1,
    "city": 2,
    "district": 3
}

# # 审核
# AuditCode = {
#     "send": 1,
#     "pass": 2,
#     "fail": 3
# }

# 咨询部 角色编号
# 咨询师
zxrole = {
    "zxs": 5,
    "zxbz": 2,  # 咨询部长
    "zxfbz": 3,  # 咨询副部长
    "swjl": 6,  # 商务经理
    "swfbz": 4  # 商务副部长
}
# 分派
zxWaitType = {
    "3": 3,  # 咨询副部长
}
# 审核
zxCheckType = {
    "3": 5,  # 咨询副部长
    "4": 1,  # 商务副部长
    "2": 2,  # 咨询部长
}

# 咨询 分配
zxFP = {
    "is_check": 1,  # 审核
    "is_pai": 2  # 分派
}

# 审核 1,2,5 | 分派 3

AcceptCode = {
    "not": 0,
    "wait": 1,
    "pass": 2,
    "fail": 3
}

# 分发
IsSend = {
    "wait": 1,
    "pass": 2,
    "reset": 3,
    "fail": 4
}

# 审核
AuditCode = {
    "send": 1,
    "pass": 2,
    "fail": 3
}

StatusCode = {
    "pass": 1,
    "fail": 2
}

# 派单
AssignCode = {
    "pass": 1,
    "reset": 2,
    "fail": 3
}

# 是否关闭订单
IsClose = {
    "close": 1,
    "reset": 2
}

# 合同
HTType = {
    "member": 1,
    "counselor": 2
}

# 咨询师类型
counselorType = {
    "person": 1,
    "enterprise": 2
}
# taskType
taskType = {
    "wtDx": 1,  # 委托 单项
    "wtZt": 2,  # 委托 总体
    "zxFW": 3,  # 咨询 服务审核
}

# 工作流程
"""
1	单项服务方案
2	总体服务方案
3	咨询副部长审批
4	预约订单分发
5	合同流程
6	订单分发
7	政策协助
8	技术协助
9	合同协助
10	渠道商流程
11  项目结算审核
"""
workFlow = {
    "wtDx": 1,  # 单项服务方案
    "wtZt": 2,  # 总体服务方案
    "zxFW": 3,  # 咨询副部长审批
    "yyddff": 4,  # 预约订单分发
    "htlc": 5,  # 合同流程
    "ddff": 6,  # 订单分发
    "zcxz": 7,  # 政策协助
    "jsxz": 8,  # 技术协助
    "htxz": 9,  # 合同协助
    "qdslc": 10,  # 渠道商流程
    "xmjssh": 11,  # 项目结算审核
}

roleDict = {
    6: "swjl",  # 商务经理
    4: "swfbz",  # 商务副部长
    2: "zxbz",  # 咨询部长
    3: "zxfbz",  # 咨询副部长
    5: "zxs",  # 咨询师
}

# 方案服务 工作流 角色对应 单项 总体
roleSort = {
    "swjl": 1,  # 商务经理
    "swfbz": 1,  # 商务副部长
    "zxbz": 2,  # 咨询部长
    "zxfbz": 3,  # 咨询副部长
    "zxs": 4,  # 咨询师
}

# 方案服务 工作流 角色对应 咨询审核
roleSortCheck = {
    "zxfbz": 1,
}

projectType = {
    "ktgt": 1,  # 开拓沟通
    "zlfwfa": 2,  # 战略服务方案
    "dxfwfa": 3,  # 单项服务方案
    "zlht": 4,  # 战略合同
    "dxht": 5,  # 单项合同
    "dxlxgt": 6,  # 单项立项沟通
    "dxjs": 7  # 单向结算
}

roleId = {
    "zxfbz": {"3": [1, 2, 3]},
    "swfbz": {"4": [4, 5, 6]},
    "zxbz": {"2": [3, 6]}
}

all_role = {
    "admin": "1",  # "超级管理员",
    "zxbbz": "2",  # "咨询部长",
    "zxfbz": "3",  # "咨询副部长",
    "swfbz": "4",  # "商务副部长",
    "zxs": "5",  # "咨询师",
    "swjl": "6",  # "商务经理",
    "ntjl": "7",  # "内拓经理",
    "jsbbz": "8",  # "技术部部长",
    "pcwhy": "9",  # "爬虫维护员",
    "sjwhy": "10",  # "数据维护员",
    "sjshy": "11",  # "数据审核员",
    "tgbz": "12",  # "推广部部长",
    "tgzy": "13",  # "推广专员",
    "zhbbz": "14",  # "综合部部长",
    "xzzy": "15",  # "行政专员",
    "zjl": "16",  # "总经理",
    "ggjl": "17",  # "公关经理",
}
