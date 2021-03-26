"""phoenix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.views.static import serve
from django.conf import settings

from blog import urls as blog_urls

from blog.index.views import IndexPageView, AuthForbiddenPageView, AuthNoPermissionPageView

urlpatterns = [
    # 处理静态资源
    path('phoenix-web/<path:path>', serve, {'document_root': settings.STATIC_URL}),

    # # 处理媒体资源
    # path('media/<path:path>', serve, {'document_root': settings.MEDIA_URL}),

    # 各app的url主路由
    path('', IndexPageView.as_view(), name='index-page'),
    path('errors/401', AuthForbiddenPageView.as_view(), name='401'),
    path('errors/403', AuthNoPermissionPageView.as_view(), name='403'),

    path('blog/', include(blog_urls)),
]
