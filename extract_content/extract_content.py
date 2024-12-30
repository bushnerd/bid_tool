import fitz  # PyMuPDF
import re

def extract_star_lines(pdf_path):
    # 打开 PDF 文件
    document = fitz.open(pdf_path)
    star_lines = []

    # 遍历每一页
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        text = page.get_text("text")

        # 使用正则表达式提取以“★”开头的行，包括换行符
        matches = re.findall(r'★.*(?:\n.*)*', text)
        star_lines.extend(matches)

    return star_lines
# 示例使用
pdf_path = '2.pdf'
star_lines = extract_star_lines(pdf_path)
for line in star_lines:
    print(line)
