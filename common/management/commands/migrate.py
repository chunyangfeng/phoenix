#!/usr/bin/env python
# coding:utf-8
# Author:Fengchunyang
# Date:2021/2/7 10:43
import importlib

from django.core.management.commands.migrate import Command as MigrateCommand


class Command(MigrateCommand):
    """重载django的migrate命令，增加自定义操作"""

    def handle(self, *args, **options):
        super(Command, self).handle(*args, **options)

        # 执行migrations文件同步，将本地生成的迁移文件保存到关联的数据库中
        command = importlib.import_module('common.mgt.commands.syncmigrate')
        self.stdout.write("开始同步迁移文件......")
        sync_cmd = getattr(command, 'Command')
        sync = sync_cmd()
        sync.save()
        self.stdout.write("迁移文件同步完成......")





