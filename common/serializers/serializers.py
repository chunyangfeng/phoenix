# -*- coding: utf-8 -*-
"""通用序列化器
时间: 2021/2/23 14:30

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/23 新增文件。

重要说明:
"""
from rest_framework import serializers
from common.models.models import User, UserToken


class UserTokenSerializer(serializers.ModelSerializer):
    """用户token序列化器"""

    class Meta:
        model = UserToken
        fields = "__all__"
