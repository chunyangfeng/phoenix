# -*- coding: utf-8 -*-
"""
时间: 2021/2/18 19:01

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/2/18 新增文件。

重要说明:
"""
from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """Csrf验证类

    """

    def enforce_csrf(self, request):
        """csrf

        Args:
            request(rest_framework.request.Request): 传入请求

        Returns:
            bool(boolean): 布尔值

        """
        return True
