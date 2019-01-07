import datetime
import json
import re
from django.views.decorators.cache import cache_page
from django.http import JsonResponse, Http404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import DetailView
from django.db import connection
from authors.models import Author
from books.models import Book
from views.models import View
from genres.models import GenreNew
from publications.models import Publication


TAG_RE = re.compile(r'<[^>]+>')

def author_list(request):
    authors = Author.objects.filter()
    page = request.GET.get('page', 1)

    paginator = Paginator(authors, settings.PAGE_SIZE)
    count = paginator.count

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    to_template = {
        'authors': authors,
        'count': count,
        'page': page
    }
    return render(request, 'authors/author_list.html', to_template)


class AuthorDetail(DetailView):
    """
    Автор
    """
    model = Author
    context_object_name = 'author'

    def get_object(self):
        object = super(AuthorDetail, self).get_object()
        if not object.is_active:
            raise Http404
        return object

    def get_context_data(self, **kwargs):
        context = super(AuthorDetail, self).get_context_data(**kwargs)
        author = Author.objects.get(pk=self.kwargs['pk'])

        # увеличивает количество просмотров
        try:
            view = View.objects.get(author_id=self.kwargs['pk'], date=datetime.date.today())
            view.views += 1
            view.save(update_fields=['views'])

            author.show_counter += 1
            author.save(update_fields=['show_counter'])
        except View.MultipleObjectsReturned:
            print('Федя задвоение книги в просмотрах author_id {}'.format(self.kwargs['pk']))
        except View.DoesNotExist:
            view = View(author_id=self.kwargs['pk'])
            view.save()
        except Exception as e:
            print('Exception AuthorDetail {} author id {}'.format(e, self.kwargs.get('pk')))

        # Книги автора сгруппированые по сериям
        cursor = connection.cursor()
        sql = "SELECT series_id,series_title,book_id,title,year,rating, string_agg(genre, ';') " \
              "FROM  (SELECT s.id AS series_id, s.title AS series_title, b.id AS book_id, b.title, b.year, b.rating, concat(g.id,':',g.slug,':', g.name) AS genre " \
              "FROM books_book AS b,books_book_author AS b_a, series_series s, books_book_genre_new bg,genres_genrenew g " \
              "WHERE bg.book_id = b.id AND bg.genrenew_id = g.id AND s.id = b.series_id AND b.id = b_a.book_id AND b_a.author_id = {0} " \
              "UNION " \
              "SELECT 0, '', b.id, b.title, b.year, b.rating, concat(g.id,':',g.slug,':', g.name) " \
              "FROM books_book AS b,books_book_author AS b_a, books_book_genre_new bg,genres_genrenew g " \
              "WHERE bg.book_id = b.id AND bg.genrenew_id = g.id AND b.series_id is null AND b.id = b_a.book_id AND b_a.author_id = {0}) AS t " \
              "GROUP BY series_id,series_title,book_id,title,year,rating ORDER BY 6;".format(self.kwargs['pk'])

        cursor.execute(sql)

        series = {}
        genresIds = []
        books_ids = []

        for row in cursor.fetchall():
            books_ids.append(row[2])

            if not series.get(row[0]):
                series[row[0]] = {'id': row[0], 'title': row[1], 'books': []}

            genres = []
            genres_tmp = row[6].split(';')
            for g in genres_tmp:
                gg = g.split(':')
                genres.append({'id': gg[0], 'slug': gg[1], 'name': gg[2]})

                if gg[0] not in genresIds:
                    genresIds.append(gg[0])

            series[row[0]]['books'].append({
                'id': row[2],
                'title': row[3],
                'year': row[4],
                'index': len(series[row[0]]['books']) + 1,
                'rating': row[5],
                'genres': genres
            })
        context['series'] = series
        context['genres'] = genresIds

        try:
            # SEO description
            context['seo_description'] = TAG_RE.sub('', author.description).replace("\n","").replace("  "," ")
        except Exception as e:
            context['seo_description'] = 'Полный перечень книг автора с сортировкой по рейтингу, годам, можно скачать.'
            print('Exception: {}'.format(e), context)

        # посты об авторе
        context['posts'] = Publication.objects.filter(author=self.kwargs['pk'])

        # посты о книгах автора
        context['posts_books'] = Publication.objects.filter(book__in=books_ids)

        context['count_posts'] = len(context['posts']) + len(context['posts_books'])

        return context


@csrf_exempt
def get_author_book_genres(request):
    genre_list = []

    try:
        data = json.loads(request.body.decode('utf-8'))
        genres = GenreNew.objects.filter(pk__in=data.get('genres_ids'))
        for genre in genres:
            genre_list.append({
                'id': genre.id,
                'url': genre.get_absolute_url(),
                'name': genre.name
            })
    except ValueError:
        print ('ValueError may be Expecting value: line 1 column 1 (char 0) author id {}'.format())

    return JsonResponse({'genres': genre_list})


@csrf_exempt
def get_author_books(request):
    data = json.loads(request.body.decode('utf-8'))

    author_id = data.get('author_id')

    if data.get('is_group'):
        # Книги автора сгруппированые по сериям
        sort = data.get('sort')
        genre = int(data.get('genre'))
        order = 'DESC'

        if sort == '-rating':
            sort = 6

        if sort == '-show_counter':
            sort = 8

        if sort == 'title':
            sort = 4
            order= 'ASC'

        cursor = connection.cursor()

        if not genre:
            sql = "SELECT series_id,series_title,book_id,title,year,rating, string_agg(genre, ';'),show_counter  " \
                  "FROM  (SELECT s.id AS series_id, s.title AS series_title, b.id AS book_id, b.title, b.year, b.rating, concat(g.id,':',g.slug,':', g.name) AS genre, b.show_counter " \
                  "FROM books_book AS b,books_book_author AS b_a, series_series s, books_book_genre_new bg,genres_genrenew g " \
                  "WHERE bg.book_id = b.id AND bg.genrenew_id = g.id AND s.id = b.series_id AND b.id = b_a.book_id AND b_a.author_id = {0} " \
                  "UNION " \
                  "SELECT 0, '', b.id, b.title, b.year, b.rating, concat(g.id,':',g.slug,':', g.name),b.show_counter " \
                  "FROM books_book AS b,books_book_author AS b_a, books_book_genre_new bg,genres_genrenew g " \
                  "WHERE bg.book_id = b.id AND bg.genrenew_id = g.id AND b.series_id is null AND b.id = b_a.book_id AND b_a.author_id = {0}) AS t " \
                  "GROUP BY series_id,series_title,book_id,title,year,rating,show_counter ORDER BY {1} {2};".format(author_id, sort, order)
        else:
            sql = "SELECT series_id,series_title,book_id,title,year,rating, string_agg(genre, ';'),show_counter  " \
                  "FROM  (SELECT s.id AS series_id, s.title AS series_title, b.id AS book_id, b.title, b.year, b.rating, concat(g.id,':',g.slug,':', g.name) AS genre, b.show_counter " \
                  "FROM books_book AS b,books_book_author AS b_a, series_series s, books_book_genre_new bg,genres_genrenew g " \
                  "WHERE bg.book_id = b.id AND bg.genrenew_id = g.id AND s.id = b.series_id AND b.id = b_a.book_id AND b_a.author_id = {0} AND g.id={3} " \
                  "UNION " \
                  "SELECT 0, '', b.id, b.title, b.year, b.rating, concat(g.id,':',g.slug,':', g.name),b.show_counter " \
                  "FROM books_book AS b,books_book_author AS b_a, books_book_genre_new bg,genres_genrenew g " \
                  "WHERE bg.book_id = b.id AND bg.genrenew_id = g.id AND b.series_id is null AND b.id = b_a.book_id AND b_a.author_id = {0} AND g.id={3}) AS t " \
                  "GROUP BY series_id,series_title,book_id,title,year,rating,show_counter ORDER BY {1} {2};".format(author_id, sort, order, genre)

        cursor.execute(sql)

        books = []
        series = {}

        for row in cursor.fetchall():
            genres = []
            genres_tmp = row[6].split(';')
            for g in genres_tmp:
                gg = g.split(':')
                genres.append({'id': gg[0], 'slug': gg[1], 'name': gg[2]})

            if row[0] not in series:
                series[row[0]] = {'id': row[0], 'title': row[1]}

            books.append({
                'series_id': row[0],
                'book_id': row[2],
                'book_title': row[3],
                'book_year': row[4],
                'book_rating': row[5],
                'book_genres': genres
            })
    else:
        sort = data.get('sort')
        genre_id = data.get('genre')
        bookss = Book.objects.prefetch_related('author', 'genre_new').filter(author=author_id).order_by(sort)

        if genre_id:
            bookss = bookss.filter(genre_new=genre_id)

        books = []
        series = {}

        for book in bookss:
            item = {
                'id': book.id,
                'url': book.get_absolute_url(),
                'title': book.title,
                'rating': book.rating,
                'genres': book.get_link_genres(),
                'year': book.year
            }

            books.append(item)

    return JsonResponse({'books': books, 'series': series})


@csrf_exempt
def vue_get_authors(request):
    data = json.loads(request.body.decode('utf-8'))

    sort = data.get('sort', '-rating')
    page = data.get('page', 1)

    if sort == '-rating':
        authors = Author.objects.all()
    else:
        authors = Author.objects.all().order_by(sort)

    paginator = Paginator(authors, settings.PAGE_SIZE)
    count = paginator.count

    try:
        authors = paginator.page(page)
    except PageNotAnInteger:
        authors = paginator.page(1)
    except EmptyPage:
        authors = paginator.page(paginator.num_pages)

    authors_list = []
    for author in authors:
        item = {
            'id': author.id,
            'url': author.get_absolute_url(),
            'name': author.name,
            'description': author.description,
            'rating': author.rating,
            'birthday': author.birthday,
            'show_counter': author.show_counter,
            'book_count': author.book_count,
            'photo': author.get_photo()
        }

        authors_list.append(item)

    return JsonResponse({'authors': authors_list, 'count': count})
