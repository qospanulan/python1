import time
from functools import lru_cache

import requests


TOKEN = '7614125102:AAHOCQgrHb6etX3rwp5ZvWgh1JObdqc3CPk'

class TelegramClient:

    def send_message(self, message: str) -> None:
        print("== in TelegramClient 1 =============================")

        time.sleep(5)
        requests.get(
            url=f"https://api.telegram.org/bot{TOKEN}/sendMessage",
            params={
                "chat_id": 'xxx',
                "text": message
            }
        )
        print("== in TelegramClient 2 =============================")

@lru_cache
def get_telegram_client() -> TelegramClient:
    return TelegramClient()
