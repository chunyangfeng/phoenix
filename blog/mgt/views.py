# -*- coding: utf-8 -*-
"""后台管理视图文件
时间: 2021/2/18 10:52

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/18 新增文件。

重要说明:
"""
from rest_framework import status as drf_status

from common.viewset.basic import BasePageView, BasicListViewSet, BasicInfoViewSet
from common.params import permissions
from blog import models
from blog import serializers


class DashboardPageView(BasePageView):
    """仪表板主页"""
    page = 'mgt/dashboard/dashboard.html'


class ArticleListPageView(BasePageView):
    """博客文章列表页面"""
    page = 'mgt/blog/list/list.html'


class ArticleDataPageView(BasePageView):
    """博客文章数据管理页面"""
    page = 'mgt/blog/data/data.html'


class ArticleDataClassifyPageView(BasePageView):
    """博客文章数据管理-博客分类新增页面"""
    page = 'mgt/blog/data/classify/add.html'


class ArticleDataTagPageView(BasePageView):
    """博客文章数据管理-博客标签新增页面"""
    page = 'mgt/blog/data/tag/add.html'


class ArticleInfoPageView(BasePageView):
    """博客文章增页面"""
    page = 'mgt/blog/info/info.html'


class ArticleListApiView(BasicListViewSet):
    """文章列表接口"""
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_name = permissions.PER_ARTICLE
    http_method_names = ('get', )


class ArticleInfoApiView(BasicInfoViewSet):
    """文章列表接口"""
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_name = permissions.PER_ARTICLE


class ArticleClassifyListApiView(BasicListViewSet):
    """文章分类列表接口"""
    queryset = models.ArticleClassify.objects.all()
    serializer_class = serializers.ArticleClassifySerializer
    permission_name = permissions.PER_ARTICLE_CLASSIFY


class ArticleClassifyInfoApiView(BasicInfoViewSet):
    """文章分类详情接口"""
    queryset = models.ArticleClassify.objects.all()
    serializer_class = serializers.ArticleClassifySerializer
    permission_name = permissions.PER_ARTICLE_CLASSIFY


class ArticleTagListApiView(BasicListViewSet):
    """文章标签列表接口"""
    queryset = models.ArticleTag.objects.all()
    serializer_class = serializers.ArticleTagSerializer
    permission_name = permissions.PER_ARTICLE_TAG


class ArticleTagInfoApiView(BasicInfoViewSet):
    """文章标签详情接口"""
    queryset = models.ArticleTag.objects.all()
    serializer_class = serializers.ArticleTagSerializer
    permission_name = permissions.PER_ARTICLE_TAG
