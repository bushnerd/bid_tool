import sys
import logging
import fitz
import pdf2image
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.INFO)

def extract_individual_social_security(employee_name):
    logging.info(f"开始提取 {employee_name} 的社保信息...")

    # 1. 读取全员社保证明文件
    try:
        doc = fitz.open("全员社保.pdf")
        total_pages = doc.page_count
    except FileNotFoundError:
        logging.error("找不到全员社保证明文件！")
        return

    # 2. 查找员工姓名所在的页码和坐标
    employee_page = None
    employee_coords = None
    for page_num in range(total_pages):
        page = doc.load_page(page_num)
        text = page.get_text()
        if employee_name in text:
            employee_page = page_num
            employee_coords = page.search_for(employee_name)
            break

    if employee_page is None:
        logging.error(f"未找到员工 {employee_name} 的信息！")
        return

    # 3. 导出包含员工姓名的页面为图片，并以员工姓名为文件名保存到当前目录
    try:
        images = pdf2image.convert_from_path("全员社保.pdf", first_page=employee_page+1, last_page=employee_page+1)
        image = images[0]  # 取第一张图片

        # 创建可绘制对象
        draw = ImageDraw.Draw(image)

        # 调整坐标以匹配图像分辨率
        scale_x = image.width / float(page.rect.width)
        scale_y = image.height / float(page.rect.height)
        draw = ImageDraw.Draw(image)

        # 4. 基于前面的坐标，为员工姓名所在那一行，用红框标注，并加粗线条。
        for coord in employee_coords:
            x0, y0, x1, y1 = coord  # 坐标格式为 (x0, y0, x1, y1)
            # 按比例调整坐标
            x0 *= scale_x
            y0 *= scale_y
            x1 *= scale_x
            y1 *= scale_y
            # 调整矩形框的宽度为整个页面的宽度
            x0 = 0
            x1 = image.width
            # 调整矩形框的高度，上下各加50%
            height_adjustment = (y1 - y0) * 0.5
            y0 -= height_adjustment
            y1 += height_adjustment
            # 画矩形框并加粗线条
            draw.rectangle([x0, y0, x1, y1], outline="red", width=5)

        image.save(f"{employee_name}.png", dpi=(120, 120))  # 以员工姓名为文件名保存到当前目录

    except Exception as e:
            logging.error(f"导出图片时出现错误：{e}")
            return

    # 4. 在图片中标注员工姓名
    for coord in employee_coords:
        # 在此示例中未标注，你可以添加标注代码
        pass

    doc.close()

    logging.info(f"{employee_name} 的社保信息提取完成！")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_individual_social_security.py <employee_name1> <employee_name2> ...")
    else:
        for employee_name in sys.argv[1:]:
            extract_individual_social_security(employee_name)
