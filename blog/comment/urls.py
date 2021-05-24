"""评论模块路由

Author: Fengchunyang

Site: https://www.fengchunyang.com

Date: 2021/5/11 11:03

Desc:
    2021/5/11 11:03 add file.
"""
from django.urls import path

from . import views

urlpatterns = [
    path('article-comment/list', views.ArticleCommentListView.as_view(), name='article-comment-list'),  # 文章评论列表数据
    path('list', views.CommentListView.as_view(), name='comment-list'),  # 评论列表数据
    path('page', views.CommentPageView.as_view(), name='comment-page'),  # 评论页面
]
