#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/25 0025 16:45
# @Site    : 
# @File    : CreatePdf.py
# @Software: PyCharm



import pdfkit, os


def createWholePdf(serviceId):
    try:
        try:
            path_wkthmltopdf = r'C:\Users\Administrator\Downloads\wkhtmltox-0.12.5-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        except:
            config = None
        cwdPath = os.getcwd()
        urlPath = cwdPath + "/static/tempservice/temp"
        if not os.path.exists(urlPath):
            os.makedirs(urlPath)
        contractPath = os.path.join(urlPath, "whole{}.pdf".format(serviceId))
        if pdfkit.from_url('http://192.168.5.21/lookAllBusinessDetail.html?id={}&printTable=1'.format(serviceId),
                           contractPath,
                           configuration=config):
            return "tempservice/temp/whole{}.pdf".format(serviceId)
        else:
            return None
    except Exception as e:
        print e
        return None


def createSinglePdf(serviceId):
    try:
        try:
            path_wkthmltopdf = r'C:\Users\Administrator\Downloads\wkhtmltox-0.12.5-1.mxe-cross-win64\wkhtmltox\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
        except:
            config=None
        cwdPath = os.getcwd()
        urlPath = cwdPath + "/static/tempservice/temp"
        if not os.path.exists(urlPath):
            os.makedirs(urlPath)
        contractPath = os.path.join(urlPath, "single{}.pdf".format(serviceId))
        if pdfkit.from_url('http://192.168.5.21/lookBusinessDetail.html?id={}&printTable=1'.format(serviceId),
                           contractPath,
                           configuration=config):
            return "tempservice/temp/single{}.pdf".format(serviceId)
        else:
            return None
    except Exception as e:
        print e
        return None
