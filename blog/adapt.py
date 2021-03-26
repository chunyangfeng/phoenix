# -*- coding: utf-8 -*-
"""模块接口适配层
时间: 2021/3/3 13:58

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2021/3/3 新增文件。

重要说明:
"""
from blog.auth.interfaces import get_user_info


def adapt_get_user_info(simple=False, **kwargs):
    """获取用户数据

    Args:
        simple(bool): 是否展示详细数据，默认不展示
        **kwargs(dict): 查询关键字

    Returns:
        dict: 用户信息
    """
    return get_user_info(simple, **kwargs)
