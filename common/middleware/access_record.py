# -*- coding: utf-8 -*-
"""接口访问记录
时间: 2021/3/9 19:31

作者: Fengchunyang

Blog: https://www.fengchunyang.com

更改记录:
    2021/3/9 新增文件。

重要说明:
"""
import re

from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from blog.models import AccessRecord
from common.utils.network import get_ip_info


class AccessRecordMiddleware(MiddlewareMixin):
    """将所有的请求都记录下来，存储在数据库中，用于分析网站seo的状态"""
    allow_record = (
        re.compile(r'/blog/index/article/\d+$'),  # 文章详情页
    )

    def process_request(self, request):
        """创建访问记录

        Args:
            request(HttpRequest): request
        """
        meta = request.META
        now = timezone.now()
        path = meta.get('PATH_INFO', '')

        for allowed in self.allow_record:
            if re.match(allowed, path) is not None:
                address = meta.get('REMOTE_ADDR', 'unknown')
                ip_info = get_ip_info(address)
                region = [ip_info.get("country", ""), ip_info.get("regionName", ""), ip_info.get("city", "")]
                data = {
                    "path": path,
                    'query_str': meta.get('QUERY_STRING', ''),
                    'address': address,
                    'user_agent': meta.get('HTTP_USER_AGENT', 'unknown'),
                    'referer': meta.get('HTTP_REFERER', ''),
                    'atime': now,
                    'source': '-'.join(region) if ip_info else '',
                }
                AccessRecord.objects.create(**data)
                break
        return
