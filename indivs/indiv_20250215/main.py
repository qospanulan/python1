import requests


class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.base_url = f"https://api.telegram.org/bot{self.token}"

    def get_updates(self):
        response = requests.get(f"{self.base_url}/getUpdates")
        return response.json()["result"]


TOKEN = "7614125102:AAHOCQgrHb6etX3rwp5ZvWgh1JObdqc3CPk"

bot = TelegramBot(token=TOKEN)


new_messages = bot.get_updates()

for new_message in new_messages:
    text = new_message["message"]["text"]
    user_from = new_message["message"]["from"]["first_name"]
    print(user_from)
    print(text)
    print("================================================")




