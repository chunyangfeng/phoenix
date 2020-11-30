# -*- coding: utf-8 -*-
"""通用模型
时间: 2020/11/26 17:39

Blog: www.fengchunyang.com

更改记录:
    2020/11/26 新增文件。

重要说明:
"""
from django.db import models

from common.models.basic import BasicModel
from common.params import params


class CommonModel(BasicModel):

    class Meta:
        ordering = ('-id', )


class Permission(models.Model):
    """权限模型"""
    code = models.CharField(verbose_name="权限编码", max_length=64, unique=True)
    name = models.CharField(verbose_name="权限名称", max_length=128, unique=True)
    desc = models.CharField(verbose_name="权限描述", max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'common_permission'
        verbose_name = '权限表'
        ordering = ('-id', )


class PermissionAction(models.Model):
    """权限动作模型"""
    permission = models.ForeignKey('Permission', verbose_name="所属权限", on_delete=models.CASCADE)
    classification = models.CharField(verbose_name="权限动作分类", choices=params.PERMISSION_ACTION_CHOICE, max_length=32)
    desc = models.CharField(verbose_name="权限动作描述", max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'common_permission_action'
        verbose_name = '权限动作表'
        ordering = ('-id', )





