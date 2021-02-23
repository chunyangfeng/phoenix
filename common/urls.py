# -*- coding: utf-8 -*-
"""通用架构路由配置
Date: 2021/1/27 14:53

Author: phoenix@fengchunyang.com

Record:
    2021/1/27 新增文件。

Site: http://www.fengchunyang.com
"""
from django.urls import path

from common import views

urlpatterns = [
    path('login/page', views.UserLoginPageView.as_view(), name='login_page'),  # 用户登录页面
    path('login', views.UserLoginView.as_view(), name='login'),  # 用户登录
    path('public-key', views.AuthPublicKeyView.as_view(), name='pubkey'),  # 获取加密公钥
]
