import pandas as pd

# 创建一个示例数据帧
data = {'Name': ['Alice', 'Bob', 'Charlie', 'David'],
        'Age': [25, 30, 35, 40],
        'City': ['New York', 'Los Angeles', 'Chicago', 'Houston']}

df = pd.DataFrame(data)

# 指定包含下拉列表的选项
dropdown_options = ['Option 1', 'Option 2', 'Option 3']

# 指定包含下拉列表的单元格范围
dropdown_range = 'C2:C5'  # 这里是示例范围，可以根据实际需求修改

# 使用 with 语句创建 Excel writer 对象，并设置下拉列表
with pd.ExcelWriter('output.xlsx', engine='xlsxwriter') as writer:
    # 将数据写入 Excel 文件
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    
    # 获取与数据写入相关联的 workbook 和 worksheet 对象
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    # 创建数据验证对象
    validation = {
        'validate': 'list',
        'source': dropdown_options
    }

    # 将数据验证对象应用于指定范围内的单元格
    worksheet.data_validation(dropdown_range, validation)