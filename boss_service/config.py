# coding:utf-8
from flask import Flask
from flask_mail import Mail
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import datetime
import logging
import logging.config
from common.createDemo import CreateApi
from common.createModels import Models
# from flask_caching import Cache
from common.FormatStr import JSONEncoder

# from gevent import monkey
# monkey.patch_all()

app = Flask(__name__)
# cache = Cache(app, config={'CACHE_TYPE': 'simple'})
CORS(app)
# Debug
# app.debug = True
app.json_encoder = JSONEncoder
# 爬虫项目路径
PROJECTS_FOLDER = "/root/boss-service/projects"
# PROJECTS_FOLDER = "F://boss-service\projects"
app.config['UPLOAD_FOLDER'] = PROJECTS_FOLDER
# 爬虫脚本存放redis
redisHost = "192.168.5.127"
redisPort = 6381
redisDb = 0
# 定时任务
redisTaskDb = 2

# other way of coinfig app.config.from_object('test')

# db config
# 内网服务器mysql地址
localConfig = 'mysql://root:root#1234@192.168.5.125:3306/zzh_boss'
# 外网服务器mysql地址
# localConfig = 'mysql://root:root#1234@121.40.183.170:3306/zzh'
# 本地服务器mysql地址
# localConfig = 'mysql://zzh:123456@127.0.0.1:3306/zzh'
app.config['SQLALCHEMY_DATABASE_URI'] = localConfig
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 外网服务器mysql地址
# app.config["SQLALCHEMY_BINDS"] = {'crawler':'mysql://root:root#url@121.40.183.170:3304/url',}
# 内网服务器mysql地址
app.config["SQLALCHEMY_BINDS"] = {'crawler': 'mysql://root:root#url@192.168.5.125:3304/ww_url', }
# 本地服务器mysql地址
# app.config["SQLALCHEMY_BINDS"] = {'crawler':'mysql://zzh:123456@127.0.0.1:3306/url',}
db = SQLAlchemy(app)

# 文本编辑器配置
app.config["static_folder"] = "static"

# app config
# delta = datetime.timedelta(seconds=2)
delta = datetime.timedelta(hours=4)
refresh_delta = datetime.timedelta(days=30)
# add by tyf 2017-7-31
app.config['JWT_IDENTITY_CLAIM'] = "identity"
app.config['JWT_TOKEN_LOCATION'] = ["headers"]
app.config['JWT_HEADER_NAME'] = "zzhToken"
app.config['JWT_HEADER_TYPE'] = "Basic"
app.config['JWT_AUTH_URL_RULE'] = "/login"
app.config['JWT_ALGORITHM'] = "HS256"
app.config['JWT_SECRET_KEY'] = "aaa"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = delta
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = refresh_delta
jwt = JWTManager(app)
runmodel = Models(db, dbname="zzh_boss")
craeteapi = CreateApi(db, dbname="zzh_boss")

logging.config.fileConfig("log.conf")
logger = logging.getLogger("cse")

# 邮件配置
app.config['MAIL_SERVER'] = "smtp.exmail.qq.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = "admin@zhengzihui.com"
app.config['MAIL_PASSWORD'] = "Zzh2017"
app.config['MAIL_DEBUG'] = True
mail = Mail(app)
