#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 0017 09:30
# @Site    : 
# @File    : flowApi.py
# @Software: PyCharm
from flask import jsonify, json, request, url_for
from flask_jwt_extended import jwt_required, current_user

import Res
from common.DatatimeNow import getTimeStrfTimeStampNow
from common.FormatStr import dictRemoveNone
from common.OperationOfDB import conditionDataListFind, findById, deleteByIdBoss
from common.OperationOfDBClass import OperationOfDB
from common.ReturnMessage import returnMsg, returnErrorMsg, errorCode
from models.Boss.Role import Role
from models.Boss.User import User
from models.Data.Aidance import Aidance, AidanceChangeDic as tableChangeDic
from models.Data.AidanceCheck import AidanceCheck, AidanceCheckChangeDic
from models.Data.SingleService import SingleService, SingleServiceChangeDic
from models.Data.SubFlow import SubFlow
from models.Data.Transfer import Transfer
from models.Data.WholeService import WholeService, WholeServiceChangeDic
from version.v3.bossConfig import app
from common.FlowCommon import getFlowSort
