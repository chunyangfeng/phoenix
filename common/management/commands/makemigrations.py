#!/usr/bin/env python
# coding:utf-8
# Author:Fengchunyang
# Date:2021/2/7 10:43
import importlib

from django.core.management.commands.makemigrations import Command as MakemigrationsCommand


class Command(MakemigrationsCommand):
    """重载django的makemigrations命令，增加自定义操作"""

    def add_arguments(self, parser):
        """重载参数设置，添加自定义参数

        Args:
            parser(ArgumentParser): 参数注册器实例
        """
        super(Command, self).add_arguments(parser)

        # 当需要载入历史迁移文件时，指定--load参数
        parser.add_argument(
            '--load', action='store_true', dest='load',
            help='执行makemigrations命令之前，从数据库中加载历史迁移记录',
        )

    def handle(self, *args, **options):
        """命令处理流程

        Args:
            *args(list): 可变参数
            **options(dict): 可变关键字参数
        """
        # 执行migrations文件同步，从关联的数据库中将保存的migrations文件读取到本地项目中
        load = options['load']
        if load:
            command = importlib.import_module('common.mgt.commands.syncmigrate')
            self.stdout.write("开始读取迁移文件......")
            sync_cmd = getattr(command, 'Command')
            sync = sync_cmd()
            sync.load()
            self.stdout.write("迁移文件读取完成......")

        super(Command, self).handle(*args, **options)







