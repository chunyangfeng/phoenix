# -*- coding: utf-8 -*-
"""博客序列化器
时间: 2021/2/26 11:31

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/26 新增文件。

重要说明:
"""
from rest_framework import serializers

from blog import models


class ArticleSerializer(serializers.ModelSerializer):
    """博客文章序列化器"""
    classify = serializers.CharField(source='classify.name', read_only=True)

    class Meta:
        model = models.Article
        fields = '__all__'
