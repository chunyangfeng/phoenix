"""视图文件

Author: Fengchunyang

Date: 2021/6/24 18:40

Desc:
    2021/6/24 18:40 add file.
"""
from django.http import HttpResponse


def handler_404(request, *args, **kwargs):
    # path = request.META.get("PATH_INFO")
    # user_agent = request.META.get('HTTP_USER_AGENT')
    # remote_host = request.META.get('REMOTE_ADDR')
    # method = request.META.get('REQUEST_METHOD')
    return HttpResponse("page not found")


def handler_500(request, *args, **kwargs):
    return HttpResponse("server error")
