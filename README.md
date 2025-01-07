# bid_tool

本项目包含多个实用的文件处理工具，主要用于 docx, PDF 和 Markdown 文件的自动化处理。

## 功能模块

### 1. 内容提取工具 (extract_content)

- 功能：从 PDF 文件中提取以"★"开头的行
- 用途：快速提取 PDF 文档中的重点内容
- 依赖：PyMuPDF (fitz)

### 2. 社保信息提取工具 (extract_individual_social_security)

- 功能：从社保 PDF 文件中提取指定员工信息，并标注保存为图片
- 特点：
  - 自动定位员工信息所在页面
  - 使用红色方框标注员工信息
  - 支持批量处理多个员工
- 依赖：PyMuPDF, pdf2image, PIL

### 3. Markdown 转 Word 工具 (md_dir_docx)

- 功能：根据 Markdown 文件结构自动创建目录，并将 PDF/图片转换为带样式的 Word 文档
- 特点：
  - 支持 Markdown 标题层级自动生成目录结构
  - 自动转换 PDF 为图片并插入 Word
  - 使用预定义模板样式
  - 支持图片自动缩放
- 依赖：python-docx, pdf2image, PIL

## 使用方法

1. 安装依赖：

```bash
pip install -r requirements.txt
```

2. 运行工具：

- 内容提取：`python extract_content/extract_content.py`
- 社保信息提取：`python extract_individual_social_security/extract_individual_social_security.py`
- Markdown 转 Word：`python md_dir_docx/md_dir_docx.py`

## 注意事项

- 确保已安装所有依赖库
- 社保信息提取工具需要配置 Poppler 路径
- Markdown 转 Word 工具需要准备 9outline.docx 模板文件
- 各工具支持的文件格式：
  - PDF：所有工具
  - 图片：仅 Markdown 转 Word 工具
  - Markdown：仅 Markdown 转 Word 工具

## 项目结构

```
.
├── extract_content/            # 内容提取工具
├── extract_individual_social_security/  # 社保信息提取工具
├── md_dir_docx/                # Markdown转Word工具
├── officetopdf/                # Office转PDF工具
├── watermark/                  # 水印工具
└── zhihuixietong_download/     # 智慧协同下载工具
```

## 许可证

本项目采用 MIT 许可证，详见 LICENSE 文件。

## CI/CD 工作流

[![Build Status](https://github.com/bushnerd/bid_tool/actions/workflows/build.yml/badge.svg)](https://github.com/bushnerd/bid_tool/actions)

本项目使用 GitHub Actions 自动打包工具：

1. 当推送代码到 main 分支或创建 Pull Request 时触发构建
2. 自动安装 Python 3.9 和依赖
3. 使用 PyInstaller 打包工具：
   - `extract_individual_social_security`：包含 poppler 二进制文件
   - `md_dir_docx`：包含 9outline.docx 模板文件
4. 构建结果自动上传为 artifacts

### 本地打包

```bash
# 打包社保信息提取工具
cd extract_individual_social_security
pyinstaller --onefile --add-data "poppler/bin/*;poppler/bin" extract_individual_social_security.py

# 打包Markdown转Word工具
cd ../md_dir_docx
pyinstaller --onefile --add-data "9outline.docx;." md_dir_docx.py
```
