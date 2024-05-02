import pandas as pd
from openpyxl import Workbook
from openpyxl.drawing.text import Paragraph, ParagraphProperties, CharacterProperties, RichText, RichTextProperties
from openpyxl.drawing.text import Text

# 创建一个DataFrame
data = {'Name': ['Alice', 'Bob', 'Charlie'],
        'Age': [25, 30, 35]}
df = pd.DataFrame(data)

# 创建一个Excel工作簿
wb = Workbook()
ws = wb.active

# 将DataFrame写入Excel
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# 添加文本框
ws['A6'] = 'Here is a text box:'
text = "This is some rich text."
paragraph = Paragraph()
paragraph.add_run(text)
ws.add_text_box(paragraph, 'B6')

# 保存Excel文件
wb.save("output.xlsx")