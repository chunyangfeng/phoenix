# -*- coding: utf-8 -*-
"""
Date: 2021/1/27 14:53

Author: phoenix@fengchunyang.com

Record:
    2021/1/27 新增文件。

Site: http://www.fengchunyang.com
"""
from common.viewset.basic import BasicInfoViewSet
from common.models.models import User, UserToken


class UserLoginView(BasicInfoViewSet):
    queryset = UserToken.objects.all()
    serializer_class = None

