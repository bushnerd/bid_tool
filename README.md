# bid_tool

本项目包含多个实用的文件处理工具，主要用于 docx, PDF 和 Markdown 文件的自动化处理。

## 功能模块

### 1. 社保信息提取工具 (extract_individual_social_security)

- 功能：从社保 PDF 文件中提取指定员工信息，并标注保存为图片
- 特点：
  - 自动定位员工信息所在页面
  - 使用红色方框标注员工信息
  - 支持批量处理多个员工
- 依赖：PyMuPDF, pdf2image, PIL

### 2. Markdown 转 Word 工具 (md_dir_docx)

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

### 社保信息提取工具 (extract_individual_social_security)

该工具用于从社保 PDF 文件中提取指定员工信息。

- **源代码运行方式：**
  - **命令行参数方式：**
    - `python extract_individual_social_security/extract_individual_social_security.py <PDF文件路径> <员工姓名1> [员工姓名2...]`
    - 示例：`python extract_individual_social_security/extract_individual_social_security.py "D:\社保证明.pdf" "张三" "李四"`
  - **交互式方式：**
    - `python extract_individual_social_security/extract_individual_social_security.py`
    - 运行后会弹出文件选择框，选择 PDF 文件，然后在控制台输入员工姓名（多个姓名用空格隔开）。
- **打包后运行方式：**
  - 运行 `dist` 目录下生成的 `extract_individual_social_security.exe` 可执行文件。
  - 示例：`./dist/extract_individual_social_security.exe "D:\社保证明.pdf" "张三" "李四"`

### Markdown 转 Word 工具 (md_dir_docx)

该工具用于根据 Markdown 文件结构自动创建目录，并将 PDF/图片转换为带样式的 Word 文档。

- **源代码运行方式：**
  - `python md_dir_docx/md_dir_docx.py`
  - 运行后会弹出文件选择框，选择 Markdown 文件。
  - 工具会根据 Markdown 标题结构在同级目录下创建 `source_dir` 目录。
  - **重要：** 请将 Markdown 中对应标题下的 PDF 或图片文件放入 `source_dir` 中相应的子目录。
  - 放置完成后，按回车键继续，工具将自动处理并生成 Word 文档。
- **打包后运行方式：**
  - 运行 `dist` 目录下生成的 `md_dir_docx.exe` 可执行文件。
  - 示例：`./dist/md_dir_docx.exe`

## 注意事项

- 确保已安装所有依赖库。
- 社保信息提取工具需要配置 Poppler 路径。
- Markdown 转 Word 工具需要准备 `9outline.docx` 模板文件，该文件应与 `md_dir_docx.py` 脚本在同一目录下。
- 各工具支持的文件格式：
  - PDF：所有工具
  - 图片：仅 Markdown 转 Word 工具
  - Markdown：仅 Markdown 转 Word 工具

## 项目结构

```
.
├── extract_individual_social_security/  # 社保信息提取工具
├── md_dir_docx/                # Markdown转Word工具
```

## Roadmap

### 1. 内容提取工具 (extract_content)

- 功能：从 PDF 文件中提取以"★"开头的行
- 用途：快速提取 PDF 文档中的重点内容
- 依赖：PyMuPDF (fitz)

### 2. Office 转 PDF 工具 (officetopdf)

- 功能：将 Office 文档转换为 PDF

### 3. 水印工具 (watermark)

- 功能：为文档添加水印

### 4. 智慧协同下载工具 (zhihuixietong_download)

- 功能：智慧协同平台下载工具

````

## 许可证

本项目采用 GNU General Public License v3.0 (GPLv3) 许可证，详见 LICENSE 文件。

## CI/CD 工作流

[![Build Status](https://github.com/bushnerd/bid_tool/actions/workflows/build.yml/badge.svg)](https://github.com/bushnerd/bid_tool/actions)

本项目使用 GitHub Actions 自动打包工具：

1. 支持以下触发方式：
   - 推送代码到 main 分支
   - 创建 Pull Request
   - 手动触发构建（GitHub Actions 页面点击 Run workflow）
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
````
