# -*- coding: utf-8 -*-
"""
时间: 2020/12/17 23:51

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/17 新增文件。

重要说明:
"""
from rest_framework import authentication
from rest_framework import exceptions
from common.models.models import UserToken


class UserAccessAuthentication(authentication.BasicAuthentication):
    """用户认证"""

    def authenticate(self, request):
        """自定义用户认证

        Args:
            request:

        Returns:

        """
        token = request.session.get('token')

        if not token:
            del request.session
            raise exceptions.AuthenticationFailed('用户认证失败')

        try:
            token_obj = UserToken.objects.get(token=token, is_expired=False)
        except UserToken.DoesNotExist:
            raise exceptions.AuthenticationFailed('用户认证失败')

        return token_obj.user.username, token_obj
