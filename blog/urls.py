# -*- coding: utf-8 -*-
"""blog路由配置
时间: 2021/2/18 10:52

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/18 新增文件。

重要说明:
"""
from django.urls import path, include

from .mgt import urls as mgt_urls

urlpatterns = [
    path('mgt/', include(mgt_urls)),
]