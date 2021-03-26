# -*- coding: utf-8 -*-
"""接口层
时间: 2021/3/26 9:47

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/26 新增文件。

重要说明:
"""
from .models import User
from .serializers import UserInfoSerializer


def get_user_info(simple=False, **kwargs):
    """获取用户数据

    Args:
        simple(bool): 是否展示详细数据，默认不展示
        **kwargs(dict): 查询关键字

    Returns:
        dict: 用户信息
    """
    try:
        instance = User.objects.get(**kwargs)
    except User.DoesNotExist:
        return dict()
    return UserInfoSerializer(instance, many=False).data
