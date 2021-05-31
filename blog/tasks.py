"""博客任务模块

Author: Fengchunyang

Date: 2021/5/28 18:40

Desc:
    2021/5/28 18:40 add file.
"""
from celery import shared_task


@shared_task
def print_msg(msg):
    print(msg)
    return
