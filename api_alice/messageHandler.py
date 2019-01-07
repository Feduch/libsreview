from api_alice.alice_answers import *
from api_alice.dialog_system import dialog_list
from django.core.cache import cache


def get_answer(body):
    # Сообщение по умолчанию если распознать не удастся
    message = {}
    message['text'] = "Прости, чего-то я устала и путаюсь, давай попробуем еще раз. Назови жанр и года."
    attachment = ''
    for c in dialog_list:
        if body['dialog_step'] in c.keys:
            message, attachment = c.process(body)
    return message, attachment


def create_answer(data):
    """analyse the branch of dialog and start dialog system"""

    user_id = data['session']['user_id']
    # analyse what step in our dialog
    if data['session']['new']:
        data['dialog_step'] = 'new_session'
        # remember the step of dialog for this user
        cache.set(user_id, "1", 86400)
    elif data['request']['command'] == 'ссылка':
        iteration_num = int(cache.get(user_id))
        iteration_num += 1
        cache.set(user_id, str(iteration_num), 86400)
        data['dialog_step'] = 'user_ask_link'
    elif data['request']['command'].lower().replace(' ', '') == 'помощь':
        iteration_num = int(cache.get(user_id))
        iteration_num += 1
        cache.set(user_id, str(iteration_num), 86400)
        data['dialog_step'] = 'user_ask_help'
    elif data['request']['command'].lower().replace(' ', '') == 'чтотыумеешь':
        iteration_num = int(cache.get(user_id))
        iteration_num += 1
        cache.set(user_id, str(iteration_num), 86400)
        data['dialog_step'] = 'what_you_can'
    elif cache.get(user_id+'-afterlink') == "1":
        iteration_num = int(cache.get(user_id))
        iteration_num += 1
        cache.set(user_id, str(iteration_num), 86400)
        data['dialog_step'] = 'after_link'
    else:
        iteration_num = int(cache.get(user_id))
        iteration_num += 1
        cache.set(user_id, str(iteration_num), 86400)
        data['dialog_step'] = 'user_lookfor_book'

    message, attachment = get_answer(body=data)
    return message, attachment
