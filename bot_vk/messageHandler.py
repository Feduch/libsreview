import bot_vk.vkapi as vkapi
from bot_vk.bot_commands import *
from bot_vk.command_system import command_list


def get_answer(body):
    # Сообщение по умолчанию если распознать не удастся
    message = "Прости, не понимаю тебя. Напиши 'помощь', чтобы узнать мои команды"
    attachment = ''
    for c in command_list:
        if body in c.keys:
            message, attachment = c.process()
    return message, attachment


def create_answer(data, token):
    user_id = data['from_id']
    message, attachment = get_answer(data['text'].lower())
    vkapi.send_message(user_id, token, message, attachment)
