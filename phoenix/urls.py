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
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from django.conf import settings

from common import urls as common_urls
from blog import urls as blog_urls

urlpatterns = [
    # 处理静态资源
    path('static/<path:path>', serve, {'document_root': settings.STATIC_URL}),

    # 处理媒体资源
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_URL}),

    # 各app的url主路由
    path('admin/', admin.site.urls),
    path('common/', include(common_urls)),
    path('blog/', include(blog_urls)),
]
