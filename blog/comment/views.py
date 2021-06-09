"""评论模块视图

Author: Fengchunyang

Site: https://www.fengchunyang.com

Date: 2021/5/11 11:03

Desc:
    2021/5/11 11:03 add file.
"""
from blog import tasks
from blog.comment.models import Comment
from blog.comment.serializers import CommentListSerializer, CommentMgtListSerializer, CommentMgtInfoSerializer
from common.views import BasicListViewSet, BasePageView, BasicInfoViewSet
from common import permissions


class ArticleCommentListView(BasicListViewSet):
    """文章评论列表接口"""
    queryset = Comment.objects.filter(comment=None, is_examine=True)
    serializer_class = CommentListSerializer
    permission_name = permissions.PER_COMMENT
    authentication_enable = False


class CommentListView(BasicListViewSet):
    """评论列表接口"""
    queryset = Comment.objects.filter(article_id=None, is_examine=True).order_by('-id')
    serializer_class = CommentListSerializer
    permission_name = permissions.PER_COMMENT
    authentication_enable = False


class CommentMgtListView(BasicListViewSet):
    """留言管理列表接口"""
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentMgtListSerializer
    permission_name = permissions.PER_COMMENT


class CommentMgtInfoView(BasicInfoViewSet):
    """文章详情接口"""
    queryset = Comment.objects.all()
    serializer_class = CommentMgtInfoSerializer
    permission_name = permissions.PER_COMMENT


class CommentPageView(BasePageView):
    """留言板页面"""
    authentication_enable = False
    page = 'index/comment/comment.html'

    def _post_get(self, request, response, *args, **kwargs):
        """响应页面之后的操作

        Args:
            request(Request): http request
            response(Response): 响应主体
            *args(list): 可变参数
            **kwargs(dict): 可变关键字参数

        Returns:
            error(str): 错误信息，None为没有错误
            reason(str): 错误原因，为''则没有错误
            response(Response): 响应主体
        """
        # 访问成功后添加访问记录
        data = tasks.get_access_record_data(request)
        tasks.access_record.delay(data)
        return None, '', response


class CommentMgtPageView(BasePageView):
    """留言管理页面"""
    page = 'mgt/blog/comment/comment.html'
