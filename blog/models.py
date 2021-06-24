# -*- coding: utf-8 -*-
"""
时间: 2021/2/26 10:26

作者: Fengchunyang

Blog: https://www.fengchunyang.com

更改记录:
    2021/2/26 新增文件。

重要说明:
"""
from django.db import models
from django.urls import reverse

from blog import params
from blog.auth.models import User
from common.models import BasicModel, CommonDataModel


class ArticleClassify(CommonDataModel):
    """博客文章分类表,用于表示博客内容的具体分类"""
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
    # classify = models.ForeignKey("ArticleClassify", verbose_name="系列分类", on_delete=models.SET_NULL,
    #                              null=True, related_name='serial')
    # tags = models.ManyToManyField("ArticleTag", verbose_name="系列标签", related_name='serial')

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

    def get_absolute_url(self):
        """返回文章的绝对路径

        Returns:
            abs_url(str): 文章的绝对路径
        """
        return reverse('article-detail-page', kwargs={'pk': self.id})

    class Meta:
        db_table = "blog_article"
        verbose_name = "博客文章表"
        ordering = ('-is_top', '-id')  # 置顶排序操作


class ProjectInCharge(BasicModel):
    """项目/业务责任人记录表"""
    name = models.CharField(verbose_name="责任人", max_length=255)
    identity = models.CharField(verbose_name="唯一性证明", max_length=255, unique=True)
    phone = models.CharField(verbose_name="联系方式", max_length=16, blank=True, null=True)
    email = models.CharField(verbose_name="电子邮箱", max_length=255, blank=True, null=True)
    remark = models.CharField(verbose_name="备注说明", max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'fapd_project_in_charge'
        verbose_name = '项目责任人记录表'


class ProjectInfo(CommonDataModel):
    """项目/业务信息记录表"""
    name = models.CharField(verbose_name="项目名称", max_length=255, unique=True)
    stime = models.DateField(verbose_name="项目开始时间")
    etime = models.DateField(verbose_name="项目结束时间")
    dtime = models.DateField(verbose_name="项目完成时间", blank=True, null=True)
    status = models.CharField(verbose_name="项目状态", choices=params.PROJECT_STATUS_CHOICE, max_length=16,
                              default=params.PROJECT_STATUS_START)

    class Meta:
        ordering = ('-id',)
        db_table = 'fapd_project_info'
        verbose_name = '项目信息表'


class ProjectPlanTask(CommonDataModel):
    """项目计划任务记录表"""
    project = models.ForeignKey('ProjectInfo', verbose_name="关联项目", on_delete=models.CASCADE,
                                related_name='plan_task', help_text='关联项目')
    name = models.CharField(verbose_name="任务名称", max_length=255)
    status = models.CharField(verbose_name="任务状态", choices=params.TASK_STATUS_CHOICE, max_length=16,
                              default=params.TASK_STATUS_PLAN, help_text="任务当前的状态")
    dtime = models.DateTimeField(verbose_name="任务完成时间", blank=True, null=True)
    remark = models.TextField(verbose_name="备注说明", blank=True, null=True)
    priority = models.IntegerField(verbose_name='优先级', choices=params.TASK_PRIORITY_CHOICE,
                                   default=params.TASK_PRIORITY_3)

    class Meta:
        ordering = ('-id', )
        db_table = 'fapd_project_plan_task'
        verbose_name = '项目计划任务表'


class AccessRecord(models.Model):
    """访问记录表"""
    path = models.CharField(verbose_name="目标地址", max_length=256, help_text='访问对象请求的目标地址')
    atime = models.DateTimeField(verbose_name="访问时间")
    user_agent = models.CharField(verbose_name="Agent属性", max_length=256, help_text='访问对象的user_agent')
    address = models.CharField(verbose_name="IP地址", max_length=256, help_text='访问对象的ip地址')
    query_str = models.CharField(verbose_name="查询字符串", max_length=256, blank=True, null=True)
    referer = models.CharField(verbose_name="上一个页面", max_length=256, blank=True, null=True)
    source = models.CharField(verbose_name="地址来源", max_length=128, blank=True, null=True)
    spider = models.CharField(verbose_name="爬虫类型", max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('-id', )
        db_table = 'blog_access_record'
        verbose_name = '访问记录表'


class SubscribeRecord(BasicModel):
    """订阅记录表"""
    name = models.CharField(verbose_name="用户名", max_length=32)
    email = models.CharField(verbose_name="电子邮箱", unique=True, max_length=64)
    enable = models.BooleanField(verbose_name="是否启用", default=True)

    class Meta:
        ordering = ('-id', )
        db_table = 'blog_subscribe_record'
        verbose_name = '订阅记录表'


class InnerMessage(BasicModel):
    """私信消息"""
    name = models.CharField(verbose_name="私信用户名", max_length=32)
    email = models.CharField(verbose_name="电子邮箱", max_length=32)
    message = models.TextField(verbose_name="私信消息")
    is_reply = models.BooleanField(verbose_name="是否回复", default=False)

    class Meta:
        ordering = ('-id', )
        db_table = 'blog_inner_message'
        verbose_name = '私信消息表'


class FriendlyLink(BasicModel):
    """友链申请表"""
    site = models.CharField(verbose_name="网站地址", max_length=256, unique=True)
    logo = models.CharField(verbose_name="网站Logo地址", max_length=256, blank=True, null=True)
    name = models.CharField(verbose_name="网站名称", max_length=256)
    enable = models.BooleanField(verbose_name="是否同意申请", default=False)
    link = models.CharField(verbose_name="挂载本站的地址", max_length=256)

    class Meta:
        ordering = ('-id', )
        db_table = 'blog_friendly_link'
        verbose_name = '友链申请表'
