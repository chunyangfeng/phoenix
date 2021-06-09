from django.db import models

from common.models import BasicModel


class Comment(BasicModel):
    """评论模块"""
    article_id = models.IntegerField(verbose_name="关联文章", blank=True, null=True,
                                     help_text="文章下评论需要关联此字段")
    comment = models.ForeignKey('Comment', verbose_name="关联评论", blank=True, null=True, on_delete=models.CASCADE,
                                related_name='sub_comment', help_text='归属于同一个评论的所有评论都被视为子评论，递归嵌套')
    nickname = models.CharField(verbose_name="评论人", max_length=64)
    email = models.CharField(verbose_name="", max_length=64)
    content = models.TextField(verbose_name="评论内容")
    # liked = models.IntegerField(verbose_name="点赞数", default=0)
    is_examine = models.BooleanField(verbose_name="是否通过审核", default=False)
    is_reply = models.BooleanField(verbose_name="是否回复", default=False)

    class Meta:
        # ordering = ('-id', )
        db_table = 'blog_comment'
        verbose_name = '评论表'
