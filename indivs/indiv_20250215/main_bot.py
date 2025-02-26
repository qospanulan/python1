from telebot import TeleBot

TOKEN = "7614125102:AAHOCQgrHb6etX3rwp5ZvWgh1JObdqc3CPk"

bot = TeleBot(token=TOKEN)

@bot.message_handler(commands=['start'])
def start_command_handler(message):
    print(f"User {message.from_user.id} started the bot")
    bot.send_message(
        chat_id=message.chat.id,
        text=f"You text me with command!"
    )


@bot.message_handler(content_types=['text'])
def help_command_handler(message):

    bot.send_message(
        chat_id=message.chat.id,
        text=f"You text me with message '{message.text}'"
    )


bot.polling()
