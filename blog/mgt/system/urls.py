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

from common.params import MODEL_UNIQUE_KEY

from . import views

urlpatterns = [
    path('seo/page', views.SeoPageView.as_view(), name='system-seo-page'),  # 文章链接页面
    path('access-record/page', views.AccessRecordPageView.as_view(), name='system-access-record-page'),  # 访问记录页面
    path('param/page', views.SystemParamPageView.as_view(), name='system-param-page'),  # 系统-参数页面
    path('flow/page', views.SystemFlowPageView.as_view(), name='system-flow-page'),  # 系统-项目流程页面
    path('project-info/add/page', views.ProjectInfoAddPageView.as_view(),
         name='system-project-info-add-page'),  # 系统-项目信息新增/编辑页面
    path('project-task/add/page', views.ProjectTaskAddPageView.as_view(),
         name='system-project-task-add-page'),  # 系统-项目任务新增/编辑页面

    path('seo/url-list', views.SeoUrlListView.as_view(), name='system-seo-url-list'),  # seo url列表接口
    path('project-info/list', views.ProjectInfoListView.as_view(), name='system-project-info-list'),  # 项目信息列表接口
    path(f'project-info/info/<int:{MODEL_UNIQUE_KEY}>', views.ProjectInfoInfoView.as_view(),
         name='system-project-info-info'),  # 项目信息详情接口
    path('project-task/list', views.ProjectTaskListView.as_view(), name='system-project-task-list'),  # 项目任务列表接口
    path(f'project-task/info/<int:{MODEL_UNIQUE_KEY}>', views.ProjectTaskInfoView.as_view(),
         name='system-project-task-info'),  # 项目任务详情接口

    path('access-record/list', views.AccessRecordListView.as_view(), name='access-record-list'),  # 访问记录列表接口
    path('article-push', views.ArticlePushApi.as_view(), name='article-push'),  # 文章推送接口
    path('flink/page', views.FlinkPageView.as_view(), name='flink-page'),  # 友链申请页面接口
    path('flink/list', views.FlinkListView.as_view(), name='flink-list'),  # 友链申请列表接口
    path(f'flink/info/<int:{MODEL_UNIQUE_KEY}>', views.FlinkInfoView.as_view(), name='flink-info'),  # 友链详情接口
]
