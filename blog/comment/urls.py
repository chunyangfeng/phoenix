"""评论模块路由

Author: Fengchunyang

Site: http://www.fengchunyang.com

Date: 2021/5/11 11:03

Desc:
    2021/5/11 11:03 add file.
"""
from django.urls import path

from . import views

urlpatterns = [
    path('list', views.CommentListView.as_view(), name='comment-list'),  # 评论列表数据
]
