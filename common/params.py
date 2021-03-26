# -*- coding: utf-8 -*-
"""全局常量配置
时间: 2020/11/23 11:10

作者: Fengchunyang

更改记录:
    2020/11/23 新增文件。

重要说明:
"""

# 日期格式相关
DATE_STANDARD = '%Y-%m-%d'
TIME_STANDARD = '%H:%M:%S'
DATETIME_STANDARD = f'{DATE_STANDARD} {TIME_STANDARD}'

# 前后端交互相关
JSON_CONTENT_TYPE = 'application/json'

# 匿名用户配置
ANONYMOUS_USER = 'anonymous'
ANONYMOUS_TOKEN = 'RK35hNaeqsB0nCTSptY4iMdQkou61b2IgfwxlHvzcX9AyrjmZPFLG7EWJ8UVDO'

# AES Salt
AES_SALT = "qBfLtQIbZfZgVJvTuTDMEq46tMinYpQX"

# Session setting
SESSION_KEY = 'authentication'
SESSION_TOKEN_KEY = 'token'
SESSION_USER_KEY = 'user'
RSA_SESSION_PRIVATE_KEY = 'RSA_PRIVATE_KEY'

# Model settings
MODEL_UNIQUE_KEY = 'pk'
LOGIN_EXPIRE_HOUR = 8

# 前端分页查询字符串
PAGINATE_PAGE = 'page'
PAGINATE_LIMIT = 'limit'

# 系统分隔符
SPLIT_COMMA = ','
SPLIT_DOT = '.'
SPLIT_DASH = '-'

# http常用响应数据
HTTP_SUCCESS = 'Success'
HTTP_Failed = 'Failed'

# 数据类型
DATA_TYPE_COMMON = 'common'



