"""评论模块序列化器

Author: Fengchunyang

Date: 2021/5/11 11:08

Desc:
    2021/5/11 11:08 add file.
"""
from rest_framework import serializers

from blog.comment.models import Comment
from blog.models import Article


class CommentListSerializer(serializers.ModelSerializer):
    comment = serializers.SerializerMethodField(read_only=True)

    @staticmethod
    def get_comment(obj):
        """获取子评论数据

        Args:
            obj(Comment): 评论数据实例对象

        Returns:
            result(list): 子评论内容
        """
        return CommentListSerializer(obj.sub_comment.all(), many=True).data

    class Meta:
        model = Comment
        fields = '__all__'


class CommentMgtListSerializer(serializers.ModelSerializer):
    article = serializers.SerializerMethodField(read_only=True)
    comment_content = serializers.SerializerMethodField(read_only=True)
    comment_id = serializers.SerializerMethodField()
    comment = serializers.PrimaryKeyRelatedField(
        queryset=Comment.objects.all(),
        error_messages={"does_not_exist": "评论不存在"}
    )

    @staticmethod
    def get_article(obj):
        """获取关联文章标题

        Args:
            obj(Comment): 评论数据实例对象

        Returns:
            result(str): 关联文章标题
        """
        article = Article.objects.filter(id=obj.article_id)
        return article[0].title if article.exists() else ""

    @staticmethod
    def get_comment_content(obj):
        """获取关联评论正文

        Args:
            obj(Comment): 评论数据实例对象

        Returns:
            result(str): 关联评论正文
        """
        return obj.comment.content if obj.comment else ""

    @staticmethod
    def get_comment_id(obj):
        """获取关联评论ID

        Args:
            obj(Comment): 评论数据实例对象

        Returns:
            result(str): 关联评论ID
        """
        return obj.comment.id if obj.comment else ""

    class Meta:
        model = Comment
        fields = '__all__'


class CommentMgtInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
