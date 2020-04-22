# <*_* python3 coding:utf-8 D:\pycharm *_*>

import xlwt, xlrd
# from xlutils.copy import copy as xl_copy
import xlutils.copy


def excel_open():
    """"""
    f = xlrd.open_workbook('../conf/case.xls', formatting_info=True)
    # 工作表
    sheet = f.sheet_by_name('response')
    """
    print(sheet)
    # 行
    print(sheet.row_values(1))
    # 列
    print(sheet.col_values(0))
    # 单元格
    print(sheet.cell(1, 0))
    # 单元格value
    """
    # print(sheet.cell_value(1, 0))

    return sheet


def excel_wr(row, col, resp):
    """"""
    # 读取文件对象,保留原有格式
    f = xlrd.open_workbook('../conf/case.xls', formatting_info=True)
    # 转为可操作对象
    wt = xlutils.copy.copy(f)
    # 创建新文件 f = xlwt.Workbook(encoding='utf-8')
    # 读取工作表
    sheets = wt.get_sheet(1)
    sheets.write(row, col, resp)
    wt.save('../case.xls')






