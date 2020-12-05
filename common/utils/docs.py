# -*- coding: utf-8 -*-
"""文档处理相关工具
时间: 2020/12/5 11:16

作者: Fengchunyang

Blog: http://www.fengchunyang.com

更改记录:
    2020/12/5 新增文件。

重要说明:
"""
import xlwt
import xlrd


class ExcelHandler:
    """处理execl"""

    def __init__(self, filename=None, file_contents=None):
        self.filename = filename
        self.file_contents = file_contents  # file object
        self.workbook = self.get_workbook()
        self.row_count = 0  # 行偏移标记
        self.col_count = 0  # 列偏移标记

    @staticmethod
    def style_cell_bgcolor(color_code):
        """设置单元格背景颜色

        Args:
            color_code(str): 颜色代码

        Returns:
            pattern(xlwt.Pattern): 样式对象
        """
        pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN  # 设置类型模式为实型
        pattern.pattern_fore_colour = color_code
        return pattern

    @staticmethod
    def style_cell_font(color_code=0x00, font_name="微软雅黑", bold=True, height=220):
        """设置单元格字体样式

        Args:
            color_code(str): 颜色代码
            font_name(str): 字体名称
            bold(bool): 是否为实型
            height(int): 高度

        Returns:
            font(xlwt.Font): 字体对象
        """
        font = xlwt.Font()
        font.name = font_name  # 设置字体
        font.colour_index = color_code  # 设置字体颜色
        font.bold = bold  # 是否加粗
        font.height = height  # 除以20之后才是excel的字号
        return font

    @staticmethod
    def style_cell_alignment(horz_obj=xlwt.Alignment.HORZ_CENTER, vert_obj=xlwt.Alignment.VERT_CENTER):
        """设置单元格对齐样式

        Args:
            horz_obj(xlwt.Alignment): 水平对齐方式
            vert_obj(xlwt.Alignment): 垂直对齐方式

        Returns:
            alignment(xlwt.Alignment): 单元格样式对象
        """
        alignment = xlwt.Alignment()
        alignment.horz = horz_obj  # 设置单元格对齐样式，类似于xlwt.Alignment.HORZ_CENTER(居中对齐)等
        alignment.vert = vert_obj  # 设置单元格字体对齐样式，类似于xlwt.Alignment.VERT_CENTER(居中对齐)等
        return alignment

    @staticmethod
    def style_borders_add(line_code=xlwt.Borders.THIN):
        """单元格边框样式

        Args:
            line_code(xlwt.Borders): 单元格边框对象

        Returns:
            borders(xlwt.Borders): 单元格边框对象
        """
        borders = xlwt.Borders()
        borders.left = line_code
        borders.right = line_code
        borders.top = line_code
        borders.bottom = line_code
        return borders

    def get_workbook(self):
        """获取工作簿

        Returns:
            workbook(xlrd.open_workbook): 工作簿对象
        """
        if self.filename:
            return xlrd.open_workbook(filename=self.filename)
        elif self.file_contents:
            return xlrd.open_workbook(file_contents=self.file_contents)
        else:
            raise ValueError("There is no filename or file object supplied to this class")

    def get_sheets(self):
        """获取工作簿中的全部sheet对象列表

        Returns:
            sheets(list): sheet对象列表
        """
        return self.workbook.sheets()

    def get_sheet_name_all(self):
        """获取工作簿中的所有sheet名称

        Returns:
            names(list): sheet名称
        """
        return self.workbook.sheet_names()

    def get_sheet_by_index(self, index):
        """根据索引获取工作簿中的sheet对象

        Args:
            index(int): 索引

        Returns:
            sheet(xlwt.sheet): sheet对象
        """
        return self.workbook.sheet_by_index(index)

    def get_sheet_by_name(self, name):
        """根据sheet名称获取工作簿的sheet

        Args:
            name(str): 工作簿名称

        Returns:
            sheet(xlwt.sheet): sheet对象
        """
        return self.workbook.sheet_by_name(name)

    @staticmethod
    def get_total_rows(sheet):
        """获取指定sheet中的最大行数

        Args:
            sheet(xlwt.sheet): sheet对象

        Returns:
            rows(int): sheet中的最大行数
        """
        return sheet.nrows

    @staticmethod
    def get_total_cols(sheet):
        """获取指定sheet中的最大列数

        Args:
            sheet(xlwt.sheet): sheet对象

        Returns:
            cols(int): sheet中的最大列数
        """
        return sheet.ncols

    @staticmethod
    def get_cell_value(sheet, row, col):
        """获取指定行号和列号的单元格内容

        Args:
            sheet(xlwt.sheet): sheet对象
            row(int): 行号
            col(int): 列号

        Returns:
            result(str): 单元格内容
        """
        return sheet.cell_value(row, col)

    def get_cell_by_row(self, sheet, first_line=True):
        """按行转化内容，每一行为一条数据

        Args:
            sheet(sheet): sheet对象
            first_line(bool): 首行内容是否为title

        Returns:
            data(list): 数据集
        """
        # first_line如果为True则从第一行开始，否则认为首行为title，不做统计
        first = 0 if first_line else 1
        data = []

        for row in range(first, self.get_total_rows(sheet)):
            tmp = {}
            for col in range(0, self.get_total_cols(sheet)):
                tmp[self.get_cell_value(sheet, 0, col)] = self.get_cell_value(sheet, row, col)
            data.append(tmp)
        return data

    @staticmethod
    def write(titles, datas):
        """
        指定内容写入excel
        :param titles: 头部标题列表，有序
        :param datas: 填充数据，一条数据为一个列表，按照title的顺序插入，此参数为一个二维列表
        :return: excel工作簿对象
        """
        workbook = xlwt.Workbook(encoding='utf-8')
        worksheet = workbook.add_sheet('sheet1')
        row_count = 0

        for index, title in enumerate(titles):
            worksheet.write(row_count, index, label=title)
        row_count += 1

        for data in datas:
            for index, value in enumerate(data):
                worksheet.write(row_count, index, value)
            row_count += 1
        return workbook
