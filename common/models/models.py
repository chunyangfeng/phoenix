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


class Resource(models.Model):
    """资源模型"""
    code = models.CharField(verbose_name="资源编码", max_length=64, unique=True)
    name = models.CharField(verbose_name="资源名称", max_length=128, unique=True)
    desc = models.CharField(verbose_name="资源描述", max_length=256, null=True, blank=True)
    allowed = models.CharField(verbose_name="允许访问范围", choices=params.PERMISSION_ALLOW_CHOICE,
                               default=params.PERMISSION_ALLOW_ALL)

    class Meta:
        db_table = 'common_resource'
        verbose_name = '资源表'
        ordering = ('-id', )


class Permission(models.Model):
    """权限模型"""
    permission = models.ForeignKey('Resource', verbose_name="所属资源", on_delete=models.CASCADE)
    classification = models.CharField(verbose_name="权限类型", choices=params.PERMISSION_CHOICE, max_length=32)
    desc = models.CharField(verbose_name="权限描述", max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'common_permission'
        verbose_name = '权限表'
        ordering = ('-id', )


class Role(models.Model):
    """角色模型"""
    name = models.CharField(verbose_name="角色名称", max_length=64, unique=True)
    desc = models.CharField(verbose_name="角色描述", max_length=256, blank=True, null=True)
    resource = models.ManyToManyField('Resource', verbose_name='关联资源', related_name='role')
    state = models.CharField(verbose_name="角色状态", choices=params.STATE_CHOICE, default=params.STATE_ENABLED)
    is_default = models.BooleanField(verbose_name="是否为内置角色", default=False)
    is_test = models.BooleanField(verbose_name="是否为测试角色", default=False)

    class Meta:
        db_table = 'common_role'
        verbose_name = '角色表'
        ordering = ('-id', )


class Department(models.Model):
    """部门模型"""
    parent = models.ForeignKey('Department', verbose_name="父级部门", blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(verbose_name="部门名称", max_length=128)
    code = models.CharField(verbose_name="部门编码", max_length=64, blank=True, null=True)
    level = models.SmallIntegerField(verbose_name="部门层级", default=0)
    desc = models.CharField(verbose_name="部门描述", max_length=256, blank=True, null=True)
    leader = models.ForeignKey('User', verbose_name="部门负责人", blank=True, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'common_department'
        verbose_name = '部门表'


class User(models.Model):
    """用户模型"""
    username = models.CharField(verbose_name="用户名", max_length=64, unique=True)
    real_name = models.CharField(verbose_name="真实姓名", max_length=64, blank=True, null=True)






