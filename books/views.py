import datetime
import json
import decimal
import requests
from django.db.models import Sum
from django.core.cache import cache
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.db.models.functions import Lower
from books.models import Book
from authors.models import Author
from views.models import View
from genres.models import GenreNew
from series.models import Series
from publications.models import Publication
from collection.models import Collection
from libs.graphqlclient import execude_libsagregator
from litresapi import LitresApi
from json_store.models import JsonStore
from json_store.views import update_book
from manager.models import BookPartnerLink
from subscribe.views import send_notify


def book_list(request):
    books = Book.objects.prefetch_related('author', 'genre_new').filter()
    page = request.GET.get('page', 1)

    paginator = Paginator(books, settings.PAGE_SIZE)
    count = paginator.count

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    to_template = {
        'books': books,
        'count': count,
        'page': page
    }
    return render(request, 'books/book_list.html', to_template)


def book_detail(request, pk=None):
    try:
        book = Book.objects.prefetch_related('author', 'genre_new').get(pk=pk)
    except Book.DoesNotExist:
        raise Http404()

    try:
        view = View.objects.get(book_id=pk, date=datetime.date.today())
        view.views += 1
        view.save(update_fields=['views'])

        book.show_counter += 1
        book.save(update_fields=['show_counter'])
    except View.MultipleObjectsReturned:
        print('Федя задвоение книги в просмотрах book_id {}'.format(pk))
    except View.DoesNotExist:
        view = View(book_id=pk)
        view.save()
    except Exception as e:
        print('Exception book_detail {}'.format(e))

    # посты
    posts = Publication.objects.filter(book__id=pk)

    try:
        json_store = JsonStore.objects.get(book=book)
    except JsonStore.DoesNotExist:
        json_store = update_book(pk)

    is_admin = False
    if request.user.is_authenticated and request.user.is_staff:
        is_admin = True

    # Получает id книги в литресе для чтения отрывка
    to_template = {
        'book': book,
        'posts': posts,
        'author_books': json_store.data.get('author_books'),
        'related_books': json_store.data.get('related_books'),
        'series_books': json_store.data.get('series_books'),
        'is_admin': is_admin,
        'rating_count': json_store.data.get('rating_count'),
        'awards': Collection.objects.filter(is_award=True, book=book)
    }

    if not to_template['rating_count'] and book.rating > 0:
        to_template['rating_count'] = 1

    return render(request, 'books/book_detail.html', to_template)


@csrf_exempt
def genre_place(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        book_id = int(data.get('book_id'))
        genre_id = int(data.get('genre_id'))

        cache_tag = 'genreplace{}{}'.format(book_id, genre_id)
        place = cache.get(cache_tag)
        if place is None:
            if book_id and genre_id:
                # место книги в жанре
                i = 1
                books = Book.objects.filter(genre_new=genre_id).values('id')

                for book in books:
                    if book['id'] == book_id:
                        place = i
                    else:
                        i += 1

                cache.set(cache_tag, place, 86400)
    except ValueError:
        place = 0

    return JsonResponse({'place': place})


@csrf_exempt
def year_place(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        book_id = int(data.get('book_id'))
        year = int(data.get('year'))

        cache_tag = 'yearplace{}{}'.format(book_id,year)
        place = cache.get(cache_tag)
        if place is None:
            if book_id and year:
                # место книги в жанре
                i = 1
                books = Book.objects.filter(year=year).values('id')

                for book in books:
                    if book['id'] == book_id:
                        place = i
                    else:
                        i += 1

                cache.set(cache_tag, place, 86400)
    except ValueError:
        place = 0

    return JsonResponse({'place': place})


@csrf_exempt
def genre_year_place(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        book_id = int(data.get('book_id'))
        genre_id = int(data.get('genre_id'))
        year = int(data.get('year'))

        cache_tag = 'genreyearplace{}{}{}'.format(book_id, year, genre_id)
        place = cache.get(cache_tag)
        if place is None:
            if book_id and genre_id:
                # место книги в жанре
                i = 1
                books = Book.objects.filter(genre_new=genre_id, year=year).values('id')

                for book in books:
                    if book['id'] == book_id:
                        place = i
                    else:
                        i += 1
                cache.set(cache_tag, place, 86400)
    except Exception:
        place = 0

    return JsonResponse({'place': place})


@csrf_exempt
def vue_get_books(request):
    data = json.loads(request.body.decode('utf-8'))

    sort = data.get('sort', '-rating')
    page = data.get('page', 1)
    genre_id = data.get('genre_id')
    start_year = data.get('start_year')
    end_year = data.get('end_year')

    if sort == '-rating':
        books = Book.objects.prefetch_related('author', 'genre_new').filter()
    else:
        books = Book.objects.prefetch_related('author', 'genre_new').filter().order_by(sort)

    if start_year:
        books = books.filter(year__gte=start_year)

    if end_year:
        books = books.filter(year__lte=end_year)

    if genre_id:
        books = books.filter(genre_new=genre_id)

    paginator = Paginator(books, settings.PAGE_SIZE)
    count = paginator.count

    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    books_list = []
    for book in books:
        item = {
            'id': book.id,
            'url': book.get_absolute_url(),
            'title': book.title,
            'description': book.description,
            'rating': book.rating,
            'authors': book.get_link_authors(),
            'genres': book.get_link_genres(),
            'year': book.year,
            'show_counter': book.show_counter,
            'image': book.get_image_preview()
        }

        books_list.append(item)

    return JsonResponse({'books': books_list, 'count': count})


def update_ratings():
    query = '''
             query books_rating($page: Int, $token: String) {
              books_rating(page: $page, token: $token) {
                libs_book_id
                rating
                flibusta {
                  id
                  flibusta_rates_quantity
                  flibusta_book_genre {
                    flibusta_id
                  }
                }
              }
            }
            '''

    page = 1
    result = True
    while result:
        params = {'page': page}
        response = execude_libsagregator(query=query, params=params)
        books_rating = response.get('books_rating')
        if len(books_rating):
            for book_rating in books_rating:
                rating = decimal.Decimal(book_rating.get('rating', 0))
                libs_book_id = book_rating.get('libs_book_id')
                flibusta = book_rating.get('flibusta')
                genres = []
                rating_partner_votes = 0

                if rating:
                    rating_partner_votes = 1

                if flibusta:
                    flibusta_book_genres = flibusta.get('flibusta_book_genre')
                    rating_partner_votes = flibusta.get('flibusta_rates_quantity', 0)
                    for flibusta_book_genre in flibusta_book_genres:
                        gs = GenreNew.objects.filter(flibusta_id=flibusta_book_genre.get('flibusta_id'))
                        for g in gs:
                            genres.append(g.id)

                try:
                    book = Book.objects.get(pk=libs_book_id)
                    book.rating = round(rating, 2)
                    book.rating_partner_votes = rating_partner_votes
                    book.save(update_fields=['rating', 'rating_partner_votes'])

                    if len(genres) and book.created_by_id != 5227 and book.modified_by_id != 5227:
                        genres_new = book.genre_new.all()
                        for genre_new in genres_new:
                            if genre_new not in genres:
                                genres.append(genre_new.id)
                        if len(genres) > len(genres_new):
                            book.genre_new.set(genres)

                    # Обновляет данные о книге в JsonStore
                    update_book(libs_book_id)

                except Book.DoesNotExist:
                    print('Этой книги нет на либсе {}'.format(book_rating))
            page += 1
        else:
            print('Перебрал все книги')
            result = False


def update_genres():
    books = Book.objects.prefetch_related('author', 'genre_new').filter()

    for book in books:
        new_genres = []
        old_genres = list(book.genre.all().values('id'))
        for old_genre in old_genres:
            # Тут слияние нескольких жанров в 1
            if old_genre['id'] == 50 or old_genre['id'] == 52:
                new_genres.append(50)
            elif old_genre['id'] == 20 or old_genre['id'] == 3:
                new_genres.append(19)
            else:
                # Для остальных поиск по новым жанрам
                try:
                    genre_new = GenreNew.objects.get(litres_id=old_genre['id'])
                    new_genres.append(genre_new.id)
                except GenreNew.DoesNotExist:
                    print("книга {} новые жанры {} старые жанры {}".format(book.id, new_genres, old_genres))
                except GenreNew.MultipleObjectsReturned:
                    genres_new = GenreNew.objects.filter(litres_id=old_genre['id'])
                    for genre_new in genres_new:
                        new_genres.append(genre_new.id)

        book.genre_new.set(new_genres)


def import_books(request):
    if not request.user.is_staff:
        return redirect('/')
    return render(request, 'books/import_books.html')


def editor(request, pk=None):
    if not request.user.is_staff:
        return redirect('/')
    return render(request, 'books/editor.html', {'id': pk})


@csrf_exempt
def vue_book_editor_get(request):
    book_dict = {}
    if request.user.is_authenticated and request.user.is_staff:

        data = json.loads(request.body.decode('utf-8'))

        id = data.get('id', None)

        if id:
            book = Book.objects.get(pk=id)
            genre_new = book.genre_new.all()
            authors = book.author.all()
            awards = book.award.all()

            book_dict = {
                'title': book.title,
                'description': book.description,
                'genre_new': [],
                'authors': [],
                'age': book.age,
                'year': book.year,
                'nr_series': book.nr_series,
                'rating': book.rating,
                'manual_rating': book.manual_rating,
                'status': book.status,
                'awards': []
            }

            if book.series:
                book_dict['series'] = {'id': book.series_id, 'title': book.series.title}

            if book.image:
                if 'http' in book.image.url:
                    book_dict['image'] = book.image.url.replace('/media/', '').replace('%3A', ':')
                else:
                    book_dict['image'] = book.image.url

            genres_list = []
            for genre in genre_new:
                item = {
                    'id': genre.id,
                    'name': genre.name
                }

                genres_list.append(item)

            book_dict['genres'] = genres_list

            authors_list = []
            for author in authors:
                item = {
                    'id': author.id,
                    'name': author.name
                }

                authors_list.append(item)

            book_dict['authors'] = authors_list

            awards_list = []
            for award in awards:
                item = {
                    'id': award.id,
                    'name': award.name
                }

                awards_list.append(item)

            book_dict['awards'] = awards_list

        genres_all = list(GenreNew.objects.all().values('id', 'name'))

    return JsonResponse({'book': book_dict, 'genres': genres_all})


@csrf_exempt
def vue_book_save(request):
    if request.user.is_authenticated and request.user.is_staff:
        image = request.FILES.get('image')

        data = request.POST.get('data')
        data = json.loads(data)

        id = data.get('id', None)
        title = data.get('title')
        description = data.get('description')
        genre_new = data.get('genres', None)
        authors = data.get('authors', None)
        age = data.get('age', None)
        year = data.get('year', None)
        series = data.get('series', None)
        nr_series = data.get('nr_series', None)
        status = data.get('status', None)
        manual_rating = data.get('manual_rating', 0)
        awards = data.get('awards', None)

        if status == 'true':
            status = True
        elif status == 'false':
            status = False

        if id:
            # Сохраняет изменения в книге
            book = Book.objects.get(pk=id)
            book.title = title
            book.description = description
            book.genre_new.set(genre_new)
            book.award.set(awards)
            book.author.set(authors)
            book.age = age
            book.year = year
            book.series_id = series
            book.nr_series = nr_series
            book.manual_rating = float(manual_rating)
            book.status = status
            book.modified_by = request.user
            book.save()
        else:
            # Создает новую книгу
            book = Book(
                title=title,
                description=description,
                age=age,
                year=year,
                series_id=series,
                nr_series=nr_series,
                status=status,
                created_by = request.user,
                modified_by = request.user,
                manual_rating=decimal.Decimal(manual_rating)
            )

            book.save()

            if genre_new:
                book.genre_new.set(genre_new)

            if authors:
                book.author.set(authors)

            if awards:
                book.award.set(awards)

        if image:
            book.image.save(image.name, image)

    return JsonResponse({'id': book.id})


@csrf_exempt
def vue_collection_editor_books_get(request):
    books_list = []

    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))

        title = data.get('title')

        books = Book.objects.annotate(lower_title=Lower('title')).order_by('title')
        books = books.filter(lower_title__startswith=title.lower())[:30]

        for book in books:
            item = {
                'id': book.id,
                'title': "{}, {}".format(book.title, book.get_text_authors())
            }

            books_list.append(item)

    return JsonResponse({'books': books_list})


@csrf_exempt
def vue_book_editor_authors_get(request):
    data = json.loads(request.body.decode('utf-8'))

    name = data.get('name')

    authors = Author.objects.annotate(lower_name=Lower('name')).order_by('name')
    authors = authors.filter(lower_name__startswith=name.lower())[:30]

    authors_list = []
    for author in authors:
        item = {
            'id': author.id,
            'name': author.name
        }
        authors_list.append(item)

    return JsonResponse({'authors': authors_list})


@csrf_exempt
def vue_book_editor_series_get(request):
    series_list = []
    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))

        title = data.get('title')

        series = Series.objects.annotate(lower_title=Lower('title')).order_by('title')
        series = series.filter(lower_title__startswith=title.lower())[:30]

        for serie in series:
            item = {
                'id': serie.id,
                'title': serie.title
            }

            series_list.append(item)

    return JsonResponse({'series': series_list})


@csrf_exempt
def vue_get_import_books(request):
    books = Book.objects.prefetch_related('author', 'genre_new').filter(status=None)[0:10]

    books_list = []
    for book in books:
        item = {
            'id': book.id,
            'url': book.get_absolute_url(),
            'title': book.title,
            'description': book.description,
            'rating': book.rating,
            'authors': book.get_link_authors(),
            'genres': book.get_link_genres(),
            'year': book.year,
            'show_counter': book.show_counter,
            'status': book.status,
            'image': book.get_image()
        }

        books_list.append(item)

    return JsonResponse({'books': books_list})


@csrf_exempt
def vue_set_import_books_status(request):
    if request.user.is_authenticated and request.user.is_staff:
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id')
        status = data.get('status')

        if id:
            book = Book.objects.get(pk=id)
            book.status = status
            book.save(update_fields=['status'])

        return JsonResponse({'book': book.id})


def import_from_litres(hour=23, minutes=59):
    image_template = 'https://partnersdnld.litres.ru/static/bookimages/{0}/{1}/{2}/{3}.bin.dir/{3}.cover.{4}'
    d = datetime.date.today()
    api = LitresApi(secret_key='D7psdo2s*Xjsoq3WdsoSWWvoo', partner_id='YABK')
    lazy_books = api.get_fresh_book(
        start_date=datetime.datetime(d.year, d.month, d.day-1, 0, 0),
        end_date=datetime.datetime(d.year, d.month, d.day-1, hour, minutes)
    )

    for lazy_book in lazy_books:
        if lazy_book.get('@lang') == 'ru':
            litres_id = lazy_book.get('@id')
            litres_file_id = lazy_book.get('@file_id')
            litres_book = lazy_book.get('title-info')
            litres_authors = litres_book.get('author')
            litres_genres = lazy_book.get('genres')
            litres_series = lazy_book.get('sequences')
            title = litres_book.get('book-title')
            description = litres_book.get('annotation')
            age = lazy_book.get('@adult')

            try:
                publish_info = lazy_book.get('publish-info')
                if publish_info:
                    year = publish_info.get('year', 0)
                    isbn = publish_info.get('isbn', '').replace('-', '')
                else:
                    date = litres_book.get('date', 0)
                    if type(date) is str:
                        year = date
                    elif type(date) is list:
                        if date.get('#text'):
                            year = date.get('#text', 0)

                    if lazy_book.get('@isbn'):
                        isbn = lazy_book.get('@isbn', '').replace('-', '')
                    else:
                        isbn = lazy_book.get('@litres_isbn', '').replace('-', '')
            except Exception as e:
                print('Exception {}'.format(e))
                print(json.dumps(lazy_book, indent=4, ensure_ascii=False))

            ext = lazy_book.get('@cover')
            rating = decimal.Decimal(lazy_book.get('@rating', 0))

            # Импорт автора
            libs_authors = []
            for litres_author in litres_authors:
                try:
                    author = Author.objects.get(litres_id=litres_author.get('id'))
                    libs_authors.append(author.id)
                except Author.DoesNotExist:
                    fi = "{} {}".format(litres_author.get('last-name'), litres_author.get('first-name'))
                    fi = fi.replace('None', '').strip()
                    authors = Author.objects.filter(name__icontains=fi)
                    if len(authors) == 1:
                        author = authors[0]
                        libs_authors.append(author.id)
                        author.litres_id = litres_author.get('id')
                        author.save(update_fields=['litres_id'])
                        print("Обновил litres_id для автора {} {}".format(author.id, author.name))
                    elif len(authors) > 1:
                        print("Множество совпадений авторов {} для книги {}".format(litres_authors, litres_book))
                    else:
                        fi = "{} {}".format(litres_author.get('first-name'), litres_author.get('last-name'))
                        fi = fi.replace('None', '').strip()
                        authors = Author.objects.filter(name__icontains=fi)
                        if len(authors) == 1:
                            author = authors[0]
                            libs_authors.append(author.id)
                            author.litres_id = litres_author.get('id')
                            author.save(update_fields=['litres_id'])
                            print("Обновил litres_id для автора {} {}".format(author.id, author.name))
                        elif len(authors) > 1:
                            print("Множество совпадений авторов {} для книги {}".format(litres_authors, litres_book))
                        else:
                            # Добавляет нового автора

                            fi = "{} {}".format(litres_author.get('last-name'), litres_author.get('first-name'))
                            fio = "{} {} {}".format(
                                litres_author.get('last-name', ''),
                                litres_author.get('first-name', ''),
                                litres_author.get('middle-name', '')
                            )

                            author = Author(
                                name=fi.replace('None', '').strip(),
                                litres_name=fio.replace('None', '').strip(),
                            )
                            author.save()
                            libs_authors.append(author.id)

            # Опрееление жанра
            libs_genres = []
            if litres_genres:
                litres_genres = litres_genres['genre']
                for litres_genre in litres_genres:
                    genres_new = GenreNew.objects.filter(genre_litres__icontains=litres_genre['@id'])

                    for genre_new in genres_new:
                        libs_genres.append(genre_new.id)

                    if not len(genres_new):
                        print("Жанр {} {} не найден".format(litres_genre['@title'], litres_genre['@id']))

            # Если есть серия
            libs_series = None
            if litres_series:
                litres_series = litres_series.get('sequence')[0]
                try:
                    # Проверяет по id
                    libs_series = Series.objects.get(litres_id=litres_series['@uuid'])
                except Series.DoesNotExist:
                    try:
                        # проверяет по названию
                        libs_series = Series.objects.get(title=litres_series['@name'])
                        libs_series.litres_id = litres_series['@uuid']
                        libs_series.save(update_fields=['litres_id'])
                        print("Обновил litres_id для серии {} {}".format(libs_series.id, libs_series.title))
                    except Series.MultipleObjectsReturned:
                        print("Задвоилась серия {} {}".format(libs_series.id, libs_series.title))
                    except Series.DoesNotExist:
                        # Добавляет новую серию
                        libs_series = Series(
                            title=litres_series['@name'],
                            litres_id=litres_series['@uuid']
                        )
                        libs_series.save()

            # Ипорт книги
            try:
                book = Book.objects.get(litres_id=litres_id)
            except Book.MultipleObjectsReturned:
                print("Затроило книги litres_id {} isbn {}".format(litres_id, isbn))
            except Book.DoesNotExist:
                # Проверяет по isbn
                try:
                    if len(isbn):
                        book = Book.objects.get(isbn=isbn)
                        book.litres_id = litres_id
                        book.save(update_fields=['litres_id'])
                        print("Обновил litres_id для книги {} {}".format(book.id, book.title))
                    else:
                        print("Пустой isbn litres_id {} isbn {}".format(litres_id, isbn))
                except Book.MultipleObjectsReturned:
                    print("Затроило книги litres_id {} isbn {}".format(litres_id, isbn))
                except Book.DoesNotExist:
                    # Проверяет совпадение по назанию
                    if title and litres_author.get('last-name'):
                        book = Book.objects.filter(title__icontains=title, author__name__icontains=litres_author.get('last-name'))
                        if len(book) == 1:
                            b = book[0]
                            b.litres_id = litres_id
                            b.isbn = isbn
                            b.save(update_fields=['litres_id', 'isbn'])
                            print("Обновил litres_id и isbn для книги {} {}".format(b.id, b.title))
                        elif len(book) > 1:
                            print("Множество совпадений c книгой {}".format(litres_book))
                        else:
                            litres_file_id_str = "{0:08d}".format(int(litres_file_id))
                            xx = litres_file_id_str[0:2]
                            yy = litres_file_id_str[2:4]
                            zz = litres_file_id_str[4:6]

                            image = image_template.format(xx, yy, zz, litres_file_id, ext)

                            if rating >= 4:
                                rating = 4

                            book = Book(
                                title=title,
                                description=description,
                                age=age,
                                year=year,
                                isbn=isbn,
                                litres_id=litres_id,
                                image=image,
                                rating=rating
                            )

                            if decimal.Decimal(rating) > 0:
                                book.rating_partner_votes = 1

                            if libs_series:
                                book.series = libs_series
                            try:
                                book.save()
                            except decimal.InvalidOperation:
                                book.rating = 0
                                book.save()

                            book.genre_new.set(libs_genres)
                            book.author.set(libs_authors)


def delete_quot():
    books = Book.objects.filter(description__contains='Array')
    for book in books:
        book.description = book.description.replace('Array', '')
        book.save(update_fields=['description'])


def read(request, pk=None):
    """Страница читать онлайн, каждый раз подгружает текс с литреса........"""
    try:
        book = Book.objects.get(pk=pk)
        if book.litres_id:
            link = "https://partnersdnld.litres.ru/pub/t/{}.txt".format(book.litres_id)
            result = requests.get(link)

            if result.status_code == 200:
                result.encoding = "cp1251"
                text = result.text

                try:
                    text = text.split('Конец ознакомительного фрагмента', 1)[0]
                except Exception as e:
                    print('Exception read line 821 {} book id {}'.format(e, book.id))

                collections = Collection.objects.filter(book=book)
                collections_list = []
                for collection in collections:
                    collections_list.append('<a href="{}">{}</a>'.format(collection.get_absolute_url(), collection.title))

                series = None
                if book.series:
                    series = book.series.get_absolute_url(),

                count = 2000
                start = 0
                end = count
                text_part = []

                while len(text[start:end]):
                    text_part.append(text[start:end].replace('\r\n', '<br />'))
                    start += count
                    end += count


                to_template = {
                    'id': book.id,
                    'title': book.title,
                    'author': book.get_author(),
                    'text': text,
                    'text_part': text_part,
                    'book_url': book.get_absolute_url(),
                    'read_url': book.get_read_url(),
                    'len': len(text),
                    'rating': book.rating,
                    'authors': book.get_link_authors(),
                    'series': series,
                    'genres': book.get_link_genres(),
                    'collections': ", ".join(collections_list)
                }
            else:
                raise Http404()
        else:
            raise Http404()
    except Book.DoesNotExist:
        raise Http404()

    return render(request, 'books/read.html', to_template)


@csrf_exempt
def vue_set_litres_id(request):
    data = json.loads(request.body.decode('utf-8'))
    litres_book_id = data.get('litres_book_id')
    book_id = data.get('book_id')
    isbn = data.get('isbn')

    try:
        book = Book.objects.get(pk=book_id)

        if not book.litres_id:
            book.litres_id = litres_book_id
            book.save(update_fields=['litres_id'])
        if not book.isbn and isbn:
            book.isbn = isbn
            book.save(update_fields=['isbn'])

    except Book.DoesNotExist:
        pass

    return JsonResponse({'result': 'ok'})


def test_book_detail(request, pk=None):
    try:
        book = Book.objects.prefetch_related('author', 'genre_new').get(pk=pk)
    except Book.DoesNotExist:
        raise Http404()

    try:
        view = View.objects.get(book_id=pk, date=datetime.date.today())
        view.views += 1
        view.save(update_fields=['views'])

        book.show_counter += 1
        book.save(update_fields=['show_counter'])
    except View.MultipleObjectsReturned:
        print('Федя задвоение книги в просмотрах book_id {}'.format(pk))
    except View.DoesNotExist:
        view = View(book_id=pk)
        view.save()
    except Exception as e:
        print('Exception test_book_detail {}'.format(e))

    # посты
    posts = Publication.objects.filter(book__id=pk)

    try:
        json_store = JsonStore.objects.get(book=book)
    except JsonStore.DoesNotExist:
        json_store = update_book(pk)

    is_admin = False
    if request.user.is_authenticated and request.user.is_staff:
        is_admin = True

    # Получает id книги в литресе для чтения отрывка
    to_template = {
        'book': book,
        'posts': posts,
        'author_books': json_store.data.get('author_books'),
        'related_books': json_store.data.get('related_books'),
        'series_books': json_store.data.get('series_books'),
        'is_admin': is_admin,
        'rating_count': json_store.data.get('rating_count')
    }

    if not to_template['rating_count'] and book.rating > 0:
        to_template['rating_count'] = 1

    return render(request, 'books/test_book_detail.html', to_template)


@csrf_exempt
def vue_book_partner_link(request):
    """
    Записывает книги укоторых < 3 партнерских ссылок.
    Удаляет если ссылок стало больше >= 3
    """
    data = json.loads(request.body.decode('utf-8'))
    book_id = data.get('book_id')
    count_partner_link = data.get('count_partner_link')

    if count_partner_link == 0:
        views = View.objects.filter(book_id=book_id).values("book_id").annotate(
            views=Sum('views'))

        try:
            view = views[0].get('views', 0)
        except Exception as e:
            print(e)

        try:
            book_partner_link = BookPartnerLink.objects.get(book_id=book_id)
            book_partner_link.count_partner_link = count_partner_link
            book_partner_link.views = view
            book_partner_link.save()
            content = {
                'info': 'Книга обновлена в журнале'
            }
            return JsonResponse(content)
        except BookPartnerLink.DoesNotExist:
            BookPartnerLink(
                book_id=book_id,
                count_partner_link=count_partner_link,
                views=view
            ).save()
            content = {
                'info': 'Книга добавлена в журнал'
            }
            return JsonResponse(content)
        except BookPartnerLink.MultipleObjectsReturned:
            BookPartnerLink.objects.filter(book_id=book_id)[0].delete()
            content = {
                'info': 'Удален дубликат книги из журнала'
            }
            return JsonResponse(content)
    else:
        try:
            book_partner_link = BookPartnerLink.objects.filter(book_id=book_id)

            if len(book_partner_link):
                # Выслать уведомление подписчикам
                send_notify(book_id)

                book_partner_link.delete()

            content = {
                'info': 'Книга удалена'
            }

            return JsonResponse(content)
        except BookPartnerLink.DoesNotExist:
            pass
