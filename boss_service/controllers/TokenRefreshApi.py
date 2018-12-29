# -*- coding: utf-8 -*-
from flask import jsonify
from flask_jwt_extended import create_access_token, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt, get_jti

from common.Log import updateLog
from common.OperationOfDB import addTokenToSql
from common.ReturnMessage import returnMsg, returnErrorMsg
from models.Boss.User import User
from version.v3.bossConfig import app


# token刷新
@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
@updateLog("boss_user")
def refresh():
    adminId = get_jwt_identity()
    if adminId == None:
        resultInfo = {}
        resultDict = returnErrorMsg(resultInfo)
    else:
        adminTable = User.query.filter(User.admin_id == adminId).first()
        if adminTable:
            postJwt = get_raw_jwt()
            postJti = postJwt.get("jti")
            refreshJti = adminTable.admin_refresh_token
            if postJti == refreshJti:
                accessToken = create_access_token(identity=adminId)
                accessTokenJti = get_jti(accessToken)
                adminTable.admin_token = accessTokenJti
                addTokenToSql(adminTable)
                dictInfo = {
                    "accessToken": accessToken
                }
                resultDict = returnMsg(dictInfo)
            else:
                resultDict = returnErrorMsg("this refresh token not match with sql!")
        else:
            resultDict = returnErrorMsg("the adminId not exit!")
    return jsonify(resultDict)
