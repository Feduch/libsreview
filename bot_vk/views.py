import json
import vk
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import bot_vk.messageHandler as messageHandler
import bot_vk.send_message_to_all as s_m_t_a
import bot_vk.post_to_wall as PostToWall
from bot_vk.appsettings import *


@csrf_exempt
def bot_vk_best_fantasy(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        # Вконтакте в своих запросах всегда отправляет поле типа
        if 'type' not in data.keys():
            return HttpResponse('not vk', content_type="text/plain")
        if data['type'] == 'confirmation':
            return HttpResponse(confirmation_token, content_type="text/plain")
        elif data['type'] == 'message_new':
            messageHandler.create_answer(data['object'], token)
            return HttpResponse('ok', content_type="text/plain")
    else:
        return HttpResponse('not a POST request', content_type="text/plain")


@csrf_exempt
def bot_vk_fantasy_subscr(request):
    s_m_t_a.send_message_all_members(169943927, 22)

@csrf_exempt
def bot_vk_post_to_wall(request):
    PostToWall.post_to_wall_best_in_genre(169943927, 22)

@csrf_exempt
def bot_debug_vk(request):
    token = '********************'
    confirmation_token = '**********'
    # Распаковываем json из пришедшего POST-запроса
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
    #     Вконтакте в своих запросах всегда отправляет поле типа..
        if 'type' not in data.keys():
            return HttpResponse('not vk', content_type="text/plain")
        if data['type'] == 'confirmation':
            return HttpResponse(confirmation_token, content_type="text/plain")
        elif data['type'] == 'message_new':
            session = vk.Session()
            api = vk.API(session, v=5.0)
            user_id = data['object']['from_id']
            api.messages.send(access_token=token, user_id=str(user_id), message=str(data))
            # Сообщение о том, что обработка прошла успешно
            return HttpResponse('ok', content_type="text/plain")
    else:
        return HttpResponse('not a POST request', content_type="text/plain")
