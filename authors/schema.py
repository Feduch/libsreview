import graphene
import datetime
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django.db.models import Sum
from authors.models import Author
from views.models import View


class AuthorNode(DjangoObjectType):
    class Meta:
        model = Author
        interfaces = (relay.Node,)
        filter_fields = {
            'name': ['exact', 'contains'],
        }
        
        
class AuthorFilter(DjangoObjectType):
    class Meta:
        model = Author


class AuthorRating(DjangoObjectType):
    class Meta:
        model = Author


class AuthorQuery(graphene.ObjectType):
    author = relay.Node.Field(AuthorNode)
    all_author = DjangoFilterConnectionField(AuthorNode)


class AuthorRatingQuery(graphene.ObjectType):
    author_rating = graphene.List(AuthorRating)

    def resolve_author_rating(self, info):
        # Получает всех авторов
        return Author.objects.all()
    

class AuthorFilterQuery(graphene.ObjectType):
    author_filter = graphene.List(
        AuthorFilter,
        permian=graphene.Int(),
        sort=graphene.String(),
        genre=graphene.Int(),
        page=graphene.Int()
    )

    def resolve_author_filter(self, info, **kwargs):
        permian = kwargs.get('permian')
        sort = kwargs.get('sort', 'rating')
        genre = kwargs.get('genre')
        page = kwargs.get('page', 1)

        if sort == 'views':
            authors = View.objects.filter(
                author__isnull=False,
            ).values("author_id").annotate(
                views=Sum('views'))[:30]
            authors_id = []
            for author in authors:
                authors_id.append(author['author_id'])
            return Author.objects.filter(id__in=authors_id)

        if sort == 'name':
            return Author.objects.all().order_by('name')[:30]

        if sort == 'rating':
            return Author.objects.all()[:30]


class AddAuthor(relay.ClientIDMutation):
    class Input:
        token = graphene.String(required=True)
        pk = graphene.Int()
        name = graphene.String(required=True)
        description = graphene.String(required=True)
        photo = graphene.String(required=True)
        birthday = graphene.String()
        death = graphene.String()
        name_original = graphene.String()
        rating = graphene.Float()
        show_counter = graphene.Int()
        date_create = graphene.String()
        book_count = graphene.Int()
        nationality = graphene.Int()

    author = graphene.Field(AuthorNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # проверяет токен
        token = input.get('token', None)
        if token != '******************':
            return "Invalid token"

        author = Author(
            name = input.get('name'),
            description=input.get('description'),
            photo=input.get('photo'),
            rating=input.get('rating', 0),
            show_counter=input.get('show_counter', 0),
            date_create=input.get('date_create', 0),
            book_count=input.get('book_count', 0),
            nationality_id=input.get('nationality', 0),
        )
        if input.get('pk'):
            author.pk=input.get('pk')
        if input.get('birthday'):
            author.birthday = input.get('birthday')
        if input.get('death'):
            author.death = input.get('death')
        if input.get('name_original'):
            author.name_original = input.get('name_original')

        author.save()

        return AddAuthor(author=author)


class AuthorMutation(graphene.ObjectType):
    add_author = AddAuthor.Field()