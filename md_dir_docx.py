# -*- coding: UTF-8 -*-
' markdown to directory to docx'

__author__ = 'bushnerd'

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
source_dir = r'D:\github\bid_tool\pdf'
image_dir = r'D:\github\bid_tool\image'
template_path = r'D:\OneDrive\documents\template\9级目录模板.docx'
output_docx = r'D:\github\bid_tool\bid.docx'

# 创建image目录
if not os.path.exists(image_dir):
    os.makedirs(image_dir)
    logging.info(f'Created image directory: {image_dir}')
else:
    logging.info(f'Image directory already exists: {image_dir}')

# 复制文件夹到image目录
for root, dirs, _ in os.walk(source_dir):
    for dir_name in dirs:
        src_dir = os.path.join(root, dir_name)
        dst_dir = os.path.join(image_dir, os.path.relpath(src_dir, source_dir))
        os.makedirs(dst_dir, exist_ok=True)
        logging.info(f'Created directory: {dst_dir}')

# 创建新的docx文档并使用模板样式
doc = Document(template_path)
logging.info(f'Loaded template document: {template_path}')

# 最大宽度设置为14cm
max_width_cm = 14.0
max_width_in = Cm(max_width_cm).inches

# 遍历source_dir目录
for root, dirs, files in os.walk(source_dir):
    # 获取当前文件夹名称作为标题
    current_folder_name = os.path.basename(root)
    if current_folder_name != '':
        heading_level = root.count(os.sep) - source_dir.count(os.sep) + 1
        doc.add_heading(current_folder_name, level=heading_level)
        logging.info(f'Added heading: {current_folder_name} at level {heading_level}')
    
    for file in files:
        file_path = os.path.join(root, file)
        rel_file_path = os.path.relpath(file_path, source_dir)
        file_extension = os.path.splitext(file)[1].lower()
        
        image_paths = []
        if file_extension == '.pdf':
            logging.info(f'Converting PDF to images: {file_path}')
            # 将pdf文件转换为图像并保存到image目录
            images = convert_from_path(file_path, dpi=72, size=(1800, None))  # 调整dpi和size以控制图片大小和清晰度
            for i, image in enumerate(images):
                image_path = os.path.join(image_dir, rel_file_path.replace('.pdf', f'_{i}.png'))
                image.save(image_path, 'PNG')
                image_paths.append(image_path)
                logging.info(f'Saved image: {image_path}')
        elif file_extension in ['.png', '.jpg', '.jpeg']:
            # 如果已经是图片文件，则直接使用
            image_path = os.path.join(image_dir, rel_file_path)
            shutil.copy(file_path, image_path)
            image_paths = [image_path]
            logging.info(f'Copied image: {image_path}')

        # 将图像插入到docx文档并设置样式
        for image_path in image_paths:
            with Image.open(image_path) as img:
                width_in_inches = img.width / img.info.get('dpi', (72, 72))[0]
                if width_in_inches > max_width_in:
                    width_in_inches = max_width_in
                    logging.info(f'Resizing image: {image_path} to width {width_in_inches} inches')
                else:
                    logging.info(f'Using original size for image: {image_path}')

            paragraph = doc.add_paragraph()
            run = paragraph.add_run()
            run.add_picture(image_path, width=Inches(width_in_inches))
            paragraph.style = doc.styles['图片样式']  # 设置为“图片样式”
            logging.info(f'Inserted image into document with style "图片样式": {image_path}')

# 保存docx文档
doc.save(output_docx)
logging.info(f'Saved final document: {output_docx}')
