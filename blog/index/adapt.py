# -*- coding: utf-8 -*-
"""适配层
时间: 2021/3/30 22:17

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/30 新增文件。

重要说明:
"""
from blog.comment.interfaces import get_comment_count


def adapt_get_comment_count(**kwargs):
    """获取指定条件下的评论总数

    Args:
        **kwargs(dict): 可变关键字参数

    Returns:
        count(int): 评论总数
    """
    return get_comment_count(**kwargs)
