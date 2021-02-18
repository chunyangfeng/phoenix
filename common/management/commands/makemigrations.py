#!/usr/bin/env python
# coding:utf-8
# Author:Fengchunyang
# Date:2021/2/7 10:43
from django.core.management.commands.makemigrations import Command as MakemigrationsCommand
from common.management.commands.syncmigrate import Command as SyncCommand


class Command(MakemigrationsCommand):
    """重载django的makemigrations命令，增加自定义操作"""

    def handle(self, *args, **options):
        # 执行migrations文件同步，从关联的数据库中将保存的migrations文件读取到本地项目中
        self.stdout.write("开始读取迁移文件......")
        sync = SyncCommand()
        sync.load()
        self.stdout.write("迁移文件读取完成......")

        super(Command, self).handle(*args, **options)





