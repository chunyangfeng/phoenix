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


class ArticleSerial(CommonDataModel):
    """博客文章系列集合"""
    name = models.CharField(verbose_name="系列名称", max_length=255, unique=True)
    classify = models.ForeignKey("ArticleClassify", verbose_name="系列分类", on_delete=models.SET_NULL,
                                 null=True, related_name='serial')
    tags = models.ManyToManyField("ArticleTag", verbose_name="系列标签", related_name='serial')

    class Meta:
        db_table = "blog_article_serial"
        verbose_name = "博客文章系列表"


class Article(CommonDataModel):
    """博客文章表，存储markdown格式内容"""
    title = models.CharField(verbose_name="文章标题", max_length=100, unique=True)
    classify = models.ForeignKey("ArticleClassify", verbose_name="博客分类", on_delete=models.SET_NULL,
                                 null=True, related_name='article')
    tags = models.ManyToManyField("ArticleTag", verbose_name="博客标签", related_name='article')
    serial = models.ForeignKey("ArticleSerial", verbose_name="所属系列", blank=True, null=True,
                               on_delete=models.SET_NULL, related_name="article")
    desc = models.TextField(verbose_name="内容简介")
    content = models.TextField(verbose_name="文章正文", help_text="markdown格式的正文内容")
    creator = models.CharField(verbose_name="作者", max_length=64)
    is_publish = models.BooleanField(verbose_name="是否发表", default=False)
    read_count = models.IntegerField(verbose_name="阅读量", default=0)
    like_count = models.IntegerField(verbose_name="点赞数", default=0)
    is_top = models.BooleanField(verbose_name="是否置顶", default=False)
    etime = models.DateTimeField(verbose_name="编辑时间", blank=True, null=True)
    html_content = models.TextField(verbose_name="html正文", blank=True, null=True,
                                    help_text="由content转化为html格式的正文内容")
    ptime = models.DateTimeField(verbose_name="发表时间", blank=True, null=True)

    def save(self, *args, **kwargs):
        """重载父类的save方法，设置初始创建时的编辑时间

        Args:
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数
        """
        if not self.etime:
            self.etime = self.ctime

        super().save(*args, **kwargs)

    class Meta:
        db_table = "blog_article"
        verbose_name = "博客文章表"
        ordering = ('-id', )

