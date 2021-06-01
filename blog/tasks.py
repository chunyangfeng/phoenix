"""博客任务模块

Author: Fengchunyang

Date: 2021/5/28 18:40

Desc:
    2021/5/28 18:40 add file.
"""
import re

from django.utils import timezone
from celery import shared_task

from blog.models import AccessRecord
from common.utils.network import get_ip_info, baidu_api_put


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

    data = {
        "path": request.META.get('PATH_INFO', ''),
        'query_str': request.META.get('QUERY_STRING', ''),
        'address': address,
        'user_agent': request.META.get('HTTP_USER_AGENT', 'unknown'),
        'referer': request.META.get('HTTP_REFERER', ''),
        'atime': timezone.now(),
        'source': '-'.join(region) if ip_info else '',
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
