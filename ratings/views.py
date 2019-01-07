import datetime
import json
import decimal
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from dateutil import relativedelta
from django.http import Http404
from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from books.models import Book
from views.models import View
from json_store.views import update_book
from ratings.models import StarRatings
from libs.graphqlclient import execude_libsagregator


@csrf_exempt
def author_set(request):
    to_template = {}
    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))
        author_id = data.get('author_id')
        user_rating = data.get('rating')

        if author_id and user_rating:
            try:
                rating = StarRatings.objects.get(user=request.user, author_id=author_id)
                rating.rating = user_rating
                rating.save()
            except StarRatings.DoesNotExist:
                StarRatings(user=request.user, rating=user_rating, author_id=author_id).save()

            to_template['result'] = 1
    else:
        to_template['result'] = 0
        to_template['auth'] = False

    return JsonResponse(to_template)


@csrf_exempt
def book_set(request):
    to_template = {}
    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))
        book_id = data.get('book_id')
        user_rating = data.get('rating')

        if book_id and user_rating:
            try:
                rating = StarRatings.objects.get(user=request.user, book_id=book_id)
                rating.rating = user_rating
                rating.save()
            except StarRatings.DoesNotExist:
                StarRatings(user=request.user, rating=user_rating, book_id=book_id).save()

            to_template['result'] = 1

            # Пересчитыает общий рейтинг книги
            try:
                book = Book.objects.get(pk=book_id)

                query = '''
                        query book_rating($libs_book_id: Int, $token: String) {
                              book_rating(libs_book_id: $libs_book_id, token: $token) {
                                rating
                              }
                            }
                        '''
                params = {'libs_book_id': book.id}

                result = execude_libsagregator(query=query, params=params)
                count = 0

                if book.manual_rating:
                    manual_rating = decimal.Decimal(book.manual_rating) * 1
                    count += 1
                else:
                    manual_rating = 0

                # Агрегированный рейтинг
                partners_rating = 0
                if result.get('book_rating'):
                    book_rating = result.get('book_rating')
                    partners_rating = decimal.Decimal(book_rating.get('rating', 0))
                    if partners_rating:
                        count += 1

                # Пользовательский рйтинг
                user_rating = decimal.Decimal(StarRatings.objects.filter(book=book).aggregate(Avg('rating'))['rating__avg'])
                if user_rating:
                    count += 1
                else:
                    user_rating = 0

                rating = round((manual_rating + partners_rating + user_rating) / count, 2)

                book.rating = rating
                book.save(update_fields=['rating'])

                # Обновляет данные о книге в JsonStore
                update_book(book.id)

            except Book.DoesNotExist:
                pass

    else:
        to_template['result'] = 0
        to_template['auth'] = False

    return JsonResponse(to_template)


@csrf_exempt
def publication_set(request):
    to_template = {}
    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))
        publication_id = data.get('publication_id')
        user_rating = data.get('rating')

        if publication_id and user_rating:
            try:
                rating = StarRatings.objects.get(user=request.user, publication_id=publication_id)
                rating.rating = user_rating
                rating.save()
            except StarRatings.DoesNotExist:
                StarRatings(user=request.user, rating=user_rating, publication_id=publication_id).save()

            to_template['result'] = 1
    else:
        to_template['result'] = 0
        to_template['auth'] = False

    return JsonResponse(to_template)


@csrf_exempt
def collection_set(request):
    to_template = {}
    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))
        collection_id = data.get('collection_id')
        user_rating = data.get('rating')

        if collection_id and user_rating:
            try:
                rating = StarRatings.objects.get(user=request.user, collection_id=collection_id)
                rating.rating = user_rating
                rating.save()
            except StarRatings.DoesNotExist:
                StarRatings(user=request.user, rating=user_rating, collection_id=collection_id).save()

            to_template['result'] = 1
    else:
        to_template['result'] = 0
        to_template['auth'] = False

    return JsonResponse(to_template)


def all(request):
    """Страница все рейтинги."""
    return render(request, 'ratings/all.html')


def best_for_today(request):
    """Страница Лучшие книги дня"""
    datetime_utc = datetime.datetime.utcnow()
    datetime_book_utc = datetime.datetime.utcnow() - datetime.timedelta(days=7)
    books = View.objects.filter(
        date__gte=datetime_utc,
        book__isnull=False,
        book__is_active=True,
        book__date_create__gte=datetime_book_utc
    ).values("book_id").annotate(views=Sum('views'))[:50]

    books_list = []
    for book in books:
        try:
            book = Book.objects.get(id=book['book_id'])
            books_list.append(book)
        except Book.DoesNotExist:
            pass

    to_template = {
        "books": books_list
    }

    return render(request, 'ratings/best_for_day.html', to_template)


def best_for_week(request):
    """Страница Лучшие книги дня"""

    datetime_utc = datetime.datetime.utcnow()  - datetime.timedelta(days=7)
    datetime_book_utc = datetime.datetime.utcnow() - datetime.timedelta(days=30)

    books = View.objects.filter(
        date__gte=datetime_utc,
        book__isnull=False,
        book__date_create__gte=datetime_book_utc
    ).values("book_id").annotate(views=Sum('views'))[:50]

    books_id = []
    for book in books:
        books_id.append(book['book_id'])
    books = Book.objects.prefetch_related('author', 'genre_new').filter(id__in=books_id)

    to_template = {
        "books": books
    }
    return render(request, 'ratings/best_for_week.html', to_template)


# @cache_page(3600, cache='default', key_prefix='best_for_month')
def best_for_month(request):
    """Страница Лучшие книги дня"""

    datetime_utc = datetime.datetime.utcnow()  - datetime.timedelta(days=30)
    books = View.objects.filter(
        date__gte=datetime_utc,
        book__isnull=False
    ).values("book_id").annotate(views=Sum('views'))[:50]

    books_id = []
    for book in books:
        books_id.append(book['book_id'])
    books = Book.objects.prefetch_related('author', 'genre_new').filter(id__in=books_id)

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_for_month.html', to_template)


# @cache_page(86400, cache='default', key_prefix='best_sellers')
def best_sellers(request):
    """Страница Лучшие книги дня"""

    datetime_utc = datetime.datetime.utcnow()  - datetime.timedelta(days=100)
    books = View.objects.filter(
        date__gte=datetime_utc,
        book__isnull=False
    ).values("book_id").annotate(views=Sum('views'))[:50]

    books_id = []
    for book in books:
        books_id.append(book['book_id'])
    books = Book.objects.prefetch_related('author', 'genre_new').filter(id__in=books_id)

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_sellers.html', to_template)


# @cache_page(86400, cache='default', key_prefix='best_world')
def best_world(request):
    """Страница Лучшие книги дня"""

    datetime_utc = datetime.datetime.utcnow()  - datetime.timedelta(days=50)
    books = View.objects.filter(
        date__gte=datetime_utc,
        book__isnull=False
    ).values("book_id").annotate(views=Sum('views'))[:100]

    books_id = []
    for book in books:
        books_id.append(book['book_id'])
    books = Book.objects.prefetch_related('author', 'genre_new').filter(id__in=books_id)

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_world.html', to_template)


# @cache_page(86400, cache='default', key_prefix='best_russian')
def best_russian(request):
    """Страница Лучшие русские книги"""
    #books = Book.objects.prefetch_related('author', 'genre_new').filter(author__nationality__slug='russian')[:100]
    books = Book.objects.prefetch_related('author', 'genre_new').filter(
        author__nationality__slug='russian'
    ).annotate(count=Count('pk')).order_by('-rating', 'pk')[:100]

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_russian.html', to_template)


# @cache_page(86400, cache='default', key_prefix='best_year')
def best_year(request, year=None):
    """Страница Лучшие книги за год...../"""
    if 1800 > int(year) or int(year) > 2020:
        raise Http404("404 Страница не найдена")

    books = Book.objects.prefetch_related('author', 'genre_new').filter(year=year)[:100]

    to_template = {
        "books": books,
        "year": year
    }

    return render(request, 'ratings/best_year.html', to_template)


# @cache_page(86400, cache='default', key_prefix='best_month_year')
def best_month_year(request, year=None, month=None):
    """Страница Лучшие книги за год"""
    if year < 2017:
        raise Http404("404 Страница не найдена")

    month_ru = {'january': 'Январь', 'february': 'Февраль', 'march': 'Март', 'april': 'Апрель',
                               'may': 'Май', 'june': 'Июнь', 'july': 'Июль', 'august': 'Август',
                               'september': 'Сентябрь',
                               'october': 'Октябрь', 'november': 'Ноябрь', 'december': 'Декабрь'}

    month_list = {
        'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6,
        'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december': 12
    }

    d1 = datetime.date.today()
    d2 = datetime.date(year, month_list.get(month), 1)
    r = relativedelta.relativedelta(d2, d1)

    if r.months >= 3 or r.years > 0:
        raise Http404("404 Страница не найдена")

    m = month_list.get(month)
    if m == 12:
        m = 1
    else:
        m += 1

    books = Book.objects.prefetch_related('author', 'genre_new').filter(
        date_create__year=year,
        date_create__month__gte=month_list.get(month),
        date_create__month__lt=m
    )[:100]

    to_template = {
        "books": books,
        "year": year,
        "month": month_ru.get(month)
    }

    return render(request, 'ratings/best_month_year.html', to_template)


# @cache_page(86400, cache='default', key_prefix='best_genres')
def best_genres(request, year=None):
    """Страница Лучшие книги дня"""

    datetime_utc = datetime.datetime.utcnow()  - datetime.timedelta(days=44)
    books = View.objects.filter(
        date__gte=datetime_utc,
        book__isnull=False,
        book__year=year
    ).values("book_id").annotate(views=Sum('views'))[:50]

    books_id = []
    for book in books:
        books_id.append(book['book_id'])
    books = Book.objects.prefetch_related('author', 'genre_new').filter(id__in=books_id)

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_genres.html', to_template)


def best_popadanci(request):
    """Страница Лучшие книги best_popadanci"""

    datetime_utc = datetime.datetime.utcnow() - datetime.timedelta(days=44)
    books = View.objects.filter(
        date__gte=datetime_utc,
        book__isnull=False,
        book__genre__book_genre__in=[51],
    ).values("book_id").annotate(views=Sum('views'))[:30]

    books_id = []
    for book in books:
        books_id.append(book['book_id'])
    books = Book.objects.prefetch_related('author', 'genre_new').filter(id__in=books_id)

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_popadanci.html', to_template)


def best_magic(request):
    books = Book.objects.prefetch_related('author', 'genre_new').filter(genre__slug="magicheskij-realizm")

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_magic.html', to_template)


def best_100(request):
    """Страница Лучшие книги дня"""
    books = Book.objects.prefetch_related('author', 'genre_new')[:100]

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_100.html', to_template)


def best_libs(request):
    books = Book.objects.prefetch_related('author', 'genre_new').filter()[:100]

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_libs.html', to_template)


def best_online(request):
    books = Book.objects.prefetch_related('author', 'genre_new').filter()[:100]

    to_template = {
        "books": books
    }

    return render(request, 'ratings/best_online.html', to_template)


def clear_all_cache(request):
    if request.user.is_authenticated and request.user.is_staff:
        cache.delete('default')
        cache.clear()
    return render(request, 'ratings/all.html')
