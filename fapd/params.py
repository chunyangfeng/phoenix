# -*- coding: utf-8 -*-
"""项目管理常量配置
时间: 2021/3/2 18:44

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/2 新增文件。

重要说明:
"""

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
