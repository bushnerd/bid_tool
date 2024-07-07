import requests
import json
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 常量定义
BASE_URL = 'http://10.217.248.47:8086/icp_zuul_web'
HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjAzNTYyODMsInVzZXJfbmFtZSI6IjE4MDYyNTAxMjY2IiwiYXV0aG9yaXRpZXMiOlsiMDAxMCIsIjAwMDYiLCIwMTA1IiwiMDAwNyIsIjAxMDYiLCIwMTAzIiwiMDEwNCIsIjAxMDIiLCIxMTAwMSIsIjYwMDciLCI2MDA2IiwiMTEwMDIiLCI2MDA4IiwiMDEwOSIsIjAxMDciLCIwMTA4IiwiNjAwMSIsIjYwMDMiLCI2MDAyIiwiNjAwNSIsIjYwMDQiLCIxMjA1IiwiMTIwNCIsIjEyMDMiLCIxMjAyIiwiMTIwMSIsIjAxMTAiLCIwMDEyIiwiMTIwMDEiLCIxMDAwMiIsIjEwMDAxIiwiMTAwMDMiXSwianRpIjoiZDk0ODBhMDktNWQzMS00NzEzLTg4NDctODk5MTIwMTI5YzVjIiwiY2xpZW50X2lkIjoiaWNwX3dlYiIsInNjb3BlIjpbImFsbCJdfQ.6fpvsl-IufF0cTBtxJNoYt8CsqYBfd56vG-vD9atRHg',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Origin': 'http://10.217.248.47:8086',
    'Referer': 'http://10.217.248.47:8086/icp_web/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

def download_qualification(resource_name, watermark):
    try:
        # 第一个请求: 获取资质列表信息
        url_getQualificheList = f'{BASE_URL}/icp-resource/qualifiche/getQualificheList?resourceName={resource_name}&resTypeCode=&publishCompany=&pageIndex=1&pageSize=12'
        response_getQualificheList = requests.post(url_getQualificheList, headers=HEADERS)

        # 检查第一个请求的响应状态码和内容
        if response_getQualificheList.status_code == 200:
            logging.info("成功获取资质列表信息")
        else:
            logging.error(f"获取资质列表信息失败，状态码: {response_getQualificheList.status_code}")

        # 提取资源ID
        data_getQualificheList = response_getQualificheList.json()
        res_id = data_getQualificheList['data']['lst'][0]['resId']
        logging.info(f"资源ID提取成功: {res_id}")

        # 第二个请求: 获取资质详情
        url_getQualificheById = f'{BASE_URL}/icp-resource/qualifiche/getQualificheById?resId={res_id}&urlType=0'
        response_getQualificheById = requests.get(url_getQualificheById, headers=HEADERS)

        # 检查第二个请求的响应状态码
        if response_getQualificheById.status_code == 200:
            logging.info("成功获取资质详情")
        else:
            logging.error(f"获取资质详情失败，状态码: {response_getQualificheById.status_code}")

        # 提取文件ID和文件名
        data_getQualificheById = response_getQualificheById.json()
        file_id = data_getQualificheById['data']['resattachmentInfo'][0]['id']
        file_name = data_getQualificheById['data']['resattachmentInfo'][0]['aTitle'] + ".pdf"
        logging.info(f"文件信息提取成功: 文件ID - {file_id}, 文件名 - {file_name}")

        # 第三个请求: 下载文件
        url_downloadZipFile = f'{BASE_URL}/icp-attachment/zip/qualificationDownloadZipFile'
        data_downloadZipFile = {
            "batchDownloadReqs": [
                {
                    "fileId": file_id,
                    "watermark": watermark
                }
            ]
        }

        # 发送第三个请求，下载文件
        response_downloadZipFile = requests.post(url_downloadZipFile, headers=HEADERS, json=data_downloadZipFile)

        # 检查第三个请求的响应状态码
        if response_downloadZipFile.status_code == 200:
            logging.info("成功下载文件")
        else:
            logging.error(f"下载文件失败，状态码: {response_downloadZipFile.status_code}")

        # 保存下载的文件
        with open(file_name, 'wb') as file:
            file.write(response_downloadZipFile.content)
        logging.info(f"文件保存成功: {file_name}")

    except Exception as e:
        logging.error(f"发生异常: {str(e)}")

# 调用函数示例
resource_name = '中移集成应急指挥调度平台'
watermark = "仅限湖南省望城经济技术开发区（铜官化工片区）重大安全风险防控项目项目投标使用"
download_qualification(resource_name, watermark)
