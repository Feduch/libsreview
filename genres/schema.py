import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from genres.models import GenreNew


# class GenreNode(DjangoObjectType):
#     class Meta:
#         model = Genre
#         interfaces = (relay.Node,)
#         filter_fields = {
#             'title': ['exact', 'contains'],
#         }
#
#
# class GenreQuery(graphene.ObjectType):
#     genre = relay.Node.Field(GenreNode)
#     genres = DjangoFilterConnectionField(GenreNode)

class GenrePlain(DjangoObjectType):
    class Meta:
        model = GenreNew


class GenreQuery(graphene.ObjectType):
    genres = graphene.List(GenrePlain)

    def resolve_genres(self, info):
        return GenreNew.objects.all()