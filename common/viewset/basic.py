# -*- coding: utf-8 -*-
"""通用视图
时间: 2020/11/25 15:13

作者: Fengchunyang

更改记录:
    2020/11/25 新增文件。

重要说明:
"""
from django.conf import settings
from django.shortcuts import render
from django.views import View

from common.mixins import views_mixin
from rest_framework.generics import GenericAPIView


class BasicListViewSet(GenericAPIView,
                       views_mixin.BasicPermissionViewMixin,
                       views_mixin.BasicCreateModelMixin,
                       views_mixin.BasicListModelMixin,
                       views_mixin.BasicUpdateModelMixin,
                       views_mixin.BasicDestroyModelMixin,
                       views_mixin.BasicPatchModelMixin):
    """
    批量进行资源的CRUD操作，支持以下操作：
    1.资源的批量创建
    2.资源的批量查询
    3.资源的批量更新
    4.资源的批量删除
    5.资源的批量处理（通过patch方法进行额外的逻辑控制，比如字段查重等）
    """

    def get(self, request, *args, **kwargs):
        """批量获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """批量创建资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """批量删除资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """批量获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """额外的逻辑控制

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.extra(request, *args, **kwargs)


class BasicInfoViewSet(GenericAPIView,
                       views_mixin.BasicPermissionViewMixin,
                       views_mixin.BasicCreateModelMixin,
                       views_mixin.BasicRetrieveModelMixin,
                       views_mixin.BasicUpdateModelMixin,
                       views_mixin.BasicDestroyModelMixin,
                       views_mixin.BasicPatchModelMixin):
    """
    单个资源的CRUD操作，支持以下操作：
    1.资源创建
    2.资源查询
    3.资源更新
    4.资源删除
    5.资源处理（通过patch方法进行额外的逻辑控制，比如字段查重等）
    """

    def get(self, request, *args, **kwargs):
        """获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """创建资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """删除资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.destroy(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """额外的逻辑控制

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        return self.extra(request, *args, **kwargs)


class BasePageView(View, views_mixin.BasicPermissionViewMixin):
    """Html页面响应基类"""
    app = settings.WEB_APP  # 前端页面的根路径
    page = None  # html页面的相对路径，用于render函数渲染
    data = dict()  # 页面渲染时传递的数据
    http_method_names = ['get', ]  # 仅允许get方式

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
        return None, ''

    def _perform_get(self, request, *args, **kwargs):
        """渲染页面内容

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应主体
        """
        return render(request, f'{self.app}{self.page}', self.data)

    def _post_get(self, request, *args, **kwargs):
        """响应页面之后的操作，由子类自定义

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，None为没有错误
            reason(str): 错误原因，为''则没有错误
        """
        return None, ''

    def get(self, request, *args, **kwargs):
        """get方法，返回请求的页面内容

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应主体
        """

        error, reason = self._pre_get(request, *args, **kwargs)
        if error:
            # TODO 后续统一错误返回
            return error, reason

        response = self._perform_get(request, *args, **kwargs)

        error, reason = self._post_get(request, *args, **kwargs)
        if error:
            # TODO 后续统一错误返回
            return error, reason
        return response
