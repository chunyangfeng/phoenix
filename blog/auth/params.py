# -*- coding: utf-8 -*-
"""认证授权参数层
时间: 2021/3/26 9:32

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/26 新增文件。

重要说明:
"""
# 权限相关
PERMISSION_VIEW = 'view'
PERMISSION_CREATE = 'create'
PERMISSION_MODIFY = 'modify'
PERMISSION_DELETE = 'delete'
PERMISSION_APPROVE = 'approve'
PERMISSION_PAGE = 'page'

PERMISSION_ALLOW_OWNER = 'owner'
PERMISSION_ALLOW_GROUP = 'group'
PERMISSION_ALLOW_ALL = 'all'

PERMISSION_ALLOW_CHOICE = (
    (PERMISSION_ALLOW_ALL, '全部'),
    (PERMISSION_ALLOW_GROUP, '组成员'),
    (PERMISSION_ALLOW_OWNER, '拥有者'),
)

PERMISSION_CHOICE = (
    (PERMISSION_VIEW, "查看"),
    (PERMISSION_CREATE, "创建"),
    (PERMISSION_MODIFY, "修改"),
    (PERMISSION_DELETE, "删除"),
    (PERMISSION_APPROVE, "审核"),
    (PERMISSION_PAGE, "页面"),
)
