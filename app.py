import time
import logging
from config import load_config
from api_client import send_request
from image_processor import process_images_in_directory
from utils import setup_logging

def main():
    config = load_config()
    setup_logging()

    for prompt in config['prompts']:
        try:
            if not send_request(prompt):
                continue
            log_message = "等待0.1分钟后继续下一个请求。"
            time.sleep(10)
            print(log_message)
            logging.info(log_message)
        except Exception as e:
            error_message = f"请求发生错误: {e}"
            print(error_message)
            logging.error(error_message)

    print("画图任务都完成了！开始切图")
    logging.info("画图任务都完成了！开始切图")

    process_images_in_directory("downloads", "output")

    print("所有的任务都完成了！")
    logging.info("所有的任务都完成了！")

if __name__ == "__main__":
    main()
