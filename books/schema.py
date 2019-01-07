import graphene
import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id
from books.models import Book
from views.models import View


class BookNode(DjangoObjectType):
    class Meta:
        model = Book
        interfaces = (relay.Node,)
        filter_fields = {
            'title': ['exact', 'contains'],
            'year': ['gte', 'lte'],
            'genre':['exact']
        }


class BookRating(DjangoObjectType):
    class Meta:
        model = Book


class BookFilter(DjangoObjectType):
    class Meta:
        model = Book


class AddBook(relay.ClientIDMutation):
    class Input:
        token = graphene.String(required=True)
        pk = graphene.Int()
        title = graphene.String(required=True)
        description = graphene.String(required=True)
        image = graphene.String(required=True)
        age = graphene.Int()
        year = graphene.String()
        original_title = graphene.String()
        author = graphene.List(graphene.Int)
        genre = graphene.List(graphene.Int)
        genres = graphene.List(graphene.Int)
        series_id = graphene.Int()
        nr_series = graphene.Int()
        rating = graphene.Float()
        date_create = graphene.String()
        show_counter = graphene.Int()

    book = graphene.Field(BookNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # проверяет токен
        token = input.get('token', None)
        if token != '******************':
            return "Invalid token"

        book = Book(
            title = input.get('title'),
            description=input.get('description'),
            image=input.get('image'),
            rating=input.get('rating', 0),
            show_counter=input.get('show_counter', 0),
            date_create=input.get('date_create', 0)
        )
        if input.get('pk'):
            book.pk=input.get('pk')
        if input.get('age'):
            book.age = input.get('age')
        if input.get('year'):
            book.year = input.get('year')
        if input.get('original_title'):
            book.original_title = input.get('original_title')
        if input.get('series_id'):
            book.series_id = input.get('series_id')
        if input.get('nr_series'):
            book.nr_series = input.get('nr_series')
        book.save()

        if input.get('author'):
            book.author.set(input.get('author'))
            book.save()
        if input.get('genre'):
            book.genre.set(input.get('genre'))
            book.save()
        if input.get('genres'):
            book.genres = input.get('genres')
            book.save(update_fields=['genres'])

        return AddBook(book=book)


class UpdateBook(relay.ClientIDMutation):
    class Input:
        token = graphene.String(required=True)
        id = graphene.String(required=True)
        title = graphene.String()
        description = graphene.String()
        image = graphene.String()
        age = graphene.Int()
        year = graphene.String()
        original_title = graphene.String()
        author = graphene.List(graphene.Int)
        genre = graphene.List(graphene.Int)
        series_id = graphene.Int()
        nr_series = graphene.Float()
        rating = graphene.Int()

    book = graphene.Field(BookNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        # проверяет токен
        token = input.get('token', None)

        if token != '******************':
            return "Invalid token"

        try:
            book = Book.objects.get(id=from_global_id(input.get('id'))[1])
            if input.get('title'):
                book.title=input.get('title')
            if input.get('description'):
                book.description=input.get('description')
            if input.get('image'):
                book.image=input.get('image')
            if input.get('age'):
                book.age=input.get('age')
            if input.get('year'):
                book.year=input.get('year')
            if input.get('original_title'):
                book.original_title=input.get('original_title')
            if input.get('author'):
                book.author=input.get('author')
            if input.get('genre'):
                book.genre=input.get('genre')
            if input.get('series_id'):
                book.series_id=input.get('series_id')
            if input.get('nr_series'):
                book.nr_series=input.get('nr_series')
            book.save()
            return UpdateBook(book=book)
        except Book.DoesNotExist:
            return "Not found this is book"


class MostViewsBooks(relay.ClientIDMutation):
    class Input:
        token = graphene.String()
        libs_book_id = graphene.Int(required=True)

    book = graphene.Field(BookNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        book = Book.objects.get(id=input.get('libs_book_id'))
        return MostViewsBooks(book=book)


class BookQuery(graphene.ObjectType):
    book = relay.Node.Field(BookNode)
    all_books = DjangoFilterConnectionField(BookNode)


class BookRatingQuery(graphene.ObjectType):
    book_rating = graphene.List(BookRating, days=graphene.Int(), month=graphene.Int())

    def resolve_book_rating(self, info, **kwargs):
        # Получает 8 популярных книг
        if kwargs.get('days'):
            datetime_utc = datetime.datetime.utcnow() - datetime.timedelta(days=kwargs.get('days'))
            books = View.objects.filter(
                date__gte=datetime_utc,
                book__isnull=False
            ).values("book_id").annotate(views=Sum('views'))[:8]
        books_id = []
        for book in books:
            books_id.append(book['book_id'])
        return Book.objects.filter(id__in=books_id)


class BookFilterQuery(graphene.ObjectType):
    # получает все книги автора
    books_author = graphene.List(BookFilter, author_id=graphene.Int(required=True))

    books_filter = graphene.List(
        BookFilter,
        start_year=graphene.Int(),
        end_year=graphene.Int(),
        sort=graphene.String(),
        genre=graphene.Int(),
        page=graphene.Int()
    )

    def resolve_books_author(self, info, **kwargs):
        author_id = kwargs.get('author_id')
        return Book.objects.filter(author=author_id)

    def resolve_books_filter(self, info, **kwargs):
        start_year = kwargs.get('start_year', 1)
        end_year = kwargs.get('end_year', 3000)
        sort = kwargs.get('sort', 'rating')
        genre = kwargs.get('genre')
        page = kwargs.get('page', 1)

        if sort == 'views':
            if genre is not None:
                books = View.objects.filter(
                    book__isnull=False,
                    book__year__gte=start_year,
                    book__year__lte=end_year,
                    book__genre=genre
                ).values("book_id").annotate(
                views=Sum('views'))[:30]
            else:
                books = View.objects.filter(
                    book__isnull=False,
                    book__year__gte=start_year,
                    book__year__lte=end_year
                ).values("book_id").annotate(
                    views=Sum('views'))[:30]

            books_id = []
            for book in books:
                books_id.append(book['book_id'])
            return Book.objects.filter(id__in=books_id)

        if sort == 'title':
            if genre is not None:
                books = Book.objects.filter(
                    year__gte=start_year,
                    year__lte=end_year,
                    genre=genre
                ).order_by('title')[:30]
            else:
                books = Book.objects.filter(
                    year__gte=start_year,
                    year__lte=end_year
                ).order_by('title')[:30]

            return books

        if sort == 'rating':
            if genre is not None:
                books = Book.objects.filter(
                    year__gte=start_year,
                    year__lte=end_year,
                    genre=genre
                )[:30]
            else:
                books = Book.objects.filter(
                    year__gte=start_year,
                    year__lte=end_year
                )[:30]

            return books


class BookMutation(graphene.ObjectType):
    add_book = AddBook.Field()
    update_book = UpdateBook.Field()
    most_views_books = MostViewsBooks.Field()
