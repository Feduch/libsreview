from django_elasticsearch_dsl import DocType, Index, fields
from authors.models import Author


# Name of the Elasticsearch index
author = Index('authors')
# See Elasticsearch Indices API reference for available settings
author.settings(
    number_of_shards=1,
    number_of_replicas=0
)


@author.doc_type
class AuthorDocument(DocType):
    class Meta:
        model = Author # The model associated with this DocType
        # queryset_pagination = 50000
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'id',
            'name'
        ]
