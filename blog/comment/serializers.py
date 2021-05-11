"""评论模块序列化器

Author: chunyang.feng@17zuoye.com

Date: 2021/5/11 11:08

Desc:
    2021/5/11 11:08 add file.
"""
from rest_framework import serializers

from blog.comment.models import Comment


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
