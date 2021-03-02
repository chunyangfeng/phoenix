# -*- coding: utf-8 -*-
"""视图类抽象Mixin
Date: 2021/1/27 15:11

Author: phoenix@fengchunyang.com

Record:
    2021/1/27 新增文件。

Site: http://www.fengchunyang.com
"""
import json

from django.db import transaction
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework import mixins
from django.shortcuts import HttpResponseRedirect
from rest_framework.settings import api_settings

from common.exceptions.authentication import UnauthorizedException
from common.models.models import UserToken
from common.params import params
from common.params.permissions import PER_BASE


class BasicResponseMixin:
    """Http响应混合类"""
    extra_data = dict()
    _total_count = 0

    def set_extra(self, key, value):
        """设置响应数据的额外内容

        Args:
            key(str): key
            value(any): value
        """
        self.extra_data[key] = value

    @property
    def main_body(self):
        """消息主体结构

        Returns:
            dict: 响应数据结构
        """
        return {
            "result": "",
            "total": 0,
            "extra": dict(),
            "data": "",
        }

    def set_response(self, result, data, extra=None, status=drf_status.HTTP_200_OK):
        """设置响应数据

        Args:
            result(str): 结果
            data(str|list): 数据主体
            extra(dict): 额外的数据主体
            status(str): 状态码

        Returns:
            response(Response): 响应数据
        """
        response = self.main_body
        response["result"] = result
        response["data"] = data
        response["extra"] = extra or dict()
        response["total"] = len(data) if isinstance(data, list) else 0
        return Response(data=response, status=status)

    def set_json(self, data):
        """设置前端响应json数据，契合layui的动态表格结构

        Args:
            data(list): 数据主体

        Returns:
            response(dict): 符合规范的响应数据字典
        """
        return {
            "code": 0,  # 状态码，暂无特殊含义，默认为0
            "msg": "Success" if len(data) else "暂无数据",  # 消息提示，当表格无数据时作为表格内容输出在页面上
            "count": self._total_count,  # 表格行数
            "data": data,  # 数据内容，列表元素为字典，字典形式为单一键值对表示的fields-value
            "extra": self.extra_data,
        }


class BasicListModelMixin(mixins.ListModelMixin, BasicResponseMixin):
    """资源列表批量获取的混合类"""

    def paginate(self, request, *args, **kwargs):
        """分页

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            query_set(QuerySet): 结果集
        """
        page = request.query_params.get(params.PAGINATE_PAGE)
        limit = request.query_params.get(params.PAGINATE_LIMIT)

        # 统计原始数据集总量
        query_set = self.get_queryset()
        total_count = len(query_set)
        self._total_count = total_count

        query_set = self.filter_queryset(query_set)

        if not any([page, limit]):
            return query_set

        start = (int(page) - 1) * int(limit)
        end = int(page) * int(limit)
        return query_set[start:end]

    def _pre_process_list(self, request, *args, **kwargs):
        """list请求预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _post_process_list(self, request, response, *args, **kwargs):
        """list请求后处理

        Args:
            request(Request): DRF Request
            response(HttpResponse): list函数的响应数据
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
            response(Response): 响应数据
        """
        return None, '', response

    def _perform_list(self, request, *args, **kwargs):
        """执行list请求

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        # 分页处理
        query_set = self.paginate(request, *args, **kwargs)

        # 获取序列化器
        serializer = self.get_serializer_class()

        # 序列化queryset
        data = serializer(query_set, many=True).data

        # 构造json数据
        json_data = self.set_json(data)
        return Response(data=json_data, status=drf_status.HTTP_200_OK)

    @transaction.atomic()
    def list(self, request, *args, **kwargs):
        """list请求,设置事务，并在异常的时候进行回滚

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        # list请求预处理
        error, reason = self._pre_process_list(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # list请求
        try:
            response = self._perform_list(request, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Failed to get model list', f'获取资源数据列表失败,错误信息为{error}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)

        # list请求后处理
        error, reason, response = self._post_process_list(request, response, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)
        return response


class BasicRetrieveModelMixin(mixins.RetrieveModelMixin, BasicResponseMixin):
    """单个资源处理流程"""

    def _pre_process_retrieve(self, request, *args, **kwargs):
        """retrieve查询预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_retrieve(self, request, instance, *args, **kwargs):
        """retrieve查询

        Args:
            request(Request): DRF Request
            instance(models.Model): model instance
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
            response(Response): 响应数据
        """
        serializer = self.get_serializer_class()
        data = serializer(instance, many=False).data
        response = self.set_response(result='Success', data=data, status=drf_status.HTTP_200_OK)
        return None, '', response

    def _post_process_retrieve(self, request, instance, *args, **kwargs):
        """retrieve查询后处理

        Args:
            request(Request): DRF Request
            instance(object): 实例
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    @transaction.atomic()
    def retrieve(self, request, *args, **kwargs):
        """执行retrieve操作

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 对请求的响应
        """
        # 查询预处理
        error, reason = self._pre_process_retrieve(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 获取model instance
        instance = self.get_object(*args, **kwargs)

        # 查询
        error, reason, response = self._perform_retrieve(request, instance, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 查询后处理
        error, reason = self._post_process_retrieve(request, instance, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        return response


class BasicBulkCreateModelMixin(mixins.CreateModelMixin, BasicResponseMixin):
    """资源批量创建的混合类"""

    def _pre_process_create(self, request, *args, **kwargs):
        """创建请求预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        self.set_default_data(request, *args, **kwargs)
        return None, ''

    def _pre_validate_create(self, request, *args, **kwargs):
        """创建请求预校验

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_create(self, request, serializer, *args, **kwargs):
        """执行create处理流程

        Args:
            request(Request): DRF Request
            serializer(serializer): DRF serializer
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            inst(object): 创建完成的资源实例
        """
        inst = serializer.save()
        return inst

    def _post_process_create(self, request, instances, *args, **kwargs):
        """执行create后的处理流程

        Args:
            request(Request): DRF Request
            instances (list): 保存数据后的实例列表
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """资源创建，设置事务，出现错误时进行回滚

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        # 请求消息预处理
        error, reason = self._pre_process_create(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 创建请求预校验
        error, reason = self._pre_validate_create(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 获取serializer
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return self.set_response('serializer is invalid', f'序列化器校验失败:{serializer.errors}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)

        # 执行创建
        try:
            instances = self._perform_create(request, serializer, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Failed to create models', f'执行创建失败,错误信息为:{error}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)

        # 创建后处理
        error, reason = self._post_process_create(request, instances, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)
        return self.set_response(params.HTTP_SUCCESS, "创建成功", status=drf_status.HTTP_201_CREATED)


class BasicCreateModelMixin(mixins.CreateModelMixin, BasicResponseMixin):
    """单个资源创建的混合类"""

    def _pre_process_create(self, request, *args, **kwargs):
        """创建请求预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _pre_validate_create(self, request, *args, **kwargs):
        """创建请求预校验

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_create(self, request, serializer, *args, **kwargs):
        """执行create处理流程

        Args:
            request(Request): DRF Request
            serializer(serializer): DRF serializer
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            inst(object): 创建完成的资源实例
        """
        inst = serializer.save()
        return inst

    def _post_process_create(self, request, instances, *args, **kwargs):
        """执行create后的处理流程

        Args:
            request(Request): DRF Request
            instances (list): 保存数据后的实例列表
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        """资源创建，设置事务，出现错误时进行回滚

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        # 请求消息预处理
        error, reason = self._pre_process_create(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 创建请求预校验
        error, reason = self._pre_validate_create(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 获取serializer
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return self.set_response('serializer is invalid', f'序列化器校验失败:{serializer.errors}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)

        # 执行创建
        try:
            instances = self._perform_create(request, serializer, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Failed to create models', f'执行创建失败,错误信息为:{error}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)

        # 创建后处理
        error, reason = self._post_process_create(request, instances, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)
        return self.set_response(params.HTTP_SUCCESS, "创建成功", status=drf_status.HTTP_201_CREATED)


class BasicBulkUpdateModelMixin(mixins.UpdateModelMixin, BasicResponseMixin):
    """批量更新model混合类"""

    def _pre_process_update(self, request, *args, **kwargs):
        """更新预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _validate_update(self, request, *args, **kwargs):
        """更新预校验

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_update(self, serializer, *args, **kwargs):
        """执行更新操作

        Args:
            serializer (Serializer): 序列化器
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _post_process_update(self, request, *args, **kwargs):
        """更新能完成后处理流程

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        """更新操作，设置事务，出现错误时进行数据回滚

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        # 更新前预处理
        error, reason = self._pre_process_update(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 获取序列化器
        serializer = self.get_serializer()
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return self.set_response('Serializer validate failed', '序列化器校验失败',
                                     status=drf_status.HTTP_400_BAD_REQUEST)

        # 更新前预校验
        error, reason = self._validate_update(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 执行更新操作
        try:
            error, reason = self._perform_update(serializer, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Update failed', f'更新失败，错误信息为:{error}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 更新后预处理
        error, reason = self._post_process_update(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        return self.set_response(params.HTTP_SUCCESS, '更新成功')


class BasicUpdateModelMixin(mixins.UpdateModelMixin, BasicResponseMixin):
    """更新model混合类"""

    def _pre_process_update(self, request, *args, **kwargs):
        """更新预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        self.set_default_data(request, *args, **kwargs)
        return None, ''

    def _validate_update(self, request, *args, **kwargs):
        """更新预校验

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_update(self, serializer, *args, **kwargs):
        """执行更新操作

        Args:
            serializer (serializer.Serializer): 序列化器
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        serializer.save()
        return None, ''

    def _post_process_update(self, request, instance, *args, **kwargs):
        """更新能完成后处理流程

        Args:
            request(Request): DRF Request
            instance (models.Models): 数据实例
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        """更新操作，设置事务，出现错误时进行数据回滚

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        # 更新前预处理
        error, reason = self._pre_process_update(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 更新前预校验
        error, reason = self._validate_update(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 获取model instance
        instance = self.get_object(*args, **kwargs)

        # 获取序列化器
        serializer = self.get_serializer(instance, data=request.data, partial=kwargs.get('partial', False))
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return self.set_response('Serializer validate failed', f'序列化器校验失败，错误信息为:{serializer.errors}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)

        # 执行更新操作
        try:
            error, reason = self._perform_update(serializer, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Update failed', f'更新失败，错误信息为:{error}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 更新后预处理
        error, reason = self._post_process_update(request, instance, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        return self.set_response(params.HTTP_SUCCESS, '更新成功')


class BasicBulkDestroyModelMixin(mixins.DestroyModelMixin, BasicResponseMixin):
    """批量删除model"""

    def _pre_process_delete(self, request, *args, **kwargs):
        """删除预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _validate_delete(self, request, *args, **kwargs):
        """删除预校验

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_delete(self, instances, *args, **kwargs):
        """执行删除

        Args:
            instances(QuerySet): 数据实例集
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
            instances(object): 已逻辑删除的实例(物理删除的实例则为None)
        """
        # 逻辑删除
        logic_delete = kwargs.get('logic_delete', False)
        if logic_delete:
            instances.update(is_delete=True)
            return None, '', instances

        # 物理删除
        instances.delete()
        return None, '', None

    def _post_process_delete(self, request, instances=None, *args, **kwargs):
        """删除后处理

        Args:
            request(Request): DRF Request
            instances(object): 已逻辑删除的实例(物理删除的实例无需传递)
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def get_delete_instances(self, request, *args, **kwargs):
        """获取待删除的实例集

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            instances(QuerySet): 实例集
        """
        delete_data = request.data.get('deleted', '')
        query_set = self.get_queryset(*args, **kwargs)
        instances = query_set.filter(id__in=delete_data.split(params.SPLIT_COMMA))
        return instances

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        """删除主流程

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 对请求的响应
        """
        # 删除预处理
        error, reason = self._pre_process_delete(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 删除预校验
        error, reason = self._validate_delete(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 获取待删除的实例集
        insts = self.get_delete_instances(request, *args, **kwargs)

        # 执行删除
        try:
            error, reason, instances = self._perform_delete(insts, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Delete failed', f'删除失败，错误信息为:{error}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)
        if error:
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 删除后处理
        error, reason = self._post_process_delete(request, instances, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        return self.set_response(params.HTTP_SUCCESS, '删除成功', status=drf_status.HTTP_200_OK)


class BasicDestroyModelMixin(mixins.DestroyModelMixin, BasicResponseMixin):
    """删除model"""

    def _pre_process_delete(self, request, *args, **kwargs):
        """删除预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _validate_delete(self, request, *args, **kwargs):
        """删除预校验

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_delete(self, instance, *args, **kwargs):
        """执行删除

        Args:
            instance(models.Model): 数据实例
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
            instances(object): 已逻辑删除的实例(物理删除的实例则为None)
        """
        # 执行逻辑删除
        logic_delete = kwargs.get('logic_delete', False)
        if logic_delete:
            setattr(instance, 'is_delete', True)
            instance.save()
            return None, '', instance

        # 执行物理删除
        instance.delete()
        return None, '', None

    def _post_process_delete(self, request, instance, *args, **kwargs):
        """删除后处理

        Args:
            request(Request): DRF Request
            instances(object): 已逻辑删除的实例(物理删除的实例为None)
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    @transaction.atomic()
    def destroy(self, request, *args, **kwargs):
        """删除主流程

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 对请求的响应
        """
        # 删除预处理
        error, reason = self._pre_process_delete(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 删除预校验
        error, reason = self._validate_delete(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 获取数据对象
        inst = self.get_object(*args, **kwargs)

        # 执行删除
        try:
            error, reason, instance = self._perform_delete(inst, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Delete failed', f'删除失败，错误信息为:{error}',
                                     status=drf_status.HTTP_400_BAD_REQUEST)
        if error:
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 删除后处理
        error, reason = self._post_process_delete(request, instance, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        return self.set_response(params.HTTP_SUCCESS, '删除成功', status=drf_status.HTTP_200_OK)


class BasicBulkPatchModelMixin(BasicResponseMixin):
    """批量处理patch请求的混合类"""

    def _pre_process_patch(self, request, *args, **kwargs):
        """patch请求预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _validate_patch(self, request, *args, **kwargs):
        """patch请求校验

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_patch(self, request, instances, *args, **kwargs):
        """执行patch请求

        Args:
            request(Request): DRF Request
            instances(QuerySet): query set
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
            response(Response): 请求响应数据
        """
        # 执行部分更新
        instances.update(**request.data)

        response = self.set_response(params.HTTP_SUCCESS, data="批量部分更新成功")
        return None, '', response

    def _post_process_patch(self, request, instances, *args, **kwargs):
        """patch请求后处理

        Args:
            request(Request): DRF Request
            instances(QuerySet): QuerySet
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    @transaction.atomic()
    def extra(self, request, *args, **kwargs):
        """

        Args:
            request(Request): DRF Request
            partial(bool): 是否部分更新
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        # patch请求预处理
        error, reason = self._pre_process_patch(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # patch请求预校验
        error, reason = self._validate_patch(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # 获取数据对象
        instances = self.get_queryset()

        # patch请求执行
        try:
            error, reason, response = self._perform_patch(request, instances, *args, **kwargs)
            if error:
                transaction.set_rollback(True)
                return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Failed to patch', f'patch请求处理失败,错误原因:{error}')

        # patch请求后处理
        error, reason = self._post_process_patch(request, instances, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        return response


class BasicPatchModelMixin(BasicResponseMixin):
    """patch请求的混合类"""

    def _pre_process_patch(self, request, *args, **kwargs):
        """patch请求预处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _validate_patch(self, request, *args, **kwargs):
        """patch请求校验

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    def _perform_patch(self, request, instance, *args, **kwargs):
        """执行patch请求的部分更新

        Args:
            request(Request): DRF Request
            instance(models.Model): model instance
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
            response(Response): 请求响应数据
        """
        # 执行部分更新
        for key, value in request.data.items():
            setattr(instance, key, value)

        instance.save()

        response = self.set_response(result=params.HTTP_SUCCESS, data="部分更新成功")
        return None, '', response

    def _post_process_patch(self, request, *args, **kwargs):
        """patch请求后处理

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

    @transaction.atomic()
    def extra(self, request, partial=False, *args, **kwargs):
        """

        Args:
            request(Request): DRF Request
            partial(bool): 是否部分更新
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        # patch请求预处理
        error, reason = self._pre_process_patch(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        # patch请求预校验
        error, reason = self._validate_patch(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)
        # 获取数据对象
        instance = self.get_object(*args, **kwargs)

        # patch请求执行
        try:
            error, reason, response = self._perform_patch(request, instance, *args, **kwargs)
            if error:
                transaction.set_rollback(True)
                return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            transaction.set_rollback(True)
            return self.set_response('Failed to patch', f'patch请求处理失败,错误原因:{error}')

        # patch请求后处理
        error, reason = self._post_process_patch(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.set_response(error, reason, status=drf_status.HTTP_400_BAD_REQUEST)

        return response


class BasicAuthPermissionViewMixin(BasicResponseMixin):
    """授权认证/权限校验混合类"""
    permission_name = PER_BASE  # 权限名称
    authentication_enable = True  # 是否启用认证检查
    permission_enable = True  # 是否启用权限检查
    http_method_names = ('get', 'post', 'put', 'delete', 'patch')

    def dispatch(self, request, *args, **kwargs):
        """路由分发

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        # 自定义认证校验
        is_auth = self.check_authentication(request, *args, **kwargs)
        if not is_auth:
            return HttpResponseRedirect(reverse('401'))

        # 自定义权限校验
        has_perm = self.check_permission(request, *args, **kwargs)
        if not has_perm:
            return HttpResponseRedirect(reverse('403'))

        response = super().dispatch(request, *args, **kwargs)
        return response

    @staticmethod
    def render_unauthorized_page():
        """未认证页面

        Returns:
            HttpResponse: response
        """
        return HttpResponseRedirect(reverse('401'))

    @staticmethod
    def render_no_permission_page():
        """未授权页面

        Returns:
            HttpResponse: response
        """
        return HttpResponseRedirect(reverse('403'))

    def check_authentication(self, request, *args, **kwargs):
        """认证检查

        Args:
            request(Request): request
            *args(list): args
            **kwargs(dict): kwargs

        Returns:
            is_auth(bool): 是否认证

        Raises:
            UnauthorizedException: 未认证
        """
        is_auth = True
        if self.authentication_enable:

            token = request.session.get(params.SESSION_TOKEN_KEY)

            if not token:
                is_auth = False

            try:
                UserToken.objects.get(token=token, is_expired=False)
            except UserToken.DoesNotExist:
                del request.session
                is_auth = False

        return is_auth

    def check_permission(self, request, *args, **kwargs):
        """权限检查

        Args:
            request(Request): request
            *args(list): args
            **kwargs(dict): kwargs

        Returns:
            has_perm(bool): 是否拥有权限
        """
        has_perm = True
        if self.permission_enable:
            pass
        return has_perm


class BasicCommonViewMixin:
    """视图集的通用混合类，提供通用的处理方法"""
    data_type = params.DATA_TYPE_COMMON  # 数据类型

    @staticmethod
    def _clear_query_params(value):
        """清洗查询字符串中的异常字符
        1.undefined/null: None
        2.左右两侧空格: ''
        3.'true'/'false': True/False

        Args:
            value(str): 待处理字符

        Returns:
            value(str): 清洗完毕后的值
        """
        if value in ('undefined', 'null'):
            value = None
        if value == 'true':
            value = True
        if value == 'false':
            value = False
        value = value.rstrip(' ')
        value = value.lstrip(' ')
        return value

    def initial_query_params(self):
        """初始化查询参数"""
        self.request.query_params._mutable = True  # 将QueryDict修改为可变

        _pop_key = list()

        for key, value in self.request.query_params.items():
            # 清洗value
            value = self._clear_query_params(value)

            if value is None or len(value) == 0:
                _pop_key.append(key)

        # 如果value没有传值，则从查询参数中删除
        for pop_key in _pop_key:
            self.request.query_params.pop(pop_key)

        self.request.query_params._mutable = False

    @staticmethod
    def set_default_data(request, *args, **kwargs):
        """设置系统级别的内置数据

        Args:
            request(Request): request
            *args(list): args
            **kwargs(dict): kwargs
        """
        # 设置默认参数
        request.data._mutable = True
        login_user = request.session.get(params.SESSION_USER_KEY).get('username')
        request.data['creator'] = login_user
        request.data['owner'] = login_user
        request.data._mutable = False










