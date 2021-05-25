"""评论模块视图

Author: Fengchunyang

Site: http://www.fengchunyang.com

Date: 2021/5/11 11:03

Desc:
    2021/5/11 11:03 add file.
"""
from blog.comment.models import Comment
from blog.comment.serializers import CommentListSerializer
from common.views import BasicListViewSet, BasePageView
from common import permissions


class ArticleCommentListView(BasicListViewSet):
    """文章评论列表接口"""
    queryset = Comment.objects.filter(comment=None)
    serializer_class = CommentListSerializer
    permission_name = permissions.PER_COMMENT
    authentication_enable = False


class CommentListView(BasicListViewSet):
    """评论列表接口"""
    queryset = Comment.objects.filter(article_id=None).order_by('-id')
    serializer_class = CommentListSerializer
    permission_name = permissions.PER_COMMENT


class CommentPageView(BasePageView):
    """留言板页面"""
    authentication_enable = False
    page = 'index/comment/comment.html'
