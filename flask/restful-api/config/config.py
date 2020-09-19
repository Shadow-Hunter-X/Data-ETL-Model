#!/usr/bin/python
# -*- coding: utf-8 -*-

#-----------------------------------------------------------
# 只有大写的配置信息才会被识别
# In both cases (loading from any Python file or loading from modules), only uppercase keys are added to the config
# two common patterns to populate the config:
# 1- app.config.from_pyfile('yourconfig.cfg')  fill the config from a config file 
# 2- app.config.from_object(__name__)  calls from_object() or provide an import path to a module that should be loaded

# Flask中的默认配置：
#    'DEBUG': False,  # 是否开启Debug模式 如果代码有修改随时自动重启
#    'TESTING': False,  # 是否开启测试模式
#    'PROPAGATE_EXCEPTIONS': None,  # 异常传播(是否在控制台打印LOG) 当Debug或者testing开启后,自动为True

# 具体常看官方的配置变量的说明： https://flask.palletsprojects.com/en/1.1.x/config/  
#-----------------------------------------------------------

class Config(object):
    DEBUG = True        # 是否开启Debug模式
    TESTING = False     # 是否开启测试模式
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# 生产配置
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:iamneo@127.0.0.1:3306/test'      #mysql-使用pymysql作为驱动
    SQLALCHEMY_ECHO = False     # 生产环境设置为FALSE，log all the statements issued to stderr which can be useful for debugging
    JWT_SECRET_KEY = 'JWT_SECRET_KEY'       # 用于JWT的加密秘钥
    SECRET_KEY = 'SECRET_KEY'   # Flask应用使用的加密秘钥
    SECRET_PASSWORD_SALT = 'SECRET_PASSWORD_SALT'  # Specifies the HMAC salt,这只在密码散列类型被设置为非纯文本时使用

# 开发环境配置
class DevelopmentConfig(Config):
    DEBUG = True 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\test.db' 
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECRET_KEY= 'SECRET-KEY'
    SECURITY_PASSWORD_SALT= 'SECRET-KEY-PASSWORD'

# 测试环境配置
class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///D:\\test.db' 
    SQLALCHEMY_ECHO = False
    JWT_SECRET_KEY = 'JWT-SECRET'
    SECRET_KEY= 'SECRET-KEY'
    SECURITY_PASSWORD_SALT= 'SECRET-KEY-PASSWORD'

	