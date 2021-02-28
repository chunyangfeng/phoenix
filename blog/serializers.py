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


class ArticleClassifySerializer(serializers.ModelSerializer):
    """博客文章分类序列化器"""

    class Meta:
        model = models.ArticleClassify
        fields = '__all__'


class ArticleTagSerializer(serializers.ModelSerializer):
    """博客文章标签序列化器"""

    class Meta:
        model = models.ArticleTag
        fields = '__all__'
