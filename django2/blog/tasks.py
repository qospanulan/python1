from celery import shared_task

from common.telegram_client import TelegramClient, get_telegram_client


@shared_task
def telegram_send_message_task(message: str):

    get_telegram_client().send_message(message=message)

