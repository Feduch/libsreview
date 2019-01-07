import json
import datetime
from django.db.models import Count
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from books.models import Book
from genres.models import GenreNew


@csrf_exempt
def vue_navigator(request):
    data = request.POST

    genre = data.get('genre', 0)
    years = data.get('year', '-')
    years = years.split('-')

    start_year = ''
    end_year = ''
    year = ''

    if len(years) > 1:
        start_year = years[0]
        end_year = years[1]
    else:
        year = years[0]

    genre_list = []
    if genre:
        try:
            genre = GenreNew.objects.get(pk=genre)
            genre_list.append({'id': genre.id, 'name': genre.name})
        except GenreNew.DoesNotExist:
            pass

    to_template = {
        'genre': genre_list,
        'start_year': start_year,
        'end_year': end_year,
        'year': year
    }

    return render(request, 'navigator.html', to_template)


@csrf_exempt
def vue_get_years(request):
    data = json.loads(request.body.decode('utf-8'))
    genre_id = data.get('genre_id')

    d = datetime.date.today()
    years = list(Book.objects.filter(year__lte=d.year + 1).values_list('year', flat=True).annotate(count=Count('year')).order_by('-year'))

    if genre_id:
        years = list(Book.objects.filter(genre_new__in=genre_id).values_list('year', flat=True).annotate(count=Count('year')).order_by('-year'))

    return JsonResponse({'years': years})


@csrf_exempt
def vue_get_books(request):
    data = json.loads(request.body.decode('utf-8'))
    sort = data.get('sort', '-rating')
    page = data.get('page', 1)
    page_size = 10
    first = page * page_size - page_size
    last = page * page_size
    genre_id = data.get('genre_id')
    start_year = data.get('start_year')
    end_year = data.get('end_year')
    year = data.get('year')

    if sort == '-rating':
        books = Book.objects.prefetch_related('author', 'genre_new').filter()
    else:
        books = Book.objects.prefetch_related('author', 'genre_new').filter().order_by(sort)

    if start_year:
        books = books.filter(year__gte=start_year)

    if end_year:
        books = books.filter(year__lte=end_year)

    if year:
        books = books.filter(year=year)

    if genre_id:
        books = books.filter(genre_new__in=genre_id)

    books = books.filter()[first:last]

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
            'image': book.get_image()
        }

        books_list.append(item)

    return JsonResponse({'books': books_list})
