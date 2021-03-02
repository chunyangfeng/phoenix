# -*- coding: utf-8 -*-
"""开发流程与进度模型集
时间: 2021/3/2 18:27

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/2 新增文件。

重要说明:
"""
from django.db import models

from common.models.models import CommonDataModel
from common.models.base import BasicModel

from . import params


class ProjectInCharge(BasicModel):
    """项目/业务责任人记录表"""
    name = models.CharField(verbose_name="责任人", max_length=255)
    identity = models.CharField(verbose_name="唯一性证明", max_length=255, unique=True)
    phone = models.CharField(verbose_name="联系方式", max_length=16, blank=True, null=True)
    email = models.CharField(verbose_name="电子邮箱", max_length=255, blank=True, null=True)
    remark = models.CharField(verbose_name="备注说明", max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'fapd_project_in_charge'
        verbose_name = '项目责任人记录表'


class ProjectInfo(CommonDataModel):
    """项目/业务信息记录表"""
    project = models.ForeignKey('ProjectInfo', on_delete=models.CASCADE, related_name='sub_project', blank=True,
                                null=True, help_text='自关联，如果关联有外键，则当前实例为子项目')
    name = models.CharField(verbose_name="项目名称", max_length=255, unique=True)
    in_charge = models.ManyToManyField('ProjectInCharge', verbose_name="责任人")
    stime = models.DateTimeField(verbose_name="项目开始时间")
    etime = models.DateTimeField(verbose_name="项目结束时间")
    dtime = models.DateTimeField(verbose_name="项目完成时间", blank=True, null=True)
    budget = models.BigIntegerField(verbose_name="项目预算", default=0)
    status = models.CharField(verbose_name="项目状态", choices=params.PROJECT_STATUS_CHOICE, max_length=16,
                              default=params.PROJECT_STATUS_START)

    class Meta:
        db_table = 'fapd_project_info'
        verbose_name = '项目信息表'


class ProjectPlanTask(CommonDataModel):
    """项目计划任务记录表"""
    project = models.ForeignKey('ProjectInfo', verbose_name="关联项目", on_delete=models.CASCADE,
                                related_name='plan_task', help_text='关联项目')
    name = models.CharField(verbose_name="任务名称", max_length=255)
    status = models.CharField(verbose_name="任务状态", choices=params.TASK_STATUS_CHOICE, max_length=16,
                              default=params.TASK_STATUS_PLAN, help_text="任务当前的状态")
    dtime = models.DateTimeField(verbose_name="任务完成时间", blank=True, null=True)
    in_charge = models.ManyToManyField('ProjectInCharge', verbose_name="责任人")
    remark = models.TextField(verbose_name="备注说明", blank=True, null=True)

    class Meta:
        db_table = 'fapd_project_plan_task'
        verbose_name = '项目计划任务表'
