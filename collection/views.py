import json
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from collection.models import Collection


class CollectionsList(ListView):
    """
    Список коллекций
    """
    model = Collection
    context_object_name = 'collections'
    paginate_by = 50


class CollectionDetail(ListView):
    """
    Список книг
    """
    model = Collection
    context_object_name = 'collection'
    template_name = 'collection/collection_detail.html'
    paginate_by = 100

    def get_context_data(self, *args, **kwargs):
        context = super(CollectionDetail, self).get_context_data(**kwargs)

        collection = Collection.objects.get(pk=self.kwargs['pk'])

        print(collection.image)

        try:
            collection.show_counter += 1
            collection.save(update_fields=['show_counter'])
        except collection.DoesNotExist:
            pass

        books = collection.book.all()
        paginator = Paginator(books, self.paginate_by)
        page = self.request.GET.get('page')

        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)

        context['books'] = books
        context['collection'] = collection

        return context


def collection_editor(request, pk=None):
    if not request.user.is_authenticated:
        return redirect('/')
    return render(request, 'collection/collection_editor.html', {'id': pk})


@csrf_exempt
def vue_get_collection_books(request):
    data = json.loads(request.body.decode('utf-8'))

    sort = data.get('sort', '-rating')
    page = data.get('page', 1)
    collection_id = data.get('collection_id')

    collection = Collection.objects.get(pk=collection_id)
    books = collection.book.all().order_by(sort)

    paginator = Paginator(books, 100)

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
            'show_counter': book.show_counter
        }
        if book.image:
            item['image'] = book.image.url.replace('/media/', '').replace('%3A', ':')

        books_list.append(item)

    return JsonResponse({'books': books_list})


@csrf_exempt
def vue_collection_save(request):
    if request.user.is_authenticated:
        image = request.FILES.get('image')

        data = request.POST.get('data')
        data = json.loads(data)

        id = data.get('id', None)
        title = data.get('title')
        text = data.get('text')
        books = data.get('books', None)

        key = make_template_fragment_key('libs__collection')
        cache.delete(key)

        if id:
            # Сохраняет изменения
            collection = Collection.objects.get(pk=id, user=request.user)
            collection.title = title
            collection.text = text
            collection.user = request.user
            collection.book.set(books)
            collection.save()
        else:
            # Создает новую коллекцию
            collection = Collection(
                title=title,
                text=text,
                user=request.user
            )
            collection.save()

            if books:
                collection.book.set(books)

        if image:
            collection.image.save(image.name, image)

    return JsonResponse({'id': collection.id})


@csrf_exempt
def vue_collection_editor_get(request):
    collection_dict = {}
    error = ''
    if request.user.is_authenticated:

        data = json.loads(request.body.decode('utf-8'))
        id = data.get('id', None)

        if id:
            try:
                collection = Collection.objects.get(pk=id, user=request.user)
                books = collection.book.all()

                collection_dict = {
                    'title': collection.title,
                    'text': collection.text,
                    'books': []
                }

                if collection.image:
                    collection_dict['image'] = collection.image.url

                books_list = []
                for book in books:
                    item = {
                        'id': book.id,
                        'title': "{}, {}".format(book.title, book.get_text_authors())
                    }

                    books_list.append(item)

                collection_dict['books'] = books_list
            except Collection.DoesNotExist:
                error = 'Коллекция не найдена'

    return JsonResponse({'collection': collection_dict, 'error': error})
