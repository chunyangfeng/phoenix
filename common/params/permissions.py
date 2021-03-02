# -*- coding: utf-8 -*-
"""
时间: 2020/11/26 17:37

作者: Fengchunyang

更改记录:
    2020/11/26 新增文件。

重要说明:
"""
PER_BASE = 'phoenix'  # 根权限，属于此权限的应用，直接略过权限校验

PER_ARTICLE = 'Article'  # 文章列表接口权限
PER_ARTICLE_CLASSIFY = 'ArticleClassify'  # 文章分类接口权限
PER_ARTICLE_TAG = 'ArticleTag'  # 文章标签接口权限
PER_ARTICLE_SERIAL = 'ArticleSerial'  # 文章系列接口权限


RES_PERM = {
    PER_BASE: 'ROOT权限',
    PER_ARTICLE: '博客文章',
    PER_ARTICLE_SERIAL: '博客系列',
    PER_ARTICLE_CLASSIFY: '博客分类',
    PER_ARTICLE_TAG: '博客标签',
}
