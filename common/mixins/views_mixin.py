# -*- coding: utf-8 -*-
"""视图类抽象Mixin
Date: 2021/1/27 15:11

Author: phoenix@fengchunyang.com

Record:
    2021/1/27 新增文件。

Site: http://www.fengchunyang.com
"""
from django.db import transaction
from rest_framework.response import Response
from rest_framework import status as drf_status
from rest_framework import mixins

from common.params.permissions import PER_BASE


class BasicResponseMixin:
    """Http响应混合类"""

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

    # def set_error_response(self, error, reason, status=drf_status.HTTP_400_BAD_REQUEST):
    #     """设置错误响应数据
    #
    #     Args:
    #         error(str): 错误信息
    #         reason(str): 错误原因
    #         status(str): 状态码，默认为400
    #
    #     Returns:
    #         response(Response): 响应数据
    #     """
    #     data = self.main_body
    #     data["result"] = "Failed"
    #     data["data"] = {
    #         "error": error,
    #         "reason": reason
    #     }
    #     return Response(data=data, status=status)
    #
    # def set_msg_response(self, msg, status=drf_status.HTTP_200_OK):
    #     """设置响应数据
    #
    #     Args:
    #         msg(str): 返回主体消息
    #         status(str): 状态码，默认为200
    #
    #     Returns:
    #         response(Response): 响应数据
    #     """
    #     data = self.main_body
    #     data["result"] = "Success"
    #     data["data"] = msg
    #     return Response(data=data, status=status)
    #
    # def set_data_response(self, data, status=drf_status.HTTP_200_OK):
    #     """设置响应数据
    #
    #     Args:
    #         data(list): 返回主体消息
    #         status(str): 状态码，默认为200
    #
    #     Returns:
    #         response(Response): 响应数据
    #     """
    #     data = self.main_body
    #     data["result"] = "ok"
    #     data["data"] = data
    #     data["total"] = len(data)
    #     return Response(data=data, status=status)

    def get_response(self, result, data, status=drf_status.HTTP_200_OK):
        """设置响应数据

        Args:
            result(str): 结果
            data(str|list): 数据主体
            status(str): 状态码

        Returns:
            response(Response): 响应数据
        """
        response = self.main_body
        response["result"] = result
        response["data"] = data
        response["total"] = len(data) if isinstance(data, list) else 0
        return Response(data=response, status=status)


class BasicListModelMixin(mixins.ListModelMixin, BasicResponseMixin):
    """资源列表获取的混合类"""

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
        # 1.获取queryset
        # 2.分页处理
        # 3.序列化queryset
        return Response({'result': 'ok', 'data': {}})

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
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # list请求
        try:
            response = self._perform_list(request, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.get_response('Failed to get model list', f'获取资源数据列表失败,错误信息为{error}',
                                     drf_status.HTTP_400_BAD_REQUEST)

        # list请求后处理
        error, reason, response = self._post_process_list(request, response, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)
        return response


class BasicCreateModelMixin(mixins.CreateModelMixin, BasicResponseMixin):
    """资源创建的混合类"""

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

    def _perform_create(self, serializer, *args, **kwargs):
        """执行create处理流程

        Args:
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
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 创建请求预校验
        error, reason = self._pre_validate_create(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 获取serializer
        serializer = self.get_serializer()
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return self.get_response('serializer is invalid', '序列化器校验失败', drf_status.HTTP_400_BAD_REQUEST)

        # 执行创建
        try:
            instances = self._perform_create(serializer, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.get_response('Failed to create models', f'执行创建失败,错误信息为:{error}',
                                     drf_status.HTTP_400_BAD_REQUEST)

        # 创建后处理
        error, reason = self._post_process_create(request, instances, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)
        return self.get_response("create success", "创建成功", drf_status.HTTP_201_CREATED)


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
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 获取序列化器
        serializer = self.get_serializer()
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return self.get_response('Serializer validate failed', '序列化器校验失败', drf_status.HTTP_400_BAD_REQUEST)

        # 更新前预校验
        error, reason = self._validate_update(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 执行更新操作
        try:
            error, reason = self._perform_update(serializer, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.get_response('Update failed', f'更新失败，错误信息为:{error}', drf_status.HTTP_400_BAD_REQUEST)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 更新后预处理
        error, reason = self._post_process_update(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        return self.get_response('update success', '更新成功')


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

    def _perform_delete(self, serializer, *args, **kwargs):
        """执行删除

        Args:
            serializer(Serializer): 序列化器
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
            instances(object): 已逻辑删除的实例(物理删除的实例则为None)
        """
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
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 删除预校验
        error, reason = self._validate_delete(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 获取序列化器
        serializer = self.get_serializer()
        if not serializer.is_valid():
            transaction.set_rollback(True)
            return self.get_response('Serializer validate failed', '序列化器校验失败', drf_status.HTTP_400_BAD_REQUEST)

        # 执行删除
        try:
            error, reason, instances = self._perform_delete(self, serializer, *args, **kwargs)
        except Exception as error:
            transaction.set_rollback(True)
            return self.get_response('Delete failed', f'删除失败，错误信息为:{error}', drf_status.HTTP_400_BAD_REQUEST)
        if error:
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 删除后处理
        error, reason = self._post_process_delete(request, instances, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        return self.get_response('delete success', '删除成功', drf_status.HTTP_200_OK)


class BasicRetrieveModelMixin(mixins.RetrieveModelMixin, BasicResponseMixin):
    """单个model处理流程"""

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

    def _perform_retrieve(self, request, *args, **kwargs):
        """retrieve查询

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
        """
        return None, ''

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
            instance(object): 实例
        """
        return None, '', instance

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
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 查询
        error, reason, response = self._perform_retrieve(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # 查询后处理
        error, reason = self._post_process_retrieve(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

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

    def _perform_patch(self, request, *args, **kwargs):
        """执行patch请求

        Args:
            request(Request): DRF Request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，没有错误为None
            reason(str): 错误原因，没有错误为''
            response(Response): 请求响应数据
        """
        response = self.get_response("patch success", "patch请求成功")
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
    def extra(self, request, *args, **kwargs):
        """

        Args:
            request(Request): DRF Request
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
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # patch请求预校验
        error, reason = self._validate_patch(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        # patch请求执行
        try:
            error, reason = self._perform_patch(request, *args, **kwargs)
            if error:
                transaction.set_rollback(True)
                return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)
        except Exception as error:
            transaction.set_rollback(True)
            return self.get_response('Failed to patch', f'patch请求处理失败,错误原因:{error}')

        # patch请求后处理
        error, reason = self._post_process_patch(request, *args, **kwargs)
        if error:
            transaction.set_rollback(True)
            return self.get_response(error, reason, drf_status.HTTP_400_BAD_REQUEST)

        return self.get_response('ok', '成功')


class BasicPermissionViewMixin:
    """权限校验混合类"""
    permission_class = None  # 权限校验器
    permission_module = 'phoenix'  # 权限模块
    permission_name = PER_BASE  # 权限名称









