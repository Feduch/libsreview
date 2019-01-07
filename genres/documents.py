from django_elasticsearch_dsl import DocType, Index, fields
from elasticsearch_dsl import analyzer, tokenizer
from genres.models import GenreNew

# Name of the Elasticsearch index
genre = Index('genres')
# See Elasticsearch Indices API reference for available settings
genre.settings(
    number_of_shards=1,
    number_of_replicas=0
)

html_strip = analyzer(
    'genre',
    tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
    filter=["lowercase"]
)

@genre.doc_type
class GenreDocument(DocType):
    name = fields.TextField(
        analyzer=html_strip,
        fields={'raw': fields.KeywordField()}
    )

    class Meta:
        model = GenreNew # The model associated with this DocType
        # queryset_pagination = 50000
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id'
        ]
