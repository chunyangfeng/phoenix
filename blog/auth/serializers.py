# -*- coding: utf-8 -*-
"""序列化器
时间: 2021/3/26 9:47

作者: Fengchunyang

Blog: https://www.fengchunyang.com

更改记录:
    2021/3/26 新增文件。

重要说明:
"""
from rest_framework import serializers

from blog.auth.models import User


class UserInfoSerializer(serializers.ModelSerializer):
    """用户信息序列化器"""

    class Meta:
        model = User
        fields = "__all__"


class UserListSerializer(serializers.ModelSerializer):
    """用户列表序列化器"""

    class Meta:
        model = User
        fields = "__all__"
