import requests
import json
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 第一个请求的信息
url_1 = 'http://10.217.248.47:8086/icp_zuul_web/icp-resource/qualifiche/getQualificheList?resourceName=%E4%B8%AD%E7%A7%BB%E9%9B%86%E6%88%90%E6%99%BA%E6%85%A7%E5%AE%89%E9%98%B2%E9%A1%B9%E7%9B%AE%E4%BA%A4%E4%BB%98%E7%AE%A1%E7%90%86%E5%B9%B3%E5%8F%B0&resTypeCode=&publishCompany=&pageIndex=1&pageSize=12'
headers_1 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjAzNTYyODMsInVzZXJfbmFtZSI6IjE4MDYyNTAxMjY2IiwiYXV0aG9yaXRpZXMiOlsiMDAxMCIsIjAwMDYiLCIwMTA1IiwiMDAwNyIsIjAxMDYiLCIwMTAzIiwiMDEwNCIsIjAxMDIiLCIxMTAwMSIsIjYwMDciLCI2MDA2IiwiMTEwMDIiLCI2MDA4IiwiMDEwOSIsIjAxMDciLCIwMTA4IiwiNjAwMSIsIjYwMDMiLCI2MDAyIiwiNjAwNSIsIjYwMDQiLCIxMjA1IiwiMTIwNCIsIjEyMDMiLCIxMjAyIiwiMTIwMSIsIjAxMTAiLCIwMDEyIiwiMTIwMDEiLCIxMDAwMiIsIjEwMDAxIiwiMTAwMDMiXSwianRpIjoiZDk0ODBhMDktNWQzMS00NzEzLTg4NDctODk5MTIwMTI5YzVjIiwiY2xpZW50X2lkIjoiaWNwX3dlYiIsInNjb3BlIjpbImFsbCJdfQ.6fpvsl-IufF0cTBtxJNoYt8CsqYBfd56vG-vD9atRHg',
    'Connection': 'keep-alive',
    'Content-Length': '0',
    'DNT': '1',
    'Origin': 'http://10.217.248.47:8086',
    'Referer': 'http://10.217.248.47:8086/icp_web/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}

# 发送第一个请求
response_1 = requests.post(url_1, headers=headers_1)
data_1 = response_1.json()

# 检查响应状态码和内容
if response_1.status_code == 200:
    logging.info("Request was successful")
else:
    logging.error(f"Request failed with status code {response_1.status_code}")

# 提取文件ID和resourceName
file_id = data_1['data']['lst'][0]['resId']
resource_name = data_1['data']['lst'][0]['resourcesName']
logging.info(f"File ID: {file_id}")
logging.info(f"Resource Name: {resource_name}")


# 第二个请求的信息
url_2 = 'http://10.217.248.47:8086/icp_zuul_web/icp-attachment/zip/qualificationDownloadZipFile'
headers_2 = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MjAzNTYyODMsInVzZXJfbmFtZSI6IjE4MDYyNTAxMjY2IiwiYXV0aG9yaXRpZXMiOlsiMDAxMCIsIjAwMDYiLCIwMTA1IiwiMDAwNyIsIjAxMDYiLCIwMTAzIiwiMDEwNCIsIjAxMDIiLCIxMTAwMSIsIjYwMDciLCI2MDA2IiwiMTEwMDIiLCI2MDA4IiwiMDEwOSIsIjAxMDciLCIwMTA4IiwiNjAwMSIsIjYwMDMiLCI2MDAyIiwiNjAwNSIsIjYwMDQiLCIxMjA1IiwiMTIwNCIsIjEyMDMiLCIxMjAyIiwiMTIwMSIsIjAxMTAiLCIwMDEyIiwiMTIwMDEiLCIxMDAwMiIsIjEwMDAxIiwiMTAwMDMiXSwianRpIjoiZDk0ODBhMDktNWQzMS00NzEzLTg4NDctODk5MTIwMTI5YzVjIiwiY2xpZW50X2lkIjoiaWNwX3dlYiIsInNjb3BlIjpbImFsbCJdfQ.6fpvsl-IufF0cTBtxJNoYt8CsqYBfd56vG-vD9atRHg',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json;charset=UTF-8',
    'DNT': '1',
    'Origin': 'http://10.217.248.47:8086',
    'Referer': 'http://10.217.248.47:8086/icp_web/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
}
data_2 = {
    "batchDownloadReqs": [
        {
            "fileId": file_id,
            "watermark": "仅限湖南省望城经济技术开发区（铜官化工片区）重大安全风险防控项目项目投标使用"
        }
    ]
}

# 发送第二个请求
response_2 = requests.post(url_2, headers=headers_2, json=data_2)

# 检查第二个请求的响应状态码
if response_2.status_code == 200:
    logging.info("Download request was successful")
else:
    logging.error(f"Download request failed with status code {response_2.status_code}")

# 生成文件名
file_name = f"{resource_name}.pdf"

# 保存下载的文件
with open(file_name, 'wb') as file:
    file.write(response_2.content)

logging.info(f"Download completed. File saved as {file_name}.")
