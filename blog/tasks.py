"""博客任务模块

Author: Fengchunyang

Date: 2021/5/28 18:40

Desc:
    2021/5/28 18:40 add file.
"""
import re

from django.conf import settings
from django.utils import timezone
from celery import shared_task

from blog.models import AccessRecord, Article
from common.utils.network import get_ip_info, baidu_api_put
from common import params


def get_access_record_data(request):
    """获取访问记录需要的数据
    celery发送消息给broker时，会对任务函数及其参数进行序列化，为了避免出现额外异常情况，
    将access_record函数的参数修改为字典类型

    Args:
        request(HttpRequest): 请求体

    Returns:
        result(dict): 数据集
    """
    address = request.META.get('REMOTE_ADDR', 'unknown')
    ip_info = get_ip_info(address)
    region = [ip_info.get("country", ""), ip_info.get("regionName", ""), ip_info.get("city", "")]
    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    spider = re.findall(r'compatible; (.+);', user_agent)

    data = {
        "path": request.META.get('PATH_INFO', ''),
        'query_str': request.META.get('QUERY_STRING', ''),
        'address': address,
        'user_agent': user_agent,
        'referer': request.META.get('HTTP_REFERER', ''),
        'atime': timezone.now(),
        'source': '-'.join(region) if ip_info else '',
        'spider': spider[0] if spider else '',
    }
    return data


@shared_task
def access_record(data):
    """记录网站访问记录

    Args:
        data(dict): 数据集

    Returns:
        result(str): 执行结果
    """
    AccessRecord.objects.create(**data)
    return "访问记录添加成功"


@shared_task
def push_article(data):
    """推送文章

    Args:
        data(dict): 数据集

    Returns:
        status(any): 结果状态
        error(any): 异常
    """
    return baidu_api_put(**data)


@shared_task
def bulk_push_article():
    """一键推送所有已发表文章至百度api

    Returns:
        result(str): 推送结果
    """
    articles = Article.objects.filter(is_publish=True)
    article_links = [f'{settings.SYSTEM_DOMAIN}{article.get_absolute_url()}' for article in articles]
    return baidu_api_put(params.SeoSite, params.SeoSiteToken, article_links)
