# -*- coding: utf-8 -*-
'''
修改文件名为local_demo.py，然后作为本地开发配置
'''
from config.base_setting import *

DATABASE = "home"
DATABASE_TYPE = "sqlite"
# DATABASE_CONF = {
#     'host': '127.0.0.1',
#     'port': 3306,
#     'user': 'root',
#     'passwd': '123456',
#     'charset': 'utf8mb4',
# }
SQLITE_DB="home.db"
SQLITE_CONF={
    'journal_mode': 'wal',
    'cache_size': 10000,  # 10000 pages, or ~40MB
    'foreign_keys': 1,  # Enforce foreign-key constraints
}