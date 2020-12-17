# -*- coding: utf-8 -*-
"""
时间: 2020/12/17 23:41

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/17 新增文件。

重要说明:
"""
from rest_framework import permissions


class UserAccessPermission(permissions.BasePermission):
    """
    用户登陆权限检查
    """
    def has_permission(self, request, view):
        """

        Args:
            request:
            view:

        Returns:

        """
        if request.user is None:
            return


# class BlacklistPermission(permissions.BasePermission):
#     """
#     对列入黑名单的IP进行全局权限检查。
#     """
#
#     def has_permission(self, request, view):
#         ip_addr = request.META['REMOTE_ADDR']
#         blacklisted = Blacklist.objects.filter(ip_addr=ip_addr).exists()
#         return not blacklisted
#
#     def has_object_permission(self, request, view, obj):
#         # 任何请求都允许读取权限，
#         # 所以我们总是允许GET，HEAD或OPTIONS 请求.
#         if request.method in permissions.SAFE_METHODS:
#             return True
#
#         # 示例必须要有一个名为`owner`的属性
#         return obj.owner == request.user
