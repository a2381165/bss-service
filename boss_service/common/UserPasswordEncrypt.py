# -*- coding: utf-8 -*-

import hashlib
import types
import random

class PasswordSort():
    def __init__(self):
        pass

    def passwordEncrypt(self, passwordStr):
        try:
            encryptStr = str(passwordStr + "zzh")
            m = hashlib.md5()
            m.update(encryptStr)
            passwordEncryptStr = m.hexdigest()
            return passwordEncryptStr
        except:
            return ""

    def passwordEncryptSlat(self, passwordStr, Slat):
        try:
            encryptStr = str(passwordStr + Slat)
            m = hashlib.md5()
            m.update(encryptStr)
            passwordEncryptStr = m.hexdigest()
            return passwordEncryptStr
        except:
            return ""

def make_appKey(name):
    try:
        encryptStr = str(name + "zzh")
        m = hashlib.md5()
        m.update(encryptStr)
        passwordEncryptStr = m.hexdigest()
        return passwordEncryptStr
    except:
        return ""


def make_appsecret(name):
    try:
        encryptStr = str(name + "secret")
        m = hashlib.md5()
        m.update(encryptStr)
        passwordEncryptStr = m.hexdigest()
        return passwordEncryptStr
    except:
        return ""
# 生成随机码，长度为codeLen的大小写字母和数组混合的随机字符串
def codeCreate(codeLen):
    code_list = []
    for i in range(10):
        code_list.append(str(i))
    for i in range(65, 91):
        code_list.append(chr(i))
    for i in range(97, 123):
        code_list.append(chr(i))
    myslice = random.sample(code_list, codeLen)
    verification_code = "".join(myslice)
    return verification_code
#
# print make_appKey("高新科服")
# print make_appsecret("高新科服")