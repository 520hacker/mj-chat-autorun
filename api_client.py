import json
import requests
from requests.exceptions import RequestException
import logging
import sseclient
from config import load_config
from utils import getImage

config = load_config()

url = f"{config['api_host']}/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream",
    "Authorization": f"Bearer {config['api_key']}",
}

data_template = {
    "messages": [
        {"role": "system", "content": "[midjourney] 根据要求绘图"},
        {"role": "user", "content": ""},
    ],
    "stream": True,
    "model": config['api_model'],
    "temperature": 0.5,
    "presence_penalty": 0,
    "frequency_penalty": 0,
    "top_p": 1,
}

data_template_dalle3 = {
    "model": config['api_model'],
    "prompt": "a cat",
    "n": 1,
    "size": "1024x1024"
}

# 1024x1024, 1024x1792 or 1792x1024

def send_request(prompt):
    data = data_template.copy()
    data["messages"][1]["content"] = prompt

    log_message = f"正在创建 '{prompt}' 的绘画线程。"
    print(log_message)
    logging.info(log_message)

    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
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

        print()

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
