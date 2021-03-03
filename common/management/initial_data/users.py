# -*- coding: utf-8 -*-
"""内置用户配置
时间: 2021/2/22 16:33

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/22 新增文件。

重要说明:
"""


BUILTIN_USER = {
    "admin": {
        'real_name': 'administrator',
        'password': '123456',
        'email': 'admin@fengchunyang.com',
        'site': 'http://www.fengchunyang.com',
        'is_builtin': True
    },
    "anonymous": {
        'real_name': 'anonymous',
        'password': '123456',
        'email': 'anonymous@fengchunyang.com',
        'site': 'http://www.fengchunyang.com',
        'is_builtin': True
    },
}
