import bot_vk.vkapi as vkapi
import bot_vk.pupular_books_in_genre as pop_book
from django.http import HttpResponse, JsonResponse


def post_to_wall_best_in_genre(subs_group_id=169943927, genre_id=22):
    """
    Постит на стену группы лучшую книгу жанра за последние Х дней
    """
    book = pop_book.pupular_books_in_genre(genre_id)[0]

    message = []
    # TODO сделать выбор случайного приветствия
    message.append('Лучшей книгой этой недели в жанре фэнтези стала')
    message.append('"'+book.title+'"')
    message.append('Общий рейтинг книги')
    message.append(book.rating)
    message.append("Голосуйте за любимые книги – не забывайте, что ваш голос помогает автору понять, "
                   "хороша книга или надо что-то менять. На этом мы прощаемся и на следующей неделе "
                   "сообщим о новой книге, которая наберет наибольшую популярность за 7 дней!")
    res_message = str(" ".join(str(e) for e in message))
    attachment = "https://libs.ru/book/" + str(book.id) + "/"
    vkapi.post_to_wall(subs_group_id, res_message, attachment)
    return HttpResponse('ok', content_type="text/plain")
