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
from django.urls import reverse

from blog.index.adapt import adapt_get_comment_count
from blog.models import Article, ArticleClassify, AccessRecord, SubscribeRecord, InnerMessage
from blog.serializers import ArticleDetailSerializer, ArticleSiteMapSerializer, ArticleSerializer, \
    InnerMessageListSerializer, SubscribeRecordListSerializer
from common import permissions
from common.params import MODEL_UNIQUE_KEY
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
            "article_count": Article.objects.filter(is_publish=True).count(),
            "fans_count": SubscribeRecord.objects.count(),
            "classify_count": ArticleClassify.objects.count(),
            "comment_count": adapt_get_comment_count(),
            "access_count": AccessRecord.objects.count(),
        }
        return self.set_response(result='Success', data=[data, ])


class IndexVisitorInfoPageView(BasePageView):
    """访客信息页面"""
    authentication_enable = False
    page = 'index/visitor/form.html'


class IndexVisitorMessageListView(BasicListViewSet):
    """访客私信接口"""
    queryset = InnerMessage.objects.all()
    serializer_class = InnerMessageListSerializer
    permission_name = permissions.PER_VISITOR_MESSAGE
    authentication_enable = False


class IndexVisitorScribeListView(BasicListViewSet):
    """访客订阅接口"""
    queryset = SubscribeRecord.objects.all()
    serializer_class = SubscribeRecordListSerializer
    permission_name = permissions.PER_VISITOR_MESSAGE
    authentication_enable = False

    def patch(self, request, *args, **kwargs):
        """额外的逻辑控制，查重

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        data = {'is_repeat': False}
        email = request.data.get('email')
        queryset = SubscribeRecord.objects.filter(email=email)
        if queryset.exists():
            data['is_repeat'] = True
        return self.set_response(result='ok', data=data)


class IndexHotArticleInfoView(BasicInfoViewSet):
    """热门文章数据接口"""
    queryset = Article.objects.filter(is_publish=True).order_by('-read_count')[:10]
    serializer_class = DoNothingSerializer
    permission_name = permissions.PER_HOT_ARTICLE
    authentication_enable = False
    http_method_names = ('get', )

    @staticmethod
    def _get_link(pk):
        """获取文章相对链接

        Args:
            pk(int): 自增id

        Returns:
            link(str): 相对链接
        """
        return reverse('article-detail-page', kwargs={MODEL_UNIQUE_KEY: pk})

    def get(self, request, *args, **kwargs):
        """获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        articles = self.get_queryset()
        data = [{
            'title': article.title,
            'read_count': article.read_count,
            'link': self._get_link(article.id)
        } for article in articles]
        return self.set_response(result='Success', data=data)
