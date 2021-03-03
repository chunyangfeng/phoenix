# -*- coding: utf-8 -*-
"""主页视图
时间: 2021/3/2 10:52

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/2 新增文件。

重要说明:
"""
from rest_framework import status as drf_status

from blog.models import Article
from blog.serializers import ArticleDetailSerializer
from common.viewset.basic import BasePageView
from common.params import params


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
    """博客主页"""
    model_class = Article
    serializer_class = ArticleDetailSerializer
    authentication_enable = False
    page = 'index/detail/detail.html'

    def _pre_get(self, request, *args, **kwargs):
        """响应页面之前的操作，由子类自定义

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，None为没有错误
            reason(str): 错误原因，为''则没有错误
        """
        pk = kwargs.get(params.MODEL_UNIQUE_KEY)
        if not pk:
            return self.set_response(result=params.HTTP_Failed, data='无效的文章ID',
                                     status=drf_status.HTTP_400_BAD_REQUEST)
        # 获取实例数据
        model = self.get_model_class()
        instance = model.objects.get(pk=pk)
        self.data['article'] = self.serializer_class(instance, many=False).data
        return None, ''
