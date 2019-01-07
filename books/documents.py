from django_elasticsearch_dsl import DocType, Index, fields
from books.models import Book
from authors.models import Author
from genres.models import GenreNew

# Name of the Elasticsearch index
book = Index('books')
# See Elasticsearch Indices API reference for available settings
book.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@book.doc_type
class BookDocument(DocType):
    isbn = fields.TextField(attr="get_isbn")
    author_text = fields.TextField(attr="get_authors")
    author = fields.NestedField(properties={
        'id': fields.IntegerField(),
        'name': fields.StringField()
    })

    class Meta:
        model = Book  # The model associated with this DocType
        # queryset_pagination = 50000
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'title'
        ]

    #    related_models = [Author]

    # def get_instances_from_related(self, related_instance):
    #     if isinstance(related_instance, Author):
    #         return related_instance.author_set.all()


