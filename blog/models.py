# -*- coding: utf-8 -*-
"""
时间: 2021/2/26 10:26

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/26 新增文件。

重要说明:
"""
from django.db import models

from common.models.models import CommonDataModel, User


class ArticleClassify(CommonDataModel):
    """博客文章分类表,用于表示博客内容的具体分类，比如python、mysql、ansible等"""
    name = models.CharField(verbose_name="分类名称", max_length=50, unique=True)

    class Meta:
        db_table = "blog_classify"
        verbose_name = "博客分类表"

    def __str__(self):
        return self.name


class ArticleTag(CommonDataModel):
    """博客文章标签表，用于标记文章内容涉及到的主要知识"""
    name = models.CharField(verbose_name="标签名称", max_length=50, unique=True)

    class Meta:
        db_table = "blog_tag"
        verbose_name = "博客标签表"

    def __str__(self):
        return self.name


class Article(CommonDataModel):
    """博客文章表，存储markdown格式内容"""
    title = models.CharField(verbose_name="文章标题", max_length=100, unique=True)
    classify = models.ForeignKey("ArticleClassify", verbose_name="博客分类", on_delete=models.SET_NULL,
                                 null=True, related_name='article')
    tags = models.ManyToManyField("ArticleTag", verbose_name="博客标签", related_name='article')
    desc = models.TextField(verbose_name="内容简介")
    content = models.TextField(verbose_name="文章正文")
    creator = models.CharField(verbose_name="作者", max_length=64)
    is_publish = models.BooleanField(verbose_name="是否发表", default=False)
    read_count = models.IntegerField(verbose_name="阅读量", default=0)
    like_count = models.IntegerField(verbose_name="点赞数", default=0)
    is_top = models.BooleanField(verbose_name="是否置顶", default=False)
    etime = models.DateTimeField(verbose_name="编辑时间", blank=True, null=True)

    class Meta:
        db_table = "blog_article"
        verbose_name = "博客文章表"
        ordering = ['-ctime', ]

