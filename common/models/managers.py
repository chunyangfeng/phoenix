# -*- coding: utf-8 -*-
"""model管理器
时间: 2021/3/9 15:26

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/9 新增文件。

重要说明:
"""
import datetime

from django.db import models

from common.models.base import BasicModelManager
from common.params.params import LOGIN_EXPIRE_HOUR


class UserTokenManager(BasicModelManager):
    """用户token管理器"""
    @staticmethod
    def _validate_expire(queryset):
        """校验过期状态

        Args:
            queryset(QuerySet): 查询结果集

        Returns:
            QuerySet: 处理后的结果集
        """
        now = datetime.datetime.now()
        expire = now - datetime.timedelta(hours=LOGIN_EXPIRE_HOUR)
        queryset.filter(login_time__lt=expire).update(is_expired=True)
        return queryset

    def get_queryset(self):
        """查询结果集之前进行登陆过期的校验

        Returns:
            QuerySet: 处理后的结果集
        """
        queryset = super().get_queryset()
        self._validate_expire(queryset)
        return queryset
