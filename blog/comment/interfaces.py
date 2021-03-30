# -*- coding: utf-8 -*-
"""评论模块接口层
时间: 2021/3/30 22:18

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/30 新增文件。

重要说明:
"""
from .models import Comment


def get_comment_count(**kwargs):
    """获取指定条件下的评论总数

    Args:
        **kwargs(dict): 可变关键字参数

    Returns:
        count(int): 评论总数
    """
    queryset = Comment.objects.filter(**kwargs)
    return queryset.count()
