# -*- coding: utf-8 -*-
"""认证授权模型层
时间: 2021/3/26 9:21

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/26 新增文件。

重要说明:
"""
from django.db import models

from blog.auth import params
from blog.params import STATE_CHOICE, STATE_ENABLED
from common.models import BasicModel, CommonDataModel
from common.utils import sington


class Resource(BasicModel):
    """资源模型"""
    code = models.CharField(verbose_name="资源编码", max_length=64, unique=True)
    name = models.CharField(verbose_name="资源名称", max_length=128, unique=True)
    desc = models.CharField(verbose_name="资源描述", max_length=256, null=True, blank=True)
    allowed = models.CharField(verbose_name="允许访问范围", choices=params.PERMISSION_ALLOW_CHOICE,
                               default=params.PERMISSION_ALLOW_ALL, max_length=64)
    url_name = models.CharField(verbose_name="url name", max_length=128, unique=True, blank=True, null=True,
                                help_text="资源访问的url名称，在urls.py中配置")

    class Meta:
        db_table = 'common_resource'
        verbose_name = '资源表'
        ordering = ('-id', )


class Permission(BasicModel):
    """权限模型"""
    resource = models.ForeignKey('Resource', verbose_name="所属资源", on_delete=models.CASCADE)
    classification = models.CharField(verbose_name="权限类型", choices=params.PERMISSION_CHOICE, max_length=32)
    desc = models.CharField(verbose_name="权限描述", max_length=256, null=True, blank=True)

    class Meta:
        db_table = 'common_permission'
        verbose_name = '权限表'
        ordering = ('-id', )


class Role(CommonDataModel):
    """角色模型"""
    name = models.CharField(verbose_name="角色名称", max_length=64, unique=True)
    desc = models.CharField(verbose_name="角色描述", max_length=256, blank=True, null=True)
    resource = models.ManyToManyField('Resource', verbose_name='关联资源', related_name='role')
    state = models.CharField(verbose_name="角色状态", choices=STATE_CHOICE,
                             default=STATE_ENABLED, max_length=32)
    is_default = models.BooleanField(verbose_name="是否为内置角色", default=False)
    is_test = models.BooleanField(verbose_name="是否为测试角色", default=False)

    class Meta:
        db_table = 'common_role'
        verbose_name = '角色表'
        ordering = ('-id', )


class UserGroup(CommonDataModel):
    name = models.CharField(verbose_name="用户组名", max_length=32, unique=True)
    users = models.ManyToManyField('User', verbose_name="用户")
    role = models.ForeignKey('Role', verbose_name="角色", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = 'common_user_group'
        verbose_name = '用户组表'


class User(CommonDataModel):
    """用户模型"""
    username = models.CharField(verbose_name="用户名", max_length=64, unique=True)
    real_name = models.CharField(verbose_name="真实姓名", max_length=64, blank=True, null=True)
    password = models.CharField(verbose_name="密码", max_length=64)
    wechat = models.CharField(verbose_name="微信号", max_length=255, blank=True, null=True)
    email = models.CharField(verbose_name="邮箱地址", max_length=64)
    phone = models.CharField(verbose_name="移动电话", max_length=11, blank=True, null=True)
    site = models.CharField(verbose_name="关联站点", max_length=256, blank=True, null=True)
    allow_login = models.BooleanField(verbose_name='是否允许登陆', default=False)
    is_builtin = models.BooleanField(verbose_name="是否为内置用户", default=False)

    def save(self, *args, **kwargs):
        """重载父类的save方法，当用户被创建时，自动加密密码

        Args:
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数
        """
        # 前端创建用户时，限制了密码长度最长为16位，AES加密后的密码长度为64位，以此判断密码是否已经被加密
        if len(self.password) != 64:
            self.password = sington.aes.encrypt(self.password)

        super().save(*args, **kwargs)

    class Meta:
        db_table = 'common_user'
        verbose_name = '用户表'


class UserToken(BasicModel):
    """用户认证token表"""
    user = models.OneToOneField('User', verbose_name="关联用户", related_name='token', on_delete=models.CASCADE,
                                help_text="token所属的用户，当用户登录成功后会创建或更新此数据")
    token = models.CharField(verbose_name='token值', max_length=64,
                             help_text="用户登录成功后生成的token值，用于发起http请求时，进行身份认证的标识")
    is_expired = models.BooleanField(verbose_name="是否过期", default=True,
                                     help_text="token是否过期的标识，过期的token会被认证系统认为是无效的")
    login_time = models.DateTimeField(verbose_name="登录时间", help_text="用户登录的时间，用于判断当前token是否过期")

    # objects = UserTokenManager()

    class Meta:
        db_table = 'common_user_token'
        verbose_name = '用户Token表'
