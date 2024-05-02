# import numpy as np
# import pandas as pd

# df = pd.read_excel("demo.xlsx")
# n_rows = df.shape[0] # 50

# # Write to xlsx file 
# writer = pd.ExcelWriter('new_demo.xlsx', engine='xlsxwriter')
# df.to_excel(writer, sheet_name='Sheet1', index=False)

# # Assign workbook and worksheet
# workbook = writer.book
# worksheet = writer.sheets['Sheet1']

# # Creation of unlocked format
# unlocked = workbook.add_format({'locked': False})
# worksheet.set_column('A:B', None, unlocked)

# # Creation of the dropdown menus
# for i in range(n_rows):
#     worksheet.data_validation('B2:B'+str(1+n_rows), {'validate' : 'list', 'source': ['上班', '居家', '休假日', '加班', '請假']})

# worksheet.protect()
# # Close the workbook
# workbook.close()

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import NamedStyle, Protection
from openpyxl.worksheet.datavalidation import DataValidation

# 读取 Excel 文件
df = pd.read_excel("demo.xlsx")
n_rows = df.shape[0]  # 50

# 创建 ExcelWriter，engine 设置为 'openpyxl'
with pd.ExcelWriter('new_demo_openpyxl.xlsx', engine='openpyxl') as writer:
    # 将 DataFrame 写入 Excel
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # 获取 Excel 的工作簿和工作表对象
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # 创建一个新的样式，解锁 "A" 列和 "B" 列的单元格
    unlocked_style = NamedStyle(name='unlocked', protection=Protection(locked=False))
    workbook.add_named_style(unlocked_style)

    # 设置第一个单元格样式
    worksheet['A1'].style = 'unlocked'

    # 设置整列的样式
    for row in worksheet.iter_rows(min_row=1, max_row=n_rows, min_col=2, max_col=2):
        for cell in row:
            cell.style = 'unlocked'

    # 创建下拉列表
    for i in range(2, n_rows + 2):
        dv = DataValidation(type="list", formula1='"上班,居家,休假日,加班,請假"', allow_blank=True)
        worksheet.add_data_validation(dv)
        dv.add(f'B{i}')

    # 保护工作表
    worksheet.protection.sheet = True