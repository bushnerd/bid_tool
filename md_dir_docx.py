import os
import shutil
import logging
from docx import Document
from docx.shared import Inches, Cm
from pdf2image import convert_from_path
from PIL import Image

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 定义路径
markdown_file = r'D:\github\bid_tool\bid.md'
source_dir = r'D:\github\bid_tool\source_dir'
image_dir = r'D:\github\bid_tool\image_dir'
template_path = r'D:\OneDrive\documents\template\9级目录模板.docx'
output_docx = r'D:\github\bid_tool\bid.docx'

# # 根据 markdown 结构创建目录
# def create_dirs_from_markdown(markdown_file, base_dir):
#     with open(markdown_file, 'r', encoding='utf-8') as file:
#         lines = file.readlines()

#     current_path = base_dir
#     for line in lines:
#         if line.startswith('#'):
#             level = line.count('#')
#             folder_name = line.strip('#').strip()
#             current_path = os.path.join(base_dir, *(folder_name.split(' ')))
#             os.makedirs(current_path, exist_ok=True)
#             logging.info(f'Created directory: {current_path}')

# create_dirs_from_markdown(markdown_file, source_dir)
# 根据 markdown 结构创建目录
def create_dirs_from_markdown(markdown_file, base_dir):
    with open(markdown_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_paths = [base_dir]  # 栈结构来存储当前路径
    for line in lines:
        if line.startswith('#'):
            level = line.count('#')
            folder_name = line.strip('#').strip()
            
            # 保证current_paths与markdown的层级一致
            while len(current_paths) > level:
                current_paths.pop()
            
            # 创建新的路径并存入栈中
            current_path = os.path.join(current_paths[-1], folder_name)
            os.makedirs(current_path, exist_ok=True)
            current_paths.append(current_path)
            logging.info(f'Created directory: {current_path}')

create_dirs_from_markdown(markdown_file, source_dir)
