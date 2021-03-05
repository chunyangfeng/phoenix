# -*- coding: utf-8 -*-
"""系统配置视图
时间: 2021/3/4 15:32

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/4 新增文件。

重要说明:
"""
from common.viewset.basic import BasePageView, BasicListViewSet
from blog import models, serializers
from common.params import permissions


class SeoPageView(BasePageView):
    """系统配置-seo管理页面"""
    page = 'mgt/system/seo/seo.html'


class SystemParamPageView(BasePageView):
    """系统参数页面"""
    page = 'mgt/system/param/param.html'


class SeoUrlListView(BasicListViewSet):
    """seo url列表接口"""
    queryset = models.Article.objects.filter(is_publish=True).order_by('-mtime')
    serializer_class = serializers.ArticleSiteMapSerializer
    permission_name = permissions.PER_SYSTEM_SEO
