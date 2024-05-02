from pdf2docx import Converter

def pdf_to_docx(pdf_file, docx_file):
    # Convert PDF to Word
    cv = Converter(pdf_file)
    cv.convert(docx_file, start=0, end=None)
    cv.close()

# 将PDF文件转换为Word文档
pdf_to_docx('Report_Template.pdf', 'Report_Template_.docx')