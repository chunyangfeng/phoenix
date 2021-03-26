# -*- coding: utf-8 -*-
"""初始化项目数据
时间: 2021/1/4 23:18

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/1/4 新增文件。

重要说明:
"""
from django.core.management import BaseCommand

from common.models import models
from common.utils.formatter import output_formatter
from common import params, permissions

from common.management.initial_data.users import BUILTIN_USER


class InitialCommandMixin:
    """初始化命令混合类"""

    def create_resource(self):
        """初始化资源数据"""
        for key, value in permissions.RES_PERM.items():
            resource, _ = models.Resource.objects.update_or_create(code=key, defaults={
                "name": value,
                "desc": value,
            })
            self.create_permission(resource)
        print(output_formatter("资源数据初始化完成"))

    @staticmethod
    def create_permission(resource):
        """初始化权限

        Args:
            resource(models.Resource): 资源实例
        """
        for key, value in params.PERMISSION_CHOICE:
            models.Permission.objects.update_or_create(resource=resource, classification=key, defaults={
                "desc": f'{resource.name}-{value}'
            })
        print(output_formatter("权限数据初始化完成"))

    @staticmethod
    def create_role():
        """初始化角色"""
        print(output_formatter("角色数据初始化完成"))

    @staticmethod
    def create_user_group():
        """初始化用户组"""
        print(output_formatter("用户组数据初始化完成"))

    @staticmethod
    def create_builtin_user():
        """初始化内置用户"""
        for username, data in BUILTIN_USER.items():
            models.User.objects.get_or_create(username=username, defaults=data)

        print(output_formatter("内置用户初始化完成"))

    def run(self):
        """执行函数入口
        """
        self.create_resource()
        self.create_role()
        self.create_user_group()
        self.create_builtin_user()


class Command(BaseCommand, InitialCommandMixin):
    """项目全局初始化命令"""

    def add_arguments(self, parser):
        """参数管理
        Args:
            parser(parser.Parser): 参数管理器
        """
        parser.add_argument(
            '--start',
            type=str,
            help="初始化全局基础数据",
        )

    def handle(self, *args, **options):
        """命令处理
        Args:
            *args(list): 可变参数
            **options: 可变关键字参数
        """
        self.run()
