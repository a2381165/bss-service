# -*- coding: utf-8 -*-

Code_Str = "code"
Status_Str = "status"
Error_Str = "error"
Info_Str = "info"
Message_Str = "message"
Success_Str = "success"
No_Data = "no data"

errorCode = {
    "no_data": "成功请求",
    "exception_request": "异常请求",
    "invalid_appkey": "无效Appkey",
    "server_exception": "服务过期",
    "param_error": "参数错误",
    "invalid_itemId": "无效项目编号",
    "invalid_orderNo": "无效订单号",
    "invalid_uid": "无效用户uid",
    "order_repeat": "订单不能重复创建",
    "order_full": "订单数量已满",
    "not_find": "无效接口请求",
    "incomplete_information": "用户信息不完整",
    "not_opened": "区域未开通",
    "deadline_itemId": "项目截止",
    "fail": "服务器异常!",
    "area_error": "区域码不正确",
    "code_expire": "验证码过期",
    "verify_code": "验证失败",
    "json_error": "json格式错误",
    "phone_use": "手机号已被使用",
    "email_use": "邮箱账号已被使用",
    "no_user": "用户不存在",
    "token_expire": "token 已过期",
    "oz_people": "此部门还有人员",
    "oz_oz": "此部门还有子部门",
    "menu_menu": "此菜单还有子菜单",
    "role_role": "此角色还有子角色",
    "role_people": "此角色还有人员,请去取消！",
    "area_code_exist": "区域code已经存在，请直接修改！",
    "area_code_no_matching": "区域不匹配当前省市区！",
    "area_set_people": "此区域还有维护人员！",
    "dept_item_has_son": "此项目维护中还有子类！",
    "param_enough": "参数不全",
    "tempItem_not_content": "通知内容未添加",
    "role_sys": "系统保留",
    "role_check_delete_add": "角色申请重复",
    "serviceAttach_delete": "删除失败，无法删除别人的附件！",
    "serviceAttach_updata": "更新失败，无法更新别人的附件！",
    "system_error":"系统异常",
    "unauthorized":"未经授权：访问由于凭据无效被拒绝。",
    "token_not_mach":"the token not mach with sql!",
    "admin_not_exit":"this admin not exit!",
    "token_expired":"the token expired!",
    "update_fail":"更新失败!查看参数是否正确!",
    "insert_fail":"插入失败!查看参数是否正确!",
    "commit_fail":"提交失败!查看参数是否正确!",
    "query_fail":"查询失败!查看参数是否正确!",
    "delete_fail":"删除失败!查看参数是否正确!",
    "delete_only_own":"只能删除自己创建的",
    "has_son":"还有子项没有删除!",
    "phone_args_fail":"请输入正确的手机号码！",
    "upload_only_excel":"请上传excel!",
    "not_remark":"请填写备注！",
    "email_fail":"请填写正确的邮箱！",
    "whole_single_service_not_del":"委托项目无法删除！",
    "rate_not_100":"提成比例不能超过100%！"
}


# 请求报错
def returnErrorMsg(CodeStr=None):
    if CodeStr:
        resultDict = {Message_Str: {"code": 0, "msg": CodeStr}}
    else:
        resultDict = {Message_Str: {"code": 0, "msg": "服务器异常!"}}
    return resultDict


# 请求成功，有数据
def returnMsg(dataDict):
    resultDict = {Info_Str: dataDict, Message_Str: {Code_Str: 1, Status_Str: Success_Str}}
    return resultDict


# # 请求成功，无数据
# def returnNoneMsg(dataDict):
#     resultDict = {Info_Str: dataDict, Message_Str: {Code_Str: 0, Status_Str: No_Data}}
#     return resultDict


# def returnCodeMsg(CodeStr):
#     if CodeStr:
#         resultDict = {Message_Str: CodeStr}
#     else:
#         resultDict = {Message_Str: {"code": "10015", "msg": "服务器异常!"}}
#     return resultDict


# def returnErrorMsg(CodeStr):
#     resultDict = {Message_Str: {"code": 0, "msg": CodeStr}}
#     return resultDict
