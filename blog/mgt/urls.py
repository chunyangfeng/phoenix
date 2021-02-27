# -*- coding: utf-8 -*-
"""后台管理接口路由配置
时间: 2021/2/18 10:52

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/18 新增文件。

重要说明:
"""
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/page', views.DashboardPageView.as_view(), name='dashboard-page'),
    path('article/list/page', views.ArticleListPageView.as_view(), name='article-list-page'),
    path('article/audit/page', views.ArticleAuditPageView.as_view(), name='article-audit-page'),

    path('article/list', views.ArticleListApiView.as_view(), name='article-list-api'),  # 文章列表接口
    path('article/info/<int:pk>', views.ArticleInfoApiView.as_view(), name='article-info-api'),  # 文章详情接口
]
