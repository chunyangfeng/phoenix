"""celery定时任务配置

Author: Fengchunyang

Date: 2021/6/7 15:20

Desc:
    2021/6/7 15:20 add file.
"""
from celery.schedules import timedelta, crontab

CELERY_BEAT_SCHEDULE = {
    'bulk_push_article': {  # 一键推送所有文章
        'task': 'blog.tasks.bulk_push_article',
        'schedule': crontab(hour=8, minute=0),
    },
}
