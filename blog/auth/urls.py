# -*- coding: utf-8 -*-
"""认证授权路由层
时间: 2021/3/26 9:37

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/26 新增文件。

重要说明:
"""
from django.urls import path

from . import views

urlpatterns = [
    path('login/page', views.UserLoginPageView.as_view(), name='login_page'),  # 用户登录页面
    path('login', views.UserLoginView.as_view(), name='login'),  # 用户登录
    path('public-key', views.AuthPublicKeyView.as_view(), name='pubkey'),  # 获取RSA公钥
    path('logout', views.LogoutView.as_view(), name='logout'),  # 退出登录
]
