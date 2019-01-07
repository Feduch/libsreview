import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
from django.contrib.auth.models import User
from publications.models import Publication


class PublicationNode(DjangoObjectType):
    class Meta:
        model = Publication
        interfaces = (relay.Node,)
        filter_fields = {
            'title': ['exact', 'contains'],
        }


class AddPublication(relay.ClientIDMutation):
    class Input:
        token = graphene.String(required=True)
        pk = graphene.Int()
        title = graphene.String(required=True)
        preview_text = graphene.String()
        detail_text = graphene.String()
        image = graphene.String()
        rating = graphene.Float()
        age = graphene.Int()
        author = graphene.List(graphene.Int)
        book = graphene.List(graphene.Int)
        user_id = graphene.Int()
        date_create = graphene.String()
        show_counter = graphene.String()

    publication = graphene.Field(PublicationNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # проверяет токен
        token = input.get('token', None)
        if token != '******************':
            return "Invalid token"

        publication = Publication(
            title = input.get('title'),
            preview_text=input.get('preview_text', ''),
            detail_text=input.get('detail_text', ''),
            image=input.get('image', ''),
            rating=input.get('rating', 0),
            user_id=input.get('user_id', 5227),
            date_create=input.get('date_create'),
            show_counter=input.get('show_counter'),
        )
        if input.get('pk'):
            publication.pk=input.get('pk')
        if input.get('age'):
            publication.age = input.get('age', 0)
        publication.save()

        if input.get('author'):
            publication.author.set(input.get('author'))
            publication.save()
        if input.get('book'):
            try:
                publication.book.set(input.get('book'))
                publication.save()
            except Exception as e:
                pass

        return AddPublication(publication=publication)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        interfaces = (relay.Node,)
        filter_fields = {
            'username': ['exact', 'contains'],
            'id': ['exact'],
            'first_name': ['exact', 'contains'],
            'last_name': ['exact', 'contains'],
            'email': ['exact'],
        }


class AddUser(relay.ClientIDMutation):
    """Добавляет пользователя"""
    class Input:
        token = graphene.String(required=True)
        pk = graphene.Int()
        username = graphene.String()
        first_name = graphene.String()
        last_name = graphene.String()
        email = graphene.String()
        password = graphene.String()

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # проверяет токен
        token = input.get('token', None)
        if token != '******************':
            return "Invalid token"

        user = User(
            pk=input.get('pk'),
            username=input.get('username', 'guest'),
            first_name=input.get('first_name'),
            last_name=input.get('last_name'),
            email=input.get('email', 'noreply@libs.ru'),
            password=input.get('password', '***************'),
        )

        user.save()

        return AddUser(user=user)


class PublicationQuery(graphene.ObjectType):
    publication = relay.Node.Field(PublicationNode)
    all_publications = DjangoFilterConnectionField(PublicationNode)


class PublicationMutation(graphene.ObjectType):
    add_publication = AddPublication.Field()


class UserMutation(graphene.ObjectType):
    add_user = AddUser.Field()
