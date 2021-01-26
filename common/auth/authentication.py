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
from common.models.models import User


class UserAccessAuthentication(authentication.BasicAuthentication):
    """
    用户认证
    """

    def authenticate(self, request):
        """自定义用户认证

        Args:
            request:

        Returns:

        """
        auth = request.session.get('authentication')
        perm = request.session.get('permission')

        if auth is None or perm is None:
            del request.session
            return None

        try:
            user = User.objects.get(username=auth.get('username'))
            return user, perm
        except User.DoesNotExist:
            return None
