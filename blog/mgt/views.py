from rest_framework import status as drf_status

from common.viewset.basic import BasePageView, BasicListViewSet, BasicInfoViewSet
from common.params import permissions
from blog import models
from blog import serializers


class DashboardPageView(BasePageView):
    """仪表板主页"""
    page = 'mgt/dashboard/dashboard.html'


class ArticleAuditPageView(BasePageView):
    """博客文章审核页面"""
    page = 'mgt/blog/audit/audit.html'


class ArticleListPageView(BasePageView):
    """博客文章列表页面"""
    page = 'mgt/blog/article/list.html'


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
    http_method_names = ('get', 'post', 'put', 'delete', 'patch')
