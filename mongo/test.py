import pandas as pd
from openpyxl.worksheet.datavalidation import DataValidation

# 创建一个示例 DataFrame
df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})

# 创建 ExcelWriter
with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
    # 将 DataFrame 写入 ExcelWriter
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # 获取当前活动的工作表
    worksheet = writer.sheets['Sheet1']

    # 创建下拉列表数据验证
    dv = DataValidation(type="list", formula1='"Option1,Option2,Option3"', allow_blank=False)

    # 添加数据验证到指定列
    for col in range(1, df.shape[1] + 1):
        dv.add(f'{chr(64 + col)}2:{chr(64 + col)}{df.shape[0] + 1}')

    # 添加数据验证到工作表
    worksheet.add_data_validation(dv)

    # 保存更改
    writer.save()