import json
from django.shortcuts import render, redirect
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from publications.models import Publication


class PublicationList(ListView):
    """
    Список постов
    """
    model = Publication
    context_object_name = 'publications'
    paginate_by = 30


class PublicationDetail(DetailView):
    """
    Пост
    """
    model = Publication
    context_object_name = 'publication'

    def get_context_data(self, **kwargs):
        context = super(PublicationDetail, self).get_context_data(**kwargs)
        publication = Publication.objects.get(pk=self.kwargs['pk'])

        # увеличивает количество просмотров
        try:
            publication.show_counter += 1
            publication.save(update_fields=['show_counter'])
        except PublicationDetail.DoesNotExist:
            pass

        return context


def publication_editor(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'publications/publication_editor.html', {'id': pk})


@csrf_exempt
def vue_publication_editor_get(request):
    publication_dict = {}
    error = ''
    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)

        if id:
            try:
                publication = Publication.objects.get(pk=id, user=request.user)

                books = publication.book.all()
                authors = publication.author.all()
                series = publication.series.all()

                publication_dict = {
                    'title': publication.title,
                    'text': publication.detail_text,
                    'books': [],
                    'authors': [],
                    'series': []
                }

                if publication.image:
                    publication_dict['image'] = publication.image.url

                books_list = []
                for book in books:
                    item = {
                        'id': book.id,
                        'title': "{}, {}".format(book.title, book.get_text_authors())
                    }
                    books_list.append(item)

                publication_dict['books'] = books_list

                authors_list = []
                for author in authors:
                    item = {
                        'id': author.id,
                        'name': author.name
                    }

                    authors_list.append(item)

                publication_dict['authors'] = authors_list

                series_list = []
                for s in series:
                    item = {
                        'id': s.id,
                        'title': s.title
                    }
                    series_list.append(item)

                publication_dict['series'] = series_list
            except Publication.DoesNotExist:
                error = 'Публикация не найдена'

    return JsonResponse({'publication': publication_dict, 'error': error})


@csrf_exempt
def vue_publication_save(request):
    to_template = {}
    if request.user.is_authenticated:
        image = request.FILES.get('image')

        data = request.POST.get('data')
        data = json.loads(data)

        id = data.get('id', None)
        title = data.get('title')
        text = data.get('text')
        books = data.get('books', None)
        authors = data.get('authors', None)
        series = data.get('series', None)

        if id:
            # Сохраняет изменения
            publication = Publication.objects.get(pk=id, user=request.user)
            publication.title = title
            publication.preview_text = Truncator(strip_tags(text)).words(33)
            publication.detail_text = text
            publication.user = request.user
            publication.series_id = series
            publication.save()

            publication.book.set(books)
            publication.author.set(authors)
            publication.series.set(series)

        else:
            # Создает новую коллекцию
            publication = Publication(
                title=title,
                user=request.user,
                preview_text = Truncator(strip_tags(text)).words(33),
                detail_text = text
            )
            publication.save()

            if books:
                publication.book.set(books)
            if authors:
                publication.author.set(authors)
            if series:
                publication.series.set(series)

        if image:
            publication.image.save(image.name, image)
            to_template['image'] = publication.image.url

        to_template['id'] = publication.id

    return JsonResponse(to_template)
