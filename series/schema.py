import graphene
import datetime
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Sum
from series.models import Series
from views.models import View


class SeriesNode(DjangoObjectType):
    class Meta:
        model = Series
        interfaces = (relay.Node,)
        filter_fields = {
            'title': ['exact', 'contains'],
        }


class AddSeries(relay.ClientIDMutation):
    class Input:
        token = graphene.String(required=True)
        pk = graphene.Int()
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        image = graphene.String(required=True)
        rating = graphene.Float()
        show_counter = graphene.Int()
        date_create = graphene.String()

    series = graphene.Field(SeriesNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # проверяет токен
        token = input.get('token', None)
        if token != '******************':
            return "Invalid token"

        series = Series(
            title = input.get('title'),
            description=input.get('description'),
            image=input.get('image'),
            rating=input.get('rating', 0),
            show_counter=input.get('show_counter', 0),
            date_create=input.get('date_create', 0),
            date_update=datetime.datetime.utcnow()
        )
        if input.get('pk'):
            series.pk=input.get('pk')
        series.save()

        return AddSeries(series=series)


class SeriesMutation(graphene.ObjectType):
    add_series = AddSeries.Field()