from django.http import JsonResponse, HttpResponse
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from genres.models import GenreNew, ParentGenre
from books.models import Book
from django.core.cache import cache
from operator import and_, or_
from functools import reduce
from django.db.models import Q
import api_alice.messageHandler as messageHandler


@csrf_exempt
def index(request):
    """
        Alice skill 1
        https://github.com/yandex/alice-skills/blob/master/python/buy-elephant/now/api.py
    """

    response = {'error': 'something went wrong'}
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        # init response for Alice
        response = {
            'version': data['version'],
            'session': data['session'],
            'response': {
                'text': '',
                'end_session': False
            },
            'version': '1.0'
        }
        # it was old version --- handle_dialog(request, data, response)
        alice_answer = messageHandler.create_answer(data)
        # alice_answer[0] - texts
        # alice_answer[1] - cards
        response['response'] = alice_answer[0]
    return JsonResponse(response)


@csrf_exempt
def alice_buy(request):
    """
        Alice skill 2
    """

    response = {'error': 'something went wrong'}
    if request.method == 'POST':
        # data = request.POST['data']
        data = json.loads(request.body.decode('utf-8'))
        response = {
            'version': data['version'],
            'session': data['session'],
            'response': {
                'text': 'Здравствуйте! Это мы, хороводоведы.',
                'end_session': False
            },
            'version': '1.0'
        }
    return JsonResponse(response)


# СТАРЫЙ МЕТОД, АРХИВ, МОЖНО УДАЛЯТЬ
def handle_dialog(request, data, res):
    """
        Works with dialogs
    """

    user_id = data['session']['user_id']

    if 'screen' in data:
        screen = True
    else:
        screen = False

    # how initialize session
    # https://stackoverflow.com/questions/2293291/create-a-session-in-django
    # user authentication
    # https://stackoverflow.com/questions/11891322/setting-up-a-user-login-in-python-django-using-json-and-have-no-idea-where-to

    if data['session']['new']:
        res['response']['text'] = 'Выбери какую книгу ты хочешь скачать или прочитать. Ты можешь сказать ' \
                                  'название жанра, книги, автора и за какой период. Например - фантастика ' \
                                  'за 2017-2018 года. Или Пелевин.'
        cache.set(user_id, "1", 86400)
        return

    iteration_num = int(cache.get(user_id))
    iteration_num += 1
    cache.set(user_id, str(iteration_num), 86400)

    user_request_list = data['request']['original_utterance'].split()

    # check for years
    year_list = []
    for x in data['request']['nlu']['entities']:
        if x['type'] == 'YANDEX.NUMBER':
            year_list.append(x['value'])
    if len(year_list) > 0:
        max_year = max(year_list)
        min_year = min(year_list)
    else:
        max_year = 2020
        min_year = 1900

    # genre = GenreNew.objects.filter(name__icontains=data['request']['original_utterance'])
    genre = GenreNew.objects.filter(reduce(or_, [Q(name__icontains=q) for q in user_request_list]))
    if genre or len(year_list) > 0:
        genre_id_list = []
        for x in genre:
            genre_id_list.append(x.pk)
        # find books
        if genre_id_list:
            book = Book.objects.prefetch_related('author', 'genre_new').filter(genre_new__in=genre_id_list,
                                                                               year__gte=min_year, year__lte=max_year)[:5]
        else:
            book = Book.objects.prefetch_related('author', 'genre_new').filter(year__gte=min_year, year__lte=max_year)[:5]
        if book:
            res['response']['text'] = 'Лучшая книга по твоему запросу {}. Ссылка на чтение и скачивание книги скажи мне ' \
                                      'Ссылка. Следующая книга в рейтинге - скажи Далее.'\
                                        .format(book[0].title)
        else:
            res['response']['text'] = 'Чего-то я не смогла ничего найти. Уточни пожалуйста запрос - название жанра и года. Например,' \
                                      ' любовная фантастика 2016 2018'
    else:
        res['response']['text'] = 'Чего-то я не смогла ничего найти. Уточни пожалуйста запрос - название жанра и года. Например,' \
                      ' любовная фантастика 2016 2018'
