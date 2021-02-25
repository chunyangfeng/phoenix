from common.viewset.basic import BasePageView


class AuthForbiddenPageView(BasePageView):
    """未授权错误页面"""
    authentication_enable = False
    page = 'errors/401.html'


class AuthNoPermissionPageView(BasePageView):
    """未授权错误页面"""
    authentication_enable = False
    page = 'errors/403.html'


class IndexPageView(BasePageView):
    """博客主页"""
    authentication_enable = False
    page = 'index/index.html'
