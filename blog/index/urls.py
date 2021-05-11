# -*- coding: utf-8 -*-
"""后台管理接口路由配置
时间: 2021/2/18 10:52

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/18 新增文件。

重要说明:
"""
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import GenericSitemap
from django.urls import path

from blog.models import Article
from common import params

from . import views

info_dict = {
    "queryset": Article.objects.filter(is_publish=True),
    "date_field": 'ctime',
}

urlpatterns = [
    path(f'article/<int:{params.MODEL_UNIQUE_KEY}>', views.ArticleDetailPageView.as_view(), name='article-detail-page'),
    # path('map', views.IndexSiteMapPageView.as_view(), name='site-map-page'),
    path('map', sitemap, {"sitemaps": {'article': GenericSitemap(info_dict, priority=0.6)}},
         name='django.contrib.sitemaps.views.sitemap'),
    path('article/list', views.IndexArticleListView.as_view(), name='index-article-list'),
    path('show-card/info', views.IndexShowCardInfoView.as_view(), name='index-show-card-info'),
    path('visitor/info/page', views.IndexVisitorInfoPageView.as_view(), name='index-visitor-info-page'),
    path('visitor/message/list', views.IndexVisitorMessageListView.as_view(), name='index-visitor-message-list'),
    path('visitor/subscribe/list', views.IndexVisitorScribeListView.as_view(), name='index-visitor-scribe-list'),
    path('hot-article/info', views.IndexHotArticleInfoView.as_view(), name='index-hot-article-info'),
]
