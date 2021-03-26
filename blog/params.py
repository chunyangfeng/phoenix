# -*- coding: utf-8 -*-
"""博客常量配置
时间: 2021/3/5 10:24

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/5 新增文件。

重要说明:
"""
# 状态相关
STATE_ENABLED = 'enabled'
STATE_DISABLED = 'disabled'
STATE_PUBLISHED = 'published'
STATE_EDITING = 'editing'
STATE_DELETED = 'deleted'

STATE_CHOICE = (
    (STATE_ENABLED, '已启用'),
    (STATE_DISABLED, '已禁用'),
    (STATE_PUBLISHED, '已发布'),
    (STATE_EDITING, '编辑中'),
    (STATE_DELETED, '已删除'),
)

# 项目状态配置
PROJECT_STATUS_START = 'start'
PROJECT_STATUS_PLAN = 'plan'
PROJECT_STATUS_EXECUTE = 'execute'
PROJECT_STATUS_OBSERVE = 'observe'
PROJECT_STATUS_ACCEPTANCE = 'acceptance'
PROJECT_STATUS_END = 'end'

PROJECT_STATUS_CHOICE = (
    (PROJECT_STATUS_START, '已启动'),
    (PROJECT_STATUS_PLAN, '规划中'),
    (PROJECT_STATUS_EXECUTE, '执行中'),
    (PROJECT_STATUS_OBSERVE, '监控中'),
    (PROJECT_STATUS_ACCEPTANCE, '已验收'),
    (PROJECT_STATUS_END, '已结束'),
)

# 项目下的任务的状态
TASK_STATUS_PLAN = 'plan'
TASK_STATUS_WIP = 'wip'
TASK_STATUS_DISCARD = 'discard'
TASK_STATUS_DONE = 'done'

TASK_STATUS_CHOICE = (
    (TASK_STATUS_PLAN, '计划中'),
    (TASK_STATUS_WIP, '进行中'),
    (TASK_STATUS_DISCARD, '已废弃'),
    (TASK_STATUS_DONE, '已完成'),
)

# 项目任务的优先级
TASK_PRIORITY_1 = 1
TASK_PRIORITY_2 = 2
TASK_PRIORITY_3 = 3

TASK_PRIORITY_CHOICE = (
    (TASK_PRIORITY_1, '紧急'),
    (TASK_PRIORITY_2, '重要'),
    (TASK_PRIORITY_3, '一般'),
)
