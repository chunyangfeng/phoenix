"""评论模块路由

Author: Fengchunyang

Site: https://www.fengchunyang.com

Date: 2021/5/11 11:03

Desc:
    2021/5/11 11:03 add file.
"""
from django.urls import path

from common import params
from . import views

urlpatterns = [
    path('article-comment/list', views.ArticleCommentListView.as_view(), name='article-comment-list'),  # 文章评论列表数据
    path('list', views.CommentListView.as_view(), name='comment-list'),  # 评论列表数据
    path('mgt/list', views.CommentMgtListView.as_view(), name='comment-mgt-list'),  # 留言管理列表数据
    path(f'mgt/info/<int:{params.MODEL_UNIQUE_KEY}>', views.CommentMgtInfoView.as_view(),
         name='comment-mgt-info'),  # 留言管理详情数据
    path('page', views.CommentPageView.as_view(), name='comment-page'),  # 评论页面
    path('mgt/page', views.CommentMgtPageView.as_view(), name='comment-mgt-page'),  # 评论管理页面
    path('mgt/count', views.CommentCountView.as_view(), name='comment-count'),  # 评论统计数据
]
