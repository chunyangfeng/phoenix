# -*- coding: utf-8 -*-
"""
时间: 2020/11/23 11:05

作者: Fengchunyang

更改记录:
    2020/11/23 新增文件。

重要说明:
"""
import datetime

from django.db import models


class BasicModel(models.Model):
    """抽象基类"""
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    desc = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)
    ctime = models.DateTimeField(verbose_name="创建时间", auto_now_add=datetime.datetime.now())
    mtime = models.DateTimeField(verbose_name="修改时间", auto_now=datetime.datetime.now())

    class Meta:
        abstract = True


class BasicModelManager(models.Manager):
    """通用模型管理器"""
    def get_queryset(self):
        """显示定义默认管理器行为，在models.objects的基础上，扩展额外的行为

        Returns:
            QuerySet: 结果集
        """
        return super().get_queryset()


class CommonDataModel(BasicModel):
    """通用数据类抽象model"""
    creator = models.CharField(verbose_name="创建者", max_length=64, blank=True, null=True)
    owner = models.CharField(verbose_name="拥有者", max_length=64, blank=True, null=True)

    class Meta:
        abstract = True


class MigrationsHistory(BasicModel):
    app_name = models.CharField(verbose_name="app名称", max_length=256)
    file_name = models.CharField(verbose_name="文件名称", max_length=256)
    file_content = models.TextField(verbose_name="文件内容")

    class Meta:
        db_table = 'common_migrations_history'
        verbose_name = "迁移文件备份表"


class SystemParameter(BasicModel):
    """系统参数"""
    name = models.CharField(verbose_name='参数名称', max_length=64, unique=True)
    value = models.CharField(verbose_name='参数值', max_length=128, unique=True)
    code = models.CharField(verbose_name='参数编码', max_length=32, unique=True)
    is_builtin = models.BooleanField(verbose_name='是否内置', default=False)

    class Meta:
        db_table = 'common_system_parameter'
        verbose_name = '系统参数表'


class SystemLogRecord(BasicModel):
    """系统日志记录"""
    pass
