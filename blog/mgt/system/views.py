# -*- coding: utf-8 -*-
"""系统配置视图
时间: 2021/3/4 15:32

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/4 新增文件。

重要说明:
"""
from common.viewset.basic import BasePageView, BasicListViewSet, BasicInfoViewSet
from blog import models, serializers
from common.params import permissions


class SeoPageView(BasePageView):
    """系统配置-seo管理页面"""
    page = 'mgt/system/seo/seo.html'


class SystemParamPageView(BasePageView):
    """系统参数页面"""
    page = 'mgt/system/param/param.html'


class SystemFlowPageView(BasePageView):
    """系统-项目流程页面"""
    page = 'mgt/system/flow/flow.html'


class ProjectInfoAddPageView(BasePageView):
    """系统-项目信息新增/编辑页面"""
    page = 'mgt/system/flow/info/info_add.html'


class ProjectTaskAddPageView(BasePageView):
    """系统-项目任务新增/编辑页面"""
    page = 'mgt/system/flow/task/task_add.html'


class SeoUrlListView(BasicListViewSet):
    """seo url列表接口"""
    queryset = models.Article.objects.filter(is_publish=True).order_by('-mtime')
    serializer_class = serializers.ArticleSiteMapSerializer
    permission_name = permissions.PER_SYSTEM_SEO


class ProjectInfoListView(BasicListViewSet):
    """项目信息列表接口"""
    queryset = models.ProjectInfo.objects.all()
    serializer_class = serializers.ProjectInfoListSerializer
    permission_name = permissions.PER_SYSTEM_PROJECT_MGT


class ProjectInfoInfoView(BasicInfoViewSet):
    """项目信息详情接口"""
    queryset = models.ProjectInfo.objects.all()
    serializer_class = serializers.ProjectInfoInfoSerializer
    permission_name = permissions.PER_SYSTEM_PROJECT_MGT


class ProjectTaskListView(BasicListViewSet):
    """项目任务列表接口"""
    queryset = models.ProjectPlanTask.objects.all()
    serializer_class = serializers.ProjectTaskListSerializer
    permission_name = permissions.PER_SYSTEM_PROJECT_MGT


class ProjectTaskInfoView(BasicInfoViewSet):
    """项目任务详情接口"""
    queryset = models.ProjectPlanTask.objects.all()
    serializer_class = serializers.ProjectTaskInfoSerializer
    permission_name = permissions.PER_SYSTEM_PROJECT_MGT
