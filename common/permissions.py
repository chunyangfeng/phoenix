# -*- coding: utf-8 -*-
"""权限配置
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

PER_SYSTEM_SEO = 'SystemSeo'  # seo管理接口
PER_SYSTEM_PROJECT_MGT = 'SystemProjectManagement'  # 项目管理接口

PER_SHOW_CARD = 'ShowCard'  # 名片信息接口

PER_VISITOR_MESSAGE = 'VisitorMessage'  # 访客私信接口
PER_VISITOR_Subscribe = 'VisitorSubscribe'  # 访客订阅接口

PER_HOT_ARTICLE = 'HotArticle'  # 热门文章接口

PER_COMMENT = 'Comment'  # 评论接口


RES_PERM = {
    PER_BASE: 'ROOT权限',
    PER_ARTICLE: '博客文章',
    PER_ARTICLE_SERIAL: '博客系列',
    PER_ARTICLE_CLASSIFY: '博客分类',
    PER_ARTICLE_TAG: '博客标签',
    PER_SYSTEM_SEO: 'SEO管理',
    PER_SYSTEM_PROJECT_MGT: '项目管理',
    PER_SHOW_CARD: '名片信息',
    PER_VISITOR_MESSAGE: '访客私信',
    PER_VISITOR_Subscribe: '访客订阅',
    PER_HOT_ARTICLE: '热门文章',
    PER_COMMENT: '评论',
}
