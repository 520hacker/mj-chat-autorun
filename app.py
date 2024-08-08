import json
import time
import requests
from requests.exceptions import RequestException
import logging
import sseclient
import re
import os
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

api_key = os.getenv("API_KEY")
api_host = os.getenv("API_HOST")
api_model = os.getenv("MIDJOURNEY_MODEL")

# 设置日志
logging.basicConfig(
    filename="log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# 读取 JSON 文件
with open("prompts.json", "r", encoding="utf-8") as file:
    prompts = json.load(file)

# 请求 URL 和头信息
url = f"{api_host}/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream",
    "Authorization": f"Bearer {api_key}",
}

# 请求数据模板
data_template = {
    "messages": [
        {"role": "system", "content": "[midjourney] 根据要求绘图"},
        {"role": "user", "content": ""},
    ],
    "stream": True,
    "model": api_model,
    "temperature": 0.5,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "top_p": 1,
}


def send_request(prompt):
    data = data_template.copy()
    data["messages"][1]["content"] = prompt

    log_message = f"正在创建 '{prompt}' 的绘画线程。"
    print(log_message)
    logging.info(log_message)

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        # response.raise_for_status()
        client = sseclient.SSEClient(response)
        result = ""
        for event in client.events():
            if event.data == "[DONE]" or event.data == " [DONE]":
                break

            try:
                data = json.loads(event.data)
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["delta"].get("content")
                    if content:
                        result += content
                        print(content, end="", flush=True)
                    else:
                        print(json.dumps(data["choices"], indent=2))
                else:
                    print(json.dumps(data, indent=2))
            except json.JSONDecodeError:
                print(f"无法解析JSON: {event.data}")
                logging.info(event.data)

        print()  # 打印一个换行

        log_message = f"'{prompt}' 的绘画线程已结束。"

        logging.info(result)
        getImage(result)

        print(log_message)
        logging.info(log_message)
    except RequestException as e:
        error_message = f"请求发生错误: {e}"
        print(error_message)
        logging.error(error_message)
        return False
    return True


def getImage(content):
    # 创建下载目录，如果不存在
    if not os.path.exists("./downloads"):
        os.makedirs("./downloads")

    # 优化后的正则表达式匹配所有 markdown 中的标准图片格式的地址
    image_urls = re.findall(
        r"!\[.*?\]\((https?://\S+?\.(?:png|jpg|jpeg|gif|bmp|tiff|webp))\)", content
    )

    if not image_urls:
        print("No image URLs found in the content.")
        logging.info("No image URLs found in the content.")
        return

    # 对提取到的每个URL进行下载
    for i, image_url in enumerate(image_urls):
        try:
            response = requests.get(image_url)

            if response.status_code == 200:
                # 生成时间戳命名
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
                file_extension = image_url.split(".")[-1]
                file_path = f"./downloads/image_{timestamp}.{file_extension}"

                # 保存图片到 ./downloads
                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {image_url} -> {file_path}")
                logging.info(f"Downloaded: {image_url} -> {file_path}")
            else:
                print(
                    f"Failed to download: {image_url}, status code: {response.status_code}"
                )
                logging.info(f"Failed to download: {image_url}, status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred while downloading {image_url}: {e}")
            logging.info(f"Error occurred while downloading {image_url}: {e}")


def main():
    for prompt in prompts:
        try:
            if not send_request(prompt):
                continue
            log_message = "等待0.1分钟后继续下一个请求。"
            time.sleep(10)  # 等待 5 分钟
            print(log_message)
            logging.info(log_message)
        except RequestException as e:
            error_message = f"请求发生错误: {e}"

    print("画图任务都完成了！开始切图")
    logging.info("画图任务都完成了！开始切图")

    current_directory = os.getcwd()
    download_directory = os.path.join(current_directory, "downloads")
    output_directory = os.path.join(current_directory, "output")
    process_images_in_directory(download_directory, output_directory)

    print("所有的任务都完成了！")
    logging.info("所有的任务都完成了！")


def split_image(image_path, output_dir):
    image = Image.open(image_path)
    width, height = image.size

    if width <= 2000:
        return

    base_name = os.path.splitext(os.path.basename(image_path))[0]
    ext = os.path.splitext(image_path)[1]

    mid_width = width // 2
    mid_height = height // 2

    # Define the box coordinates for cropping
    boxes = [
        (0, 0, mid_width, mid_height),
        (mid_width, 0, width, mid_height),
        (0, mid_height, mid_width, height),
        (mid_width, mid_height, width, height),
    ]

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, box in enumerate(boxes):
        cropped_image = image.crop(box)
        output_path = os.path.join(output_dir, f"{base_name}_{i+1}{ext}")
        cropped_image.save(output_path)


def process_images_in_directory(directory, output_dir):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(
                (".png", ".jpg", ".jpeg", ".bmp", ".gif", ".tiff", ".webp")
            ):
                image_path = os.path.join(root, file)
                split_image(image_path, output_dir)


if __name__ == "__main__":
    main()
