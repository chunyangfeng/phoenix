# -*- coding: utf-8 -*-
"""
时间: 2020/12/17 23:51

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/17 新增文件。

重要说明:
"""
from django.utils import timezone

from rest_framework import authentication
from rest_framework import exceptions
from common.models.models import UserToken, User
from common.params import params
from common.params.params import ANONYMOUS_TOKEN


class UserAccessAuthentication(authentication.BasicAuthentication):
    """用户认证"""

    def authenticate(self, request):
        """自定义用户认证

        Args:
            request(HttpRequest): request

        Returns:
            username(str): 用户名
            token(object): token对象
        """
        print(request.session)
        token = request.session.get(params.SESSION_KEY, dict()).get(params.SESSION_TOKEN_KEY)

        if not token:
            raise exceptions.AuthenticationFailed('用户认证失败')

        try:
            token_obj = UserToken.objects.get(token=token, is_expired=False)
        except UserToken.DoesNotExist:
            del request.session
            raise exceptions.AuthenticationFailed('用户认证失败')

        return token_obj.user.username, token_obj

    def authenticate_header(self, request):
        """authenticate_header

        Args:
            request:

        Returns:

        """
        return 'Unauthentication'


class NoAuthentication(authentication.BasicAuthentication):
    """全局公共资源认证，当某个资源的访问不需要认证时，使用此类"""

    def authenticate(self, request):
        """自定义认证规则

        Args:
            request(HttpRequest): request

        Returns:
            username(str): 用户名
            token(object): token对象
        """
        anonymous_user = User.objects.get(username='anonymous')
        token_obj, _ = UserToken.objects.get_or_create(user=anonymous_user, defaults={
            'token': ANONYMOUS_TOKEN,
            'login_time': timezone.now()
        })
        return token_obj.user.username, token_obj
