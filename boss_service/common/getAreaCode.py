#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 0017 15:29
# @Site    : 
# @File    : getAreaCode.py
# @Software: PyCharm
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 0017 15:26
# @Site    :
# @File    : common.py
# @Software: PyCharm
from models.Base.Area import Area


def getAreaCode(areaCode):
    provinceName = ""
    cityName = ""
    districtName = ""
    try:
        areaCode = areaCode
        if areaCode:
            if areaCode[:2] != "00":
                newAreaCode = "{}0000".format(areaCode[:2])
                areaCodetable = Area.query.filter(Area.area_code == newAreaCode).first()
                if areaCodetable:
                    provinceName = areaCodetable.area_name
            if areaCode[2:4] != "00":
                newAreaCode = "{}00".format(areaCode[:4])
                areaCodetable = Area.query.filter(Area.area_code == newAreaCode).first()
                if areaCodetable:
                    cityName = areaCodetable.area_name
            if areaCode[4:6] != "00":
                newAreaCode = "{}".format(areaCode)
                areaCodetable = Area.query.filter(Area.area_code == newAreaCode).first()
                if areaCodetable:
                    districtName = areaCodetable.area_name
        return provinceName, cityName, districtName
    except:
        return provinceName, cityName, districtName
