import api_alice.dialog_system as dialog_system
from genres.models import GenreNew, ParentGenre
from books.models import Book
from django.core.cache import cache
from operator import and_, or_
from functools import reduce
from django.db.models import Q


def hello(data):
    message = {}
    message['text'] = 'Привет! Я нахожу лучшую книгу в выбранном жанре за год или промежуток годов. Ты можешь сказать ' \
             'название жанра и период. Например - фантастика ' \
             'за 2017-2018 года.'
    return message, ''

hello_command = dialog_system.Dialog()

hello_command.keys = ['new_session']
hello_command.description = ''
hello_command.process = hello


def find_book(data):
    """find the book as user request = genres + range of years"""
    message = {}
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
    user_request_list = data['request']['original_utterance'].split()
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
            message['text'] = 'Лучшая книга по твоему запросу {}. Ссылка на чтение и скачивание книги скажи мне ' \
                           'Ссылка на книгу. Или сделай новый запрос, жанр и года.'.format(book[0].title)
            # write to caсhe book id
            user_id = data['session']['user_id']
            cache.set(user_id+'-bookid', str(book[0].pk), 86400)
        else:
            message['text'] = 'Чего-то я не смогла ничего найти. Уточни пожалуйста запрос - название жанра и года. Например,' \
                      ' любовная фантастика 2016 2018'
    else:
        message['text'] = 'Чего-то я не смогла ничего найти. Уточни пожалуйста запрос - название жанра и года. Например,' \
                   ' любовная фантастика 2016 2018'

    attachment = ''
    return message, ''

find_command = dialog_system.Dialog()

find_command.keys = ['user_lookfor_book']
find_command.description = ''
find_command.process = find_book


def user_ask_help(data):
    """help for user"""
    message = {}
    user_id = data['session']['user_id']

    message['text'] = 'Все очень просто - назови жанр и год. Например - фантастика 2017 2018 года. ' \
                      'И я выберу для тебя лучшую книгу в этом жанре за эти года.'
    attachment = ''
    return message, ''


link_command = dialog_system.Dialog()

link_command.keys = ['user_ask_help']
link_command.description = ''
link_command.process = user_ask_help


def answer_what_you_can(data):
    """help for user"""
    message = {}
    user_id = data['session']['user_id']

    message['text'] = 'Я умею находить лучшие книги в жанре за выбранный год или года. Например скажи Приключения 2010 год.'
    attachment = ''
    return message, ''


link_command = dialog_system.Dialog()

link_command.keys = ['what_you_can']
link_command.description = ''
link_command.process = answer_what_you_can


def find_link(data):
    """find the book as user request = genres + range of years"""
    message = {}
    user_id = data['session']['user_id']
    book_id = int(cache.get(user_id+'-bookid'))
    book = Book.objects.get(pk=book_id)
    if book:
        if 'screen' in data['meta']['interfaces']:
            message['text'] = 'Ниже кнопочка для перехода на книгу.'
            prompt = [{'title': 'Перейти на книгу', 'url': 'https://libs.ru/book/'+str(book_id)+'/', 'hide': True}]
            message['buttons'] = prompt
        else:
            message['text'] = 'Не могу отобразить ссылку, перейди плиз на дивайс с экраном.'
        cache.set(user_id + '-afterlink', "1", 86400)
    else:
        message['text'] = 'Чего-то я не смогла ничего найти. Уточни пожалуйста запрос - название жанра и года. Например,' \
                  ' любовная фантастика 2016 2018'
    attachment = ''
    return message, ''


link_command = dialog_system.Dialog()

link_command.keys = ['user_ask_link']
link_command.description = ''
link_command.process = find_link


def after_link(data):
    message = {}
    message['text'] = 'Можем продолжить поиск или почитай эту и потом я найду новую.'
    user_id = data['session']['user_id']
    cache.set(user_id + '-afterlink', "2", 86400)
    return message, ''


afterlink_command = dialog_system.Dialog()

afterlink_command.keys = ['after_link']
afterlink_command.description = ''
afterlink_command.process = after_link
