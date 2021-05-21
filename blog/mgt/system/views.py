# -*- coding: utf-8 -*-
"""系统配置视图
时间: 2021/3/4 15:32

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/4 新增文件。

重要说明:
"""
from django.db.models import QuerySet
from rest_framework.status import HTTP_201_CREATED

from common.params import HTTP_SUCCESS
from common.serializers import DoNothingSerializer
from common.utils.network import baidu_api_put
from common.views import BasePageView, BasicListViewSet, BasicInfoViewSet
from blog import models, serializers
from common import permissions
from common import params


class SeoPageView(BasePageView):
    """seo管理页面"""
    page = 'mgt/system/seo/seo.html'


class AccessRecordPageView(BasePageView):
    """访问记录管理页面"""
    page = 'mgt/system/seo/access_record.html'


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


class AccessRecordListView(BasicListViewSet):
    """项目任务详情接口"""
    queryset = models.AccessRecord.objects.all()
    serializer_class = serializers.AccessRecordListSerializer
    permission_name = permissions.PER_SYSTEM_PROJECT_MGT


class ArticlePushApi(BasicListViewSet):
    """文章批量推送接口"""
    queryset = QuerySet()
    serializer_class = DoNothingSerializer
    permission_name = permissions.PER_SYSTEM_SEO

    def post(self, request, *args, **kwargs):
        """批量创建资源数据

        Args:
            request(Request): http request
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            response(Response): 响应数据
        """
        data = request.data.get("data", list())
        code, res = baidu_api_put(params.SeoSite, params.SeoSiteToken, data.split('\n'))
        return self.set_response(HTTP_SUCCESS, res, status=HTTP_201_CREATED)


class FlinkListView(BasicListViewSet):
    """友链申请列表接口"""
    queryset = models.FriendlyLink.objects.all()
    serializer_class = serializers.FriendlyLinkListSerializer
    permission_name = permissions.PER_SYSTEM_SEO


class FlinkPageView(BasePageView):
    """友链申请页面"""
    page = 'mgt/system/seo/flink.html'
