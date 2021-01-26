# -*- coding: utf-8 -*-
"""
时间: 2020/11/23 11:05

作者: Fengchunyang

更改记录:
    2020/11/23 新增文件。

重要说明:
"""
import datetime

from django.db import models


class BasicModel(models.Model):
    """抽象基类"""
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    desc = models.CharField(verbose_name="描述", max_length=256, blank=True, null=True)
    ctime = models.DateTimeField(verbose_name="创建时间", auto_now_add=datetime.datetime.now())
    mtime = models.DateTimeField(verbose_name="修改时间", auto_now=datetime.datetime.now())

    class Meta:
        abstract = True

    def serializer(self, formatter="json"):
        """
        序列化模型数据
        :param formatter: 序列化类型，默认json
        :return:
        """
        data = {}
        for field in self._meta.fields:
            key = field.name
            value = getattr(self, key)
            data.update(self.formatter(field, key, value))
        return data

    @staticmethod
    def get_datetime(obj, formatter="%Y-%m-%d %H:%M:%S"):
        """
        处理datetime.datetime()对象
        :param obj: datetime.datetime()对象
        :param formatter: 格式化字符串
        :return: 时间字符串
        """
        return obj.strftime(formatter)

    def formatter(self, field, key, value):
        """格式化model field内容"""
        v_str = value.__str__()

        if type(value) == datetime.datetime:
            v_str = self.get_datetime(value)

        if type(value) == datetime.date:
            # 由于datetime.date是datetime.datetime的子类，所以使用isinstance方法判断不出具体类型
            v_str = self.get_datetime(value, "%Y-%m-%d")

        if isinstance(field, (models.BooleanField, models.NullBooleanField)):
            v_str = value

        if isinstance(field, models.ForeignKey):
            v_str = getattr(self, f"get_{key}")  # 利用反射在获取定义在model中的外键值(仅限主属性)

        if v_str is None:
            v_str = ''
        return {key: v_str}
