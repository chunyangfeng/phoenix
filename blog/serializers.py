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


class ArticleSerialSerializer(serializers.ModelSerializer):
    """博客文章系列序列化器"""
    classify = serializers.CharField(source='classify.name', read_only=True)
    tags = ArticleTagSerializer(many=True)

    class Meta:
        model = models.ArticleSerial
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    """博客文章序列化器"""
    classify = serializers.CharField(source='classify.name', read_only=True)
    tags = ArticleTagSerializer(many=True, read_only=True)
    tags_id = serializers.ListField(write_only=True, required=False)
    classify_id = serializers.CharField(write_only=True, required=False)
    serial_id = serializers.CharField(write_only=True, required=False)

    def create(self, validated_data):
        """重载create，处理多对多关系

        Args:
            validated_data(dict): 有效数据

        Returns:
            instance(models.Model): 实例
        """
        tags_id = validated_data.pop('tags_id')
        instance = self.Meta.model.objects.create(**validated_data)
        instance.tags.set(tags_id)
        return instance


    class Meta:
        model = models.Article
        fields = '__all__'
