from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView
from genres.models import GenreNew, ParentGenre
from books.models import Book


def genres_list(request):
    parent_genres = ParentGenre.objects.all()
    genres = GenreNew.objects.all()
    return render(request, 'genres/genre_list.html', {'parent_genres': parent_genres, 'genres': genres})


class GenreDetail(ListView):
    """
    Список книг
    """
    model = Book
    context_object_name = 'books'
    template_name = 'genres/genre_detail.html'
    paginate_by = settings.PAGE_SIZE
    queryset = Book.objects.prefetch_related('author', 'genre_new')

    def get_context_data(self, *args, **kwargs):
        context = super(GenreDetail, self).get_context_data(**kwargs)

        try:
            genre = GenreNew.objects.get(slug=self.kwargs['slug'])
        except GenreNew.MultipleObjectsReturned:
            genre = GenreNew.objects.filter(slug=self.kwargs['slug'])[0]
        except GenreNew.DoesNotExist:
            raise Http404()

        books = self.queryset.filter(genre_new__in=[genre.id])

        paginator = Paginator(books, settings.PAGE_SIZE)
        page = self.request.GET.get('page')

        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        # получает похожие жанры
        genres_id = []
        image = None
        for book in books:
            genres = book.genre_new.all()
            for g in genres:
                if g not in genres_id:
                    genres_id.append(g.id)
            if image is None and book.image:
                image = book.get_image()

        context['genres'] = GenreNew.objects.filter(id__in=genres_id)
        context['genre'] = genre
        context['year'] = self.kwargs.get('year')
        context['books'] = books
        context['image'] = image

        return context


@csrf_exempt
def vue_genres_get(request):
    genres = list(GenreNew.objects.all().values('id', 'name'))
    return JsonResponse({'genres': genres})
