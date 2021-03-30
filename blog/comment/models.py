from django.db import models

from common.models import BasicModel


class Comment(BasicModel):
    """评论模块"""
    fk = models.IntegerField(verbose_name="外联主键", blank=True, null=True)
    comment = models.ForeignKey('Comment', verbose_name="关联评论", blank=True, null=True, on_delete=models.CASCADE,
                                related_name='sub_comment', help_text='归属于同一个评论的所有评论都被视为子评论，递归嵌套')
    user_id = models.IntegerField(verbose_name="评论人")
    content = models.TextField(verbose_name="评论内容")
    liked = models.IntegerField(verbose_name="点赞数", default=0)

    class Meta:
        ordering = ('-id', )
        db_table = 'comment'
        verbose_name = '评论表'
