# -*- coding: utf-8 -*-
"""
Date: 2021/1/27 14:53

Author: phoenix@fengchunyang.com

Record:
    2021/1/27 新增文件。

Site: http://www.fengchunyang.com
"""
from common.viewset.basic import BasicInfoViewSet, BasePageView
from common.models.models import User, UserToken


class UserLoginPageView(BasePageView):
    """用户登陆主页"""
    page = "auth/login.html"


class UserLoginView(BasicInfoViewSet):
    queryset = UserToken.objects.all()
    serializer_class = None

