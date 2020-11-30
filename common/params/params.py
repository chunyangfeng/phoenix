# -*- coding: utf-8 -*-
"""全局常量配置
时间: 2020/11/23 11:10

作者: fengchunyang@cyai.com

更改记录:
    2020/11/23 新增文件。

重要说明:
"""

# 权限动作
PERMISSION_VIEW = 'view'
PERMISSION_CREATE = 'create'
PERMISSION_MODIFY = 'modify'
PERMISSION_DELETE = 'delete'
PERMISSION_APPROVE = 'approve'
PERMISSION_PAGE = 'page'

PERMISSION_ACTION_CHOICE = (
    (PERMISSION_VIEW, "查看"),
    (PERMISSION_CREATE, "创建"),
    (PERMISSION_MODIFY, "修改"),
    (PERMISSION_DELETE, "删除"),
    (PERMISSION_APPROVE, "审核"),
    (PERMISSION_PAGE, "页面"),
)


