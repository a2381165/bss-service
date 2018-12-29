#! /usr/bin/env python
#-*-coding:utf-8 -*-

import glob
import os
import time
import shutil
import sys
import tempfile
import redis
import json
import logging
from os.path import join
from subprocess import check_call

import configparser
from common.FormatStr import dictRemoveNone
from apscheduler.schedulers.background import BackgroundScheduler
from scrapy.utils.python import retry_on_eintr
from common.OperationOfDB import executeTheSQLStatement
from models.Boss.Area import Area as DataArea, tableChangeDic
from models.Boss.SpiderScriptNode import SpiderScriptNode, tableChangeDic
from models.Boss.SpiderSchedule import SpiderSchedule,tableChangeDic
from models.Boss.SpiderScript import SpiderScript, tableChangeDic
from models.Boss.SpiderScriptSchedule import SpiderScriptSchedule, tableChangeDic
from models.Boss.SpiderSchedule import SpiderSchedule
from config import PROJECTS_FOLDER,redisHost,redisPort,redisTaskDb
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler


jobstores = {
    'redis': RedisJobStore(host=redisHost,port=redisPort,db=redisTaskDb)
}
executors = {
    'default': ThreadPoolExecutor(10),#默认线程数
    'processpool': ProcessPoolExecutor(3)#默认进程
}

schedul = BackgroundScheduler(jobstores=jobstores, executors=executors)


def scrapyd_url(ip, port):
    """
    get scrapyd url
    :param ip: host
    :param port: port
    :return: string
    """
    url = 'http://{ip}:{port}'.format(ip=ip, port=port)
    return url


def log_url(ip, port, project, spider, job):
    """
    get log url
    :param ip: host
    :param port: port
    :param project: project
    :param spider: spider
    :param job: job
    :return: string
    """
    url = 'http://{ip}:{port}/logs/{project}/{spider}/{job}.log'.format(ip=ip, port=port, project=project,
                                                                        spider=spider, job=job)
    return url



def config(path, section, option, name='scrapy.cfg', default=None):
    try:
        cf = configparser.ConfigParser()
        cfg_path = join(path, name)
        cf.read(cfg_path)
        return cf.get(section, option)
    except configparser.NoOptionError:
        return default


def build_project(project):
    egg = build_egg(project)
    print('Built %(project)s into %(egg)s' % {'egg': egg, 'project': project})
    return egg


_SETUP_PY_TEMPLATE = \
    """# Automatically created by: gerapy
from setuptools import setup, find_packages
setup(
    name='%(project)s',
    version='1.0',
    packages=find_packages(),
    entry_points={'scrapy':['settings=%(settings)s']},
)"""



# 构建Egg
def build_egg(project):
    work_path = os.getcwd()
    try:
        path = os.path.abspath(join(os.getcwd(), PROJECTS_FOLDER))
        project_path = join(path, project)
        os.chdir(project_path)
        settings = config(project_path, 'settings', 'default')
        create_default_setup_py(project_path, settings=settings, project=project)
        d = tempfile.mkdtemp(prefix="zzh-")
        o = open(os.path.join(d, "stdout"), "wb")
        e = open(os.path.join(d, "stderr"), "wb")
        retry_on_eintr(check_call, [sys.executable, 'setup.py', 'clean', '-a', 'bdist_egg', '-d', d],
                       stdout=o, stderr=e)
        o.close()
        e.close()
        egg = glob.glob(os.path.join(d, '*.egg'))[0]
        # Delete Origin file
        if find_egg(project_path):
            os.remove(join(project_path, find_egg(project_path)))
        shutil.move(egg, project_path)
        return join(project_path, find_egg(project_path))
    except Exception as e:
        print(e.args)
    finally:
        os.chdir(work_path)


def find_egg(path):
    items = os.listdir(path)
    for name in items:
        if name.endswith(".egg"):
            return name
    return None


def create_default_setup_py(path, **kwargs):
    with open(join(path, 'setup.py'), 'w') as f:
        print(kwargs)
        file = _SETUP_PY_TEMPLATE % kwargs
        f.write(file)
        f.close()


