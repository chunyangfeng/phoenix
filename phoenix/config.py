# -*- coding: utf-8 -*-
"""全局配置文件
时间: 2021/3/4 13:11

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/4 新增文件。

重要说明:
"""

DEBUG = True

if DEBUG is True:
    # 系统设置
    ALLOWED_HOSTS = ['*']
    SYSTEM_DOMAIN = 'http://127.0.0.1:8888'
    BACKEND_DB = {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'USER': 'root',
        'PASSWORD': 'nishengri',
        'NAME': 'phoenix_test',
    }
else:
    ALLOWED_HOSTS = ['www.fengchunyang.com', '127.0.0.1']
    SYSTEM_DOMAIN = 'http://www.fengchunyang.com'
    BACKEND_DB = {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '192.168.1.103',
        'USER': 'root',
        'PASSWORD': 'nishengri',
        'NAME': 'phoenix_test',
    }
