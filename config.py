import os
import json
from dotenv import load_dotenv


def load_config():
    load_dotenv()

    api_key = os.getenv("API_KEY")
    api_host = os.getenv("API_HOST")
    api_model = os.getenv("MIDJOURNEY_MODEL")

    with open("prompts.json", "r", encoding="utf-8") as file:
        prompts = json.load(file)

    return {
        "api_key": api_key,
        "api_host": api_host,
        "api_model": api_model,
        "prompts": prompts,
    }
