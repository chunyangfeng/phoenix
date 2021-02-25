# -*- coding: utf-8 -*-
"""序列化器抽象基类
Date: 2021/1/29 13:57

Author: phoenix@fengchunyang.com

Record:
    2021/1/29 新增文件。

Site: http://www.fengchunyang.com
"""
from rest_framework import serializers


class SerializerDataCache:
    """序列化器数据缓存，用于缓存查询的数据"""
    _cache = dict()

    @property
    def cache(self):
        return self._cache

    @cache.setter
    def cache(self, data):
        self._cache = data


class DoNothingSerializer(serializers.ModelSerializer):
    """什么都不做的序列化器，用于部分不需要序列化数据的接口"""
    pass


