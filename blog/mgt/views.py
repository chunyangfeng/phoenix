# -*- coding: utf-8 -*-
"""后台管理视图文件
时间: 2021/2/18 10:52

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/18 新增文件。

重要说明:
"""
import datetime

from django.db.models import QuerySet

from blog.index.adapt import adapt_get_comment_count
from blog.params import TASK_STATUS_PLAN
from common.serializers import DoNothingSerializer
from common.views import BasePageView, BasicListViewSet, BasicInfoViewSet
from common import permissions
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


class ArticleInfoApiView(BasicInfoViewSet):
    """文章详情接口"""
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


class ArticleSerialListApiView(BasicListViewSet):
    """文章系列列表接口"""
    queryset = models.ArticleSerial.objects.all()
    serializer_class = serializers.ArticleSerialSerializer
    permission_name = permissions.PER_ARTICLE_SERIAL


class DashboardStatisticView(BasicInfoViewSet):
    """仪表板统计数据接口"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer
    permission_name = permissions.PER_DASHBOARD
    http_method_names = ('get', )

    def get(self, request, *args, **kwargs):
        """获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        articles = models.Article.objects.all()
        data = {
            "article_count": articles.count(),
            "unpublish_count": articles.filter(is_publish=False).count(),
            "tags_count": models.ArticleTag.objects.count(),
            "comment_count": adapt_get_comment_count(),
            "access_count": models.AccessRecord.objects.count(),
            "flink_apply": 0,
            "fans_count": models.SubscribeRecord.objects.filter(enable=True).count()
        }
        return self.set_response(result='Success', data=[data, ])


class DashboardAccessChart(BasicInfoViewSet):
    """仪表板访问数据折线图接口"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer
    permission_name = permissions.PER_DASHBOARD
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        """获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        data = list()
        now = datetime.datetime.now()
        flag = 31
        while flag != 0:
            data.insert(0, {
                "date": now.strftime("%m-%d"),
                "count": models.AccessRecord.objects.filter(
                    atime__year=now.year, atime__month=now.month, atime__day=now.day
                ).count()
            })
            now -= datetime.timedelta(days=1)
            flag -= 1
        return self.set_response(result='Success', data=data)


class DashboardArticleChart(BasicInfoViewSet):
    """仪表板文章发表数据柱状图接口"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer
    permission_name = permissions.PER_DASHBOARD
    http_method_names = ('get',)

    def get(self, request, *args, **kwargs):
        """获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        data = list()
        now = datetime.datetime.now()
        flag = 31
        while flag != 0:
            data.insert(0, {
                "date": now.strftime("%m-%d"),
                "count": models.Article.objects.filter(
                    ctime__year=now.year, ctime__month=now.month, ctime__day=now.day
                ).count()
            })
            now -= datetime.timedelta(days=1)
            flag -= 1
        return self.set_response(result='Success', data=data)


class DashboardProcessData(BasicInfoViewSet):
    """仪表板事件进度统计接口"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer
    permission_name = permissions.PER_DASHBOARD
    http_method_names = ('get',)

    @staticmethod
    def _get_article_update_rate(days=30):
        """获取文章的更新频率

        Args:
            days(int): 统计周期，默认为最近30天

        Returns:
            rate(float): 更新频率
        """
        now = datetime.datetime.now()
        start = now - datetime.timedelta(days=days)
        date_range = (
            f'{start.strftime("%F")} 00:00:00',
            f'{now.strftime("%F")} 23:59:59'
        )
        obj = models.Article.objects.filter(ctime__range=date_range)
        update_date = [qs.strftime("%F") for qs in obj.values_list('ctime', flat=True)]
        update_date = list(set(update_date))
        return round(len(update_date)*100 / days, 2)

    @staticmethod
    def _get_incomplete_task_rate():
        """获取未完成任务占比

        Returns:
            rate(float): 未完成任务占比
        """
        total = models.ProjectPlanTask.objects.count()
        incomplete = models.ProjectPlanTask.objects.filter(status=TASK_STATUS_PLAN).count()
        if total == 0:  # 如果没有计划任务，则未完成任务占比为0
            return 0
        return round(incomplete*100/total, 2)

    def get(self, request, *args, **kwargs):
        """获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        data = list()
        data.append({
            "article_update_rate": self._get_article_update_rate(),
            "task_incomplete_rate": self._get_incomplete_task_rate(),
        })
        return self.set_response(result='Success', data=data)
