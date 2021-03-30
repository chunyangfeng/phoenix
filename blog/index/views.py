# -*- coding: utf-8 -*-
"""主页视图
时间: 2021/3/2 10:52

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/2 新增文件。

重要说明:
"""
from django.db.models import QuerySet

from blog.models import Article, ArticleClassify, AccessRecord
from blog.serializers import ArticleDetailSerializer, ArticleSiteMapSerializer, ArticleSerializer
from common import permissions
from common.serializers import DoNothingSerializer
from common.views import BasePageView, BasicListViewSet, BasicInfoViewSet


class AuthForbiddenPageView(BasePageView):
    """未授权错误页面"""
    authentication_enable = False
    page = 'errors/401.html'


class AuthNoPermissionPageView(BasePageView):
    """未授权错误页面"""
    authentication_enable = False
    page = 'errors/403.html'


class IndexPageView(BasePageView):
    """博客主页"""
    authentication_enable = False
    page = 'index/index.html'


class ArticleDetailPageView(BasePageView):
    """博客文章详情页"""
    model_class = Article
    serializer_class = ArticleDetailSerializer
    authentication_enable = False
    page = 'index/detail/detail.html'

    def _pre_get(self, request, *args, **kwargs):
        """响应页面之前的操作，设置文章数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，None为没有错误
            reason(str): 错误原因，为''则没有错误
        """
        error, reason, instance = self.get_object(*args, **kwargs)
        if error:
            return error, reason

        # 添加文章数据至模板对象中
        self.data['article'] = self.serializer_class(instance, many=False).data

        setattr(self, 'instance', instance)
        return None, ''

    def _post_get(self, request, response, *args, **kwargs):
        """响应页面之后的操作，增加文章的阅读数

        Args:
            request(Request): http request
            response(Response): 响应主体
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，None为没有错误
            reason(str): 错误原因，为''则没有错误
            response(Response): 响应主体
        """
        # 当访问成功时，将文章的阅读数量加一
        instance = getattr(self, 'instance')
        instance.read_count += 1
        instance.save()
        return None, '', response


class IndexSiteMapPageView(BasePageView):
    """网站地图"""
    model_class = Article
    serializer_class = ArticleSiteMapSerializer
    authentication_enable = False
    page = 'index/map/map.html'

    def _pre_get(self, request, *args, **kwargs):
        """响应页面之前的操作，设置文章链接

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，None为没有错误
            reason(str): 错误原因，为''则没有错误
        """
        instances = self.model_class.objects.filter(is_publish=True)

        # 添加文章链接数据至模板对象中
        self.data['articles'] = self.serializer_class(instances, many=True).data
        return None, ''


class IndexArticleListView(BasicListViewSet):
    """首页展示的文章列表接口"""
    queryset = Article.objects.filter(is_publish=True)
    serializer_class = ArticleSerializer
    permission_name = permissions.PER_ARTICLE
    authentication_enable = False
    http_method_names = ('get', )


class IndexShowCardInfoView(BasicInfoViewSet):
    """个人名片数据接口"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer
    permission_name = permissions.PER_SHOW_CARD
    authentication_enable = False
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
        data = {
            "article_count": Article.objects.count(),
            "fans_count": "0",
            "classify_count": ArticleClassify.objects.count(),
            "comment_count": "0",
            "access_count": AccessRecord.objects.count(),
        }
        return self.set_response(result='Success', data=[data, ])
