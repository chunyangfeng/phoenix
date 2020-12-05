# -*- coding: utf-8 -*-
"""加密相关工具
时间: 2020/12/5 11:16

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/5 新增文件。

重要说明:
"""
import hashlib


def get_md5(obj):
    """
    获取传入的不可变对象的md5
    :param obj: 不可变的对象
    :return: md5
    """
    md5 = hashlib.md5()
    md5.update(obj.encode("utf8"))
    return md5.hexdigest()
