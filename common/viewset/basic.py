# -*- coding: utf-8 -*-
"""通用视图
时间: 2020/11/25 15:13

作者: Fengchunyang

更改记录:
    2020/11/25 新增文件。

重要说明:
"""
from common.mixins import views_mixin
from rest_framework.generics import GenericAPIView


class BasicListViewSet(GenericAPIView,
                       views_mixin.BasicCreateModelMixin,
                       views_mixin.BasicListModelMixin,
                       views_mixin.BasicUpdateModelMixin,
                       views_mixin.BasicDestroyModelMixin):
    """
    批量进行资源的CRUD操作，支持以下操作：
    1.资源的批量创建
    2.资源的批量查询
    3.资源的批量更新
    4.资源的批量删除
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
