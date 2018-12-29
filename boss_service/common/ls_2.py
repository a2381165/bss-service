#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/11 0011 16:50
# @Site    : 
# @File    : ls_2.py
# @Software: PyCharm

import pdfkit,os
path_wkthmltopdf = r'C:\Users\Administrator\Downloads\wkhtmltox-0.12.5-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
# pdfkit.from_url('http://192.168.5.21/lookBusinessDetail.html?id=53', 'out.pdf', configuration=config)
cwdPath = os.getcwd()
serviceId =28
urlPath = cwdPath + r"/static/tempcontract/temp"
contractPath = os.path.join(urlPath, "single{}.pdf".format(serviceId))
print contractPath
# contractPath = r"E:\dfk\zzh\bss-service\boss_service\static\tempcontract\temp\single.pdf"
# pdfkit.from_url('http://192.168.5.21/lookBusinessDetail.html?id={}'.format(serviceId), contractPath,configuration=config)