# -*- coding: utf-8 -*-
import types
from functools import wraps

from flask import jsonify
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt

from common.ReturnMessage import returnErrorMsg, errorCode
from config import jwt
from config import jwt as jwt_admin
from models.Boss.User import User


# 访问受保护端口 会调用此函数
@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    adminTable = User.query.filter(User.admin_id == identity).first()
    postJwt = get_raw_jwt()
    postCounselorToken = postJwt.get("jti")
    if adminTable:
        userToken = adminTable.admin_token
        refreshToken = adminTable.admin_refresh_token
        if userToken == postCounselorToken or refreshToken == postCounselorToken:
            return adminTable
        else:
            return None
    else:
        return None


# 认证失败 自动调用此函数
@jwt.user_loader_error_loader
def custom_user_loader_error(identity):
    # ret = {
    #     "msg": "User {} not found".format(identity)
    # }
    resultDict = returnErrorMsg(errorCode["unauthorized"])
    return jsonify(resultDict), 401


def admin_require(fn):
    @jwt_required
    @wraps(fn)
    def _deco():
        if type(request.json) != types.DictType:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        adminId = get_jwt_identity()
        if not adminId:
            resultDict = returnErrorMsg(errorCode["param_error"])
            return jsonify(resultDict)
        adminTable = User.query.filter(User.admin_id == adminId).first()
        postJwt = get_raw_jwt()
        postAdminToken = postJwt.get("jti")
        if adminTable:
            adminToken = adminTable.admin_token
            if adminToken == postAdminToken:
                return fn()
            else:
                resultDict = returnErrorMsg(errorCode["token_not_mach"])
        else:
            resultDict = returnErrorMsg(errorCode["admin_not_exit"])
        return jsonify(resultDict)

    return _deco


@jwt_admin.invalid_token_loader  # 无效令牌控制
@jwt_admin.unauthorized_loader  # 当没有JWT的请求访问受保护端点时调用的函数
def my_unauthorized_loader(identy):
    dictInfo = "The has no token: %s" % identy
    resultDict = returnErrorMsg(dictInfo)
    return jsonify(resultDict), 401


@jwt_admin.expired_token_loader  # 过期token处理
def my_expired_token_callback():
    returnInfo = returnErrorMsg(errorCode["token_expired"])
    return jsonify(returnInfo),200
