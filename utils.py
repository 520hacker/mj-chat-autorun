import os
import re
import logging
import requests
from datetime import datetime


def setup_logging():
    logging.basicConfig(
        filename="log.txt",
        level=logging.INFO,
        format="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def getImage(content):
    if not os.path.exists("./downloads"):
        os.makedirs("./downloads")

    # image_urls = re.findall(
    #     r"!\[.*?\]\((https?://\S+?\.(?:png|jpg|jpeg|gif|bmp|tiff|webp))\)", content
    # ) 
    image_urls = re.findall(
        r"!\[.*?\]\((https?://[^\s]+(?:\.(?:png|jpg|jpeg|gif|bmp|tiff|webp))?)\)", content
    )

    if not image_urls:
        print("No image URLs found in the content.")
        logging.info("No image URLs found in the content.")
        return

    for image_url in enumerate(image_urls):
        try:
            headers = {
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "accept-language": "en,zh-CN;q=0.9,zh;q=0.8",
                "priority": "u=0, i",
                "sec-ch-ua": '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "document",
                "sec-fetch-mode": "navigate",
                "sec-fetch-site": "none",
                "sec-fetch-user": "?1",
                "upgrade-insecure-requests": "1",
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            }
            print(image_url)

            response = requests.get(image_url[1], headers=headers)
            # response = requests.get(image_url)
            # print(response.content)
            # print(response.text)

            if response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")

                file_extension = "jpg"
                if "." in image_url:
                    file_extension = image_url.split(".")[-1]

                # file_extension = image_url.split(".")[-1]
                file_path = f"./downloads/image_{timestamp}.{file_extension}"

                with open(file_path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded: {image_url} -> {file_path}")
                logging.info(f"Downloaded: {image_url} -> {file_path}")
            else:
                print(
                    f"Failed to download: {image_url}, status code: {response.status_code}"
                )
                logging.info(
                    f"Failed to download: {image_url}, status code: {response.status_code}"
                )
        except Exception as e:
            print(f"Error occurred while downloading {image_url}: {e}")
            logging.info(f"Error occurred while downloading {image_url}: {e}")
