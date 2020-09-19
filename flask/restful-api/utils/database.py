#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()      # 创建SQLAlchemy engine 在后面进行绑定到App，与进行数据库初始化操作