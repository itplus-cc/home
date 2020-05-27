# -*- coding: utf-8 -*-
'''
修改文件名为local_demo.py，然后作为本地开发配置
'''
from config.base_setting import *

DATABASE = "home"
DATABASE_CONF = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'passwd': '123456',
    'charset': 'utf8mb4',
}