# -*- coding: utf-8 -*-
"""后台管理接口路由配置
时间: 2021/2/18 10:52

作者: Fengchunyang

Blog: https://www.fengchunyang.com

更改记录:
    2021/2/18 新增文件。

重要说明:
"""
from django.urls import path, include

from common import params
from . import views
from .system import urls as system_urls

urlpatterns = [
    path('dashboard/page', views.DashboardPageView.as_view(), name='dashboard-page'),
    path('dashboard/statistic/info', views.DashboardStatisticView.as_view(),
         name='dashboard-statistic'),  # 仪表板统计数据接口
    path('dashboard/statistic/access-chart', views.DashboardAccessChart.as_view(),
         name='dashboard-access-chart'),  # 仪表板访问数据统计接口
    path('dashboard/statistic/article-chart', views.DashboardArticleChart.as_view(),
         name='dashboard-article-chart'),  # 仪表板文章发表数据统计接口
    path('dashboard/statistic/process/data', views.DashboardProcessData.as_view(),
         name='dashboard-process-data'),  # 仪表板事件进度统计接口

    path('article/list/page', views.ArticleListPageView.as_view(), name='article-list-page'),
    path('article/data/page', views.ArticleDataPageView.as_view(), name='article-data-page'),
    path('article/data/classify/page', views.ArticleDataClassifyPageView.as_view(), name='article-data-classify-page'),
    path('article/data/tag/page', views.ArticleDataTagPageView.as_view(), name='article-data-tag-page'),
    path('article/data/serial/page', views.ArticleDataSerialPageView.as_view(), name='article-data-serial-page'),
    path('article/info/page', views.ArticleInfoPageView.as_view(), name='article-info-page'),

    path('article/list', views.ArticleListApiView.as_view(), name='article-list-api'),  # 文章列表接口
    path(f'article/info/<int:{params.MODEL_UNIQUE_KEY}>', views.ArticleInfoApiView.as_view(),
         name='article-info-api'),  # 文章详情接口
    path('article/data/classify/list', views.ArticleClassifyListApiView.as_view(),
         name='article-classify-list-api'),  # 文章分类列表接口
    path(f'article/data/classify/info/<int:{params.MODEL_UNIQUE_KEY}>', views.ArticleClassifyInfoApiView.as_view(),
         name='article-classify-info-api'),  # 文章分类详情接口
    path('article/data/tag/list', views.ArticleTagListApiView.as_view(), name='article-tag-list-api'),  # 文章标签列表接口
    path(f'article/data/tag/info/<int:{params.MODEL_UNIQUE_KEY}>', views.ArticleTagInfoApiView.as_view(),
         name='article-tag-info-api'),  # 文章标详情表接口
    path('article/data/serial/list', views.ArticleSerialListApiView.as_view(),
         name='article-serial-list-api'),  # 文章系列列表接口
    path(f'article/data/serial/info/<int:{params.MODEL_UNIQUE_KEY}>', views.ArticleSerialInfoApiView.as_view(),
         name='article-serial-info-api'),  # 文章标详情表接口

    path('system/', include(system_urls)),  # 系统配置路由入口
]
