import graphene
import datetime
from django.conf import settings
from graphene import relay
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from views.models import View


class ViewNode(DjangoObjectType):
    class Meta:
        model = View
        interfaces = (relay.Node,)
        filter_fields = {"book_id", "author_id", "date"}


class AddView(graphene.ClientIDMutation):
    view = graphene.Field(ViewNode)

    class Input:
        token = graphene.String(required=True)
        book_id = graphene.Int()
        author_id = graphene.Int()

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # проверяет токен
        token = input.get('token', None)

        if token != settings.GRAPHENE_API_TOKEN:
            return "Invalid token"

        books_id = input.get('book_id')
        author_id = input.get('author_id')

        if books_id is not None:
            try:
                view = View.objects.get(book_id=books_id, date=datetime.date.today())
                view.views += 1
                view.save(update_fields=['views'])
            except View.DoesNotExist:
                view = View(book_id=books_id)
                view.save()
            return AddView(view=view)

        if author_id is not None:
            try:
                view = View.objects.get(author_id=author_id, date=datetime.date.today())
                view.views += 1
                view.save(update_fields=['views'])
            except View.DoesNotExist:
                view = View(author_id=author_id)
                view.save()
            return AddView(view=view)


class ViewQuery(graphene.ObjectType):
    view_book = relay.Node.Field(ViewNode)


class ViewMutation(graphene.ObjectType):
    add_view = AddView.Field()
