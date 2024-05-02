import pandas as pd

# 创建一个DataFrame示例
data = {'A': [1, 2, 3, 4],
        'B': [5, 6, 7, 8],
        'C': [9, 10, 11, 12],
        'D': [13, 14, 15, 16],
        'E': [17, 18, 19, 20],
        'F': [21, 22, 23, 24],
        'G': [25, 26, 27, 28],
        'H': [29, 30, 31, 32],
        'I': [33, 34, 35, 36],
        'J': [37, 38, 39, 40],
        'K': [41, 42, 43, 44],
        'L': [45, 46, 47, 48],
        'M': [49, 50, 51, 52],
        'N': [53, 54, 55, 56],
        'O': [57, 58, 59, 60],
        'P': [61, 62, 63, 64],
        'S': [65, 66, 67, 68]}

df = pd.DataFrame(data)

# 创建一个Excel写入器，engine设置为openpyxl
with pd.ExcelWriter('output_openpyxl.xlsx', engine='openpyxl') as writer:
    # 将DataFrame写入Excel
    df.to_excel(writer, sheet_name='Sheet1', index=False)

    # 获取Excel的工作表对象
    worksheet = writer.sheets['Sheet1']

    # 添加公式到指定单元格
    formula = '=SUM(A1:S1)'
    worksheet['T1'] = formula