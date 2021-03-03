# -*- coding: utf-8 -*-
"""博客序列化器
时间: 2021/2/26 11:31

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/26 新增文件。

重要说明:
"""
from django.urls import reverse
from rest_framework import serializers

from blog import models
from blog.adapt import adapt_get_user_info
from common.params import params


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
    serial = serializers.SerializerMethodField(read_only=True)
    tags = ArticleTagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)

    tags_id = serializers.ListField(write_only=True, required=False)
    classify_id = serializers.CharField(required=False)
    serial_id = serializers.CharField(required=False)

    @staticmethod
    def get_serial(obj):
        """获取serial name

        Args:
            obj(models.Article): 数据实例

        Returns:
            name(str): serial name
        """
        return obj.serial or ''

    def get_comment_count(self, obj):
        """获取评论数

        Args:
            obj(models.Article): 数据实例

        Returns:
            count(int): 评论数
        """
        return 0

    @staticmethod
    def get_creator(obj):
        """获取文章作者真实姓名

        Args:
            obj(models.Article): 数据实例

        Returns:
            rel_name(str): 文章作者
        """
        user_info = adapt_get_user_info(True, username=obj.creator)
        return user_info.get('real_name', obj.creator)

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

    def update(self, instance, validated_data):
        """重载update，处理多对多关系

        Args:
            instance(models.Article): 数据实例
            validated_data(dict): 有效数据

        Returns:
            instance(models.Article): 数据实例
        """
        tags_id = validated_data.pop('tags_id')
        instance = super().update(instance, validated_data)

        # 清空多对多关系，并重新赋值
        instance.tags.clear()
        instance.tags.set(tags_id)
        return instance

    class Meta:
        model = models.Article
        fields = '__all__'


class ArticleDetailSerializer(serializers.ModelSerializer):
    """文章详情序列化器"""
    classify_name = serializers.CharField(source="classify.name", read_only=True)
    word_count = serializers.SerializerMethodField(read_only=True)
    link = serializers.SerializerMethodField(read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)
    relate = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def _get_url(pk, url_name='article-detail-page'):
        """获取指定主键对应的url

        Args:
            url_name(str): url配置的name值
            pk(int): 主键值

        Returns:
            data(dict): {title: '', link: ''}
        """
        url = reverse(url_name, kwargs={params.MODEL_UNIQUE_KEY: pk})
        link = f'{params.SYSTEM_DOMAIN}{url}'
        return link

    @staticmethod
    def get_word_count(obj):
        """获取文章字数

        Args:
            obj(models.Article): 数据实例

        Returns:
            word_count(int): 文章字数
        """
        return len(obj.content)

    def get_link(self, obj):
        """获取文章链接

        Args:
            obj(models.Article): 数据实例

        Returns:
            link(str): 文章链接
        """
        return self._get_url(pk=obj.id)

    @staticmethod
    def get_creator(obj):
        """获取文章作者真实姓名

        Args:
            obj(models.Article): 数据实例

        Returns:
            rel_name(str): 文章作者
        """
        user_info = adapt_get_user_info(True, username=obj.creator)
        return user_info.get('real_name', obj.creator)

    def _get_relate_data(self, pk, previous=True, latest=False):
        """获取指定主键的关联数据

        Args:
            pk(int): 主键值
            previous(bool): 获取上一条
            latest(bool): 获取下一条

        Returns:
            data(dict): 数据结果
        """
        data = {
            "title": "没有了",
            "link": "#",
        }

        try:
            if previous and not latest:
                instance = self.Meta.model.objects.filter(id__lte=pk).order_by('-id').first()
            elif not previous and latest:
                instance = self.Meta.model.objects.filter(id__gt=pk).first()
            else:
                instance = None
            if instance:
                data['title'] = instance.title
                data['link'] = self._get_url(instance.id)
        except self.Meta.model.DoesNotExist:
            pass

        return data

    def get_relate(self, obj):
        """获取当前文章关联的文章信息

        Args:
            obj(models.Article): 数据实例

        Returns:
            relate(dict): 关联信息
        """
        data = {
            'previous': self._get_relate_data(obj.id-1, previous=True, latest=False),
            'latest': self._get_relate_data(obj.id+1, previous=False, latest=True),
        }
        return data

    class Meta:
        model = models.Article
        fields = '__all__'
