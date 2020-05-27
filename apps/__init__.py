# -*- coding: utf-8 -*-
'''
专门为web程序准备的初始化入口
'''
from app import app

'''
toolbar
'''


# toolbar = DebugToolbarExtension(app)

'''
统一拦截处理和统一错误处理
'''

'''
蓝图功能，对所有的url进行蓝图功能配置
'''
from interceptors.MIDDLEWARE import *
from apps.urls import route_index,route_api


MODULES = (
    (route_index, '/'),
    (route_api, '/api'),

)


def setting_modules(app, modules):
    """ 注册Blueprint模块 """
    for module, url_prefix in modules:
        app.register_blueprint(module, url_prefix=url_prefix)


setting_modules(app, MODULES)
