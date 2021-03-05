# -*- coding: utf-8 -*-
"""系统配置路由入口
时间: 2021/3/4 15:32

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/4 新增文件。

重要说明:
"""
from django.urls import path

from . import views

urlpatterns = [
    path('seo/page', views.SeoPageView.as_view(), name='system-seo-page'),  # seo管理页面
    path('param/page', views.SystemParamPageView.as_view(), name='system-param-page'),  # 系统参数页面

    path('seo/url-list', views.SeoUrlListView.as_view(), name='system-seo-url-list'),  # seo url列表接口
]
