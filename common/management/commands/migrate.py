#!/usr/bin/env python
# coding:utf-8
# Author:Fengchunyang
# Date:2021/2/7 10:43
from django.core.management.commands.migrate import Command as MigrateCommand
from common.management.commands.syncmigrate import Command as SyncCommand


class Command(MigrateCommand):
    """重载django的migrate命令，增加自定义操作"""

    def handle(self, *args, **options):
        # 执行migrations文件同步，将本地生成的迁移文件保存到关联的数据库中
        self.stdout.write("开始同步迁移文件......")
        sync = SyncCommand()
        sync.save()
        self.stdout.write("迁移文件同步完成......")

        super(Command, self).handle(*args, **options)





