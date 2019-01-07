from collection.models import Collection
from genres.models import GenreNew


def last_collections(request):
    return {'last_collections': Collection.objects.all().order_by('?')[:6]}


def all_genres(request):
    return {'all_genres': GenreNew.objects.all()}
