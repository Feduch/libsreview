from json_store.models import JsonStore
from books.models import Book
import bot_vk.command_system as command_system
import bot_vk.vkapi as vkapi
import datetime
from views.models import View
from django.db.models import Sum


def pupular_books_in_genre(genre_id, ago_stat=7, ago_added=30):
    """
    выдает лучшие книги в жанре по просмотрам за последние ago_stat дней,
    среди книг, которые были добавлены в период от сегодня до ago_added дней назад
    """
    date_ago_stat = datetime.datetime.utcnow() - datetime.timedelta(days=ago_stat)
    date_ago_added = datetime.datetime.utcnow() - datetime.timedelta(days=ago_added)

    books = View.objects.filter(
        date__gte=date_ago_stat,
        book__date_create__gte=date_ago_added,
        book__isnull=False,
        book__genre_new=genre_id,
        book__is_active=True
    ).values("book_id").annotate(views=Sum('views'))[:1]

    book = Book.objects.prefetch_related('author', 'genre_new').get(pk=books[0]['book_id'])
    attachment = "https://libs.ru"+book.get_image()

    return book, attachment
