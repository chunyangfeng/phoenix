# -*- coding: utf-8 -*-
"""
时间: 2020/12/17 23:51

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/17 新增文件。

重要说明:
"""
from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


class UserAccessAuthentication(authentication.BasicAuthentication):
    """
    用户认证
    """

    def authenticate(self, request):
        """

        Args:
            request:

        Returns:

        """
        return 1, 2


# class ExampleAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         username = request.META.get('X_USERNAME')
#         if not username:
#             return None
#
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             raise exceptions.AuthenticationFailed('No such user')
#
#         return (user, None)
