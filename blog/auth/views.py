# -*- coding: utf-8 -*-
"""认证授权视图层
时间: 2021/3/26 9:37

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/26 新增文件。

重要说明:
"""
from django.db.models import QuerySet
from django.urls import reverse
from django.utils import timezone
from rest_framework import status as drf_status
from rest_framework.response import Response

from common.serializers import DoNothingSerializer
from common.views import BasicInfoViewSet, BasePageView
from blog.auth.models import User, UserToken
from common import params
from common.utils import sington, encryption


class UserLoginPageView(BasePageView):
    """用户登录主页"""
    authentication_enable = False
    page = "auth/login.html"


class UserLoginView(BasicInfoViewSet):
    """用户登录相关操作"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer
    authentication_enable = False
    http_method_names = ('post', 'get')

    def get(self, request, *args, **kwargs):
        """获取用户认证状态

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        token = request.session.get(params.SESSION_KEY, dict()).get(params.SESSION_TOKEN_KEY)
        result = 'Success' if token else 'Failed'
        data = '已经登录' if token else '尚未登录'
        status = drf_status.HTTP_200_OK if token else drf_status.HTTP_401_UNAUTHORIZED
        return self.set_response(result, data, status)

    def post(self, request, *args, **kwargs):
        """登录操作

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        # 数据校验
        username = request.data.get('username')
        password = request.data.get('password')
        if not any([username, password]):
            return self.set_response('username or password is required', '用户名或密码不能为空',
                                     status=drf_status.HTTP_400_BAD_REQUEST)

        # 登录流程
        private_key = request.session.get(params.RSA_SESSION_PRIVATE_KEY)
        raw_password = encryption.rsa_decrypt(password, private_key)
        encrypt_password = sington.aes.encrypt(raw_password)
        now = timezone.now()
        try:
            user = User.objects.get(username=username, password=encrypt_password, allow_login=True)
        except User.DoesNotExist:
            return self.set_response('user login failed', '用户登录失败', status=drf_status.HTTP_400_BAD_REQUEST)
        token = encryption.get_md5(f'{username}-{encrypt_password}-{now.strftime(params.DATETIME_STANDARD)}')
        UserToken.objects.update_or_create(user=user, defaults={
            'token': token,
            'is_expired': False,
            'login_time': now,
        })
        request.session[params.SESSION_TOKEN_KEY] = token
        request.session[params.SESSION_USER_KEY] = {
            'username': user.username
        }
        extra = {
            'redirect': reverse('dashboard-page'),
            'token': token,
            'username': f'{user.username}({user.real_name})',
        }
        return self.set_response(result='success', data='登录成功', extra=extra)


class AuthPublicKeyView(BasicInfoViewSet):
    """RSA的public-key 接口"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer
    authentication_enable = False

    def get(self, request, *args, **kwargs):
        """获取资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        public_key, private_key = encryption.rsa_generate()
        data = {'public_key': public_key}
        request.session[params.RSA_SESSION_PRIVATE_KEY] = private_key
        return Response(data=data, content_type=params.JSON_CONTENT_TYPE)


class LogoutView(BasicInfoViewSet):
    """退出当前用户的登录"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer

    def get(self, request, *args, **kwargs):
        """退出登录

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        token = request.session.get(params.SESSION_TOKEN_KEY)
        token_obj = UserToken.objects.filter(token=token)

        token_obj.update(is_expired=True)  # 更新token实例，使其过期

        del request.session[params.SESSION_TOKEN_KEY]
        del request.session[params.SESSION_USER_KEY]
        return self.set_response('Success', '退出成功')
