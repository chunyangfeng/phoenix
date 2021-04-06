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

from common import params

from . import views

urlpatterns = [
    path(f'article/<int:{params.MODEL_UNIQUE_KEY}>', views.ArticleDetailPageView.as_view(), name='article-detail-page'),
    path('map', views.IndexSiteMapPageView.as_view(), name='site-map-page'),
    path('article/list', views.IndexArticleListView.as_view(), name='index-article-list'),
    path('show-card/info', views.IndexShowCardInfoView.as_view(), name='index-show-card-info'),
    path('visitor/info/page', views.IndexVisitorInfoPageView.as_view(), name='index-visitor-info-page'),
    path('visitor/message/list', views.IndexVisitorMessageListView.as_view(), name='index-visitor-message-list'),
]
