import decimal
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from sorl.thumbnail import get_thumbnail
from authors.models import Author
from genres.models import Genre, GenreNew
from series.models import Series
from awards.models import Award
from ratings.models import StarRatings
from django.db.models import Avg
from libs.graphqlclient import execude_libsagregator, execude_libspartners


def book_image_path(instance, filename):
    return 'books/{0}/{1}'.format(instance.id, filename)


class Book(models.Model):
    """Модель книги"""
    title = models.CharField(verbose_name='Название книги', max_length=400)
    description = models.TextField(verbose_name='Описание книги', blank=True, null=True, default='')
    image = models.ImageField(verbose_name='Обложка', upload_to=book_image_path, blank=True, null=True)
    age = models.PositiveIntegerField(verbose_name='Возрасное ограничение', default=0, null=True)
    year = models.PositiveIntegerField(verbose_name='Год издания', default=0, null=True, db_index=True)
    original_title = models.CharField('Оригинальное название', max_length=255, blank=True, null=True)
    author = models.ManyToManyField(Author, related_name="book_author", blank=True)
    genre = models.ManyToManyField(Genre, related_name="book_genre", blank=True)
    genre_new = models.ManyToManyField(GenreNew, related_name="book_genre_new", blank=True)
    genres = ArrayField(models.IntegerField(), verbose_name='Жанры', blank=True, null=True)
    series = models.ForeignKey(Series, related_name="book_series", blank=True, null=True, on_delete=models.DO_NOTHING)
    nr_series = models.PositiveSmallIntegerField('Номер книги в серии', blank=True, null=True)
    rating = models.DecimalField('Рейтинг', default=0, max_digits=3, decimal_places=2)
    rating_partner_votes = models.PositiveIntegerField('Количество партнерских голосов', default=0)
    manual_rating = models.DecimalField('Ручной рейтинг', default=0, max_digits=2, decimal_places=1)
    date_create = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    date_update = models.DateTimeField(auto_now=True, blank=True, null=True, help_text="Дата обновления")
    show_counter = models.PositiveIntegerField('Количество просмотров', default=0)
    is_online = models.BooleanField('Лучшее оналайн', default=False)
    status = models.NullBooleanField('Да - проверена и опубликована, Нет - проверена и отключена, Неизвестно - на проверке')
    litres_id = models.PositiveIntegerField('ID у партнера', blank=True, null=True)
    isbn = models.CharField(verbose_name='ISBN', max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Активна', default=True)
    award = models.ManyToManyField(Award, related_name="book_award", blank=True)
    created_by = models.ForeignKey(User, verbose_name="Кто создал", related_name="book_created_by", default=5227, on_delete=models.DO_NOTHING)
    modified_by = models.ForeignKey(User, verbose_name="Кто изменил", related_name="book_modified_by", default=5227, on_delete=models.DO_NOTHING)

    def __str__(self):
        return "{0}".format(self.title)

    def rating_to_float(self):
        return float(self.rating)

    def get_type(self):
        return 'book'

    def get_authors(self):
        return ", ".join([a.name for a in self.author.all()])

    def get_authors_id(self):
        ids = []
        for a in self.author.filter(is_active=True):
            ids.append(a.id)
        return ids

    def get_genres(self):
        return ", ".join([g.name for g in self.genre_new.all()])

    def get_genres_id(self):
        ids = []
        for g in self.genre_new.all():
            ids.append(g.id)
        return ids

    def get_author(self):
        author = ''
        try:
            author = self.author.filter(is_active=True)[0].name
        except Exception as e:
            pass
        return author

    def get_text_authors(self):
        authors = []
        for a in self.author.filter(is_active=True):
            authors.append(a.name)
        return ", ".join(authors)

    def get_link_authors(self):
        authors = []
        for a in self.author.filter(is_active=True):
            authors.append('<a itemprop="url" href="{0}"><span itemprop="name">{1}</span></a>'.format(a.get_absolute_url(), a.name))
        return ", ".join(authors)

    def get_link_genres(self):
        genres = []
        for g in self.genre_new.all():
            genres.append('<a itemprop="url" href="{0}"><span itemprop="genre">{1}</span></a>'.format(g.get_absolute_url(), g.name))
        return ", ".join(genres)

    def get_link_awards(self):
        awards = []
        for a in self.award.all():
            awards.append('<span itemprop="award">{}</span>'.format(a.name))
        return ", ".join(awards)

    def get_link_genres_collection(self):
        genres = []
        for g in self.genre_new.all():
            genres.append({'id': g.id, 'url': g.get_absolute_url(), 'name': g.name, 'url_year': "{}{}/".format(g.get_absolute_url(), self.year)})
        return genres

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'pk': self.pk})

    def get_read_url(self):
        return reverse('book-read', kwargs={'pk': self.pk})

    def get_image(self):
        image = None
        if self.image:
            try:
                if 'http' in self.image.url:
                    image = self.image.url.replace('/media/', '').replace('%3A', ':')
                    # Уменьшает картинки которые пришли от литреса
                    im = get_thumbnail(image, '570x850', crop='center', quality=80)
                    image = im.url
                else:
                    image = self.image.url
            except Exception as e:
                print(e)
        return image

    def get_image_vk_wall(self):
        image = None
        if self.image:
            if 'http' in self.image.url:
                image = self.image.url.replace('/media/', '').replace('%3A', ':')
                # Уменьшает картинки которые пришли от литреса
                im = get_thumbnail(image, '400x300', crop='80% top', quality=80)
                image = im.url
            else:
                image = self.image.url
        return image


    def get_image_preview(self):
        image = None
        if self.image:
            if 'http' in self.image.url:
                image = self.image.url.replace('/media/', '').replace('%3A', ':')
                # Уменьшает картинки которые пришли от литреса
                im = get_thumbnail(image, '150x224', crop='center', quality=80)
                image = im.url
            else:
                image = self.image.url
        return image

    def get_isbn(self):
        if self.isbn:
            return self.isbn.replace('-', '')
        else:
            return ''

    class Meta:
        ordering = ['-rating', '-show_counter']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


@receiver(pre_save, sender = Book)
def update_rating(instance, **kwargs):
    if instance.manual_rating > 0:
        query = '''
                query book_rating($libs_book_id: Int, $token: String) {
                      book_rating(libs_book_id: $libs_book_id, token: $token) {
                        rating
                      }
                    }
                '''
        params = {'libs_book_id': instance.pk}

        result = execude_libsagregator(query=query, params=params)

        manual_rating = decimal.Decimal(instance.manual_rating) * 1
        partners_rating = 0
        count = 1

        # Пользовательский рйтинг
        user_rating = StarRatings.objects.filter(book_id=instance.pk).aggregate(Avg('rating'))['rating__avg']
        if user_rating:
            user_rating = decimal.Decimal(user_rating)
            count += 1
        else:
            user_rating = 0

        if result.get('book_rating'):
            book_rating = result.get('book_rating')
            partners_rating = decimal.Decimal(book_rating.get('rating', 0))
            if partners_rating:
                count += 1

        instance.rating = round((manual_rating + partners_rating + user_rating) / count, 2)


def get_stat_partner_links():
    from views.models import View
    from manager.models import BookPartnerLink
    from django.db.models import Sum
    books = BookPartnerLink.objects.all()

    for book in books:
        query = '''
                query books_price($name: String!, $author: String, $libsid: Int, $litresid: Int) {
                      books_price(name:$name, author:$author, libsid: $libsid, litresid: $litresid) {
                        type
                        available
                        url
                        price
                        oldprice
                        currency
                        name
                        author
                        partner {
                          name,
                          logo
                        }
                      }
                    }
                '''
        params = {
            'name': book.book.title,
            'author': book.book.get_author(),
            'libsid': book.book.id,
            'litresid': book.book.litres_id
        }

        result = execude_libspartners(query=query, params=params)
        """
            Записывает книги укоторых < 3 партнерских ссылок.
            Удаляет если ссылок стало больше >= 3
            """
        book_id = book.book.id
        count_partner_link = len(result['books_price'])

        if count_partner_link == 0:
            views = View.objects.filter(book_id=book_id).values("book_id").annotate(
                views=Sum('views'))

            try:
                view = views[0].get('views', 0)
            except Exception as e:
                print(e)

            try:
                book_partner_link = BookPartnerLink.objects.get(book_id=book_id)
                book_partner_link.count_partner_link = count_partner_link
                book_partner_link.views = view
                book_partner_link.save()
                print('Книга обновлена в журнале')
            except BookPartnerLink.DoesNotExist:
                BookPartnerLink(
                    book_id=book_id,
                    count_partner_link=count_partner_link,
                    views=view
                ).save()
                print('Книга добавлена в журнале')
            except BookPartnerLink.MultipleObjectsReturned:
                BookPartnerLink.objects.filter(book_id=book_id)[0].delete()
                print('Удален дубликат книги из журнала')
        else:
            try:
                book_partner_link = BookPartnerLink.objects.filter(book_id=book_id)
                if len(book_partner_link):
                    book_partner_link.delete()
                    print('Книга удалена')
            except BookPartnerLink.DoesNotExist:
                pass


def get_stat_partner_links_elastic():
    from views.models import View
    from manager.models import BookPartnerLink
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import Search
    from elasticsearch_dsl import Q

    partner_books = BookPartnerLink.objects.all()

    for partner_book in partner_books:
        client = Elasticsearch(['85.10.246.202'])
        q = Q("match_phrase", name=partner_book.book.title) & Q("match_phrase", author=partner_book.book.get_author())
        s = Search().using(client).query(q)
        response = s.execute()

        for hit in s:
            if hit.available:
                print ("{}/{}/{} <=> {}/{}/{}/{}/{}".format(partner_book.book.id, partner_book.book.title, partner_book.book.get_author(), hit.id, hit.name, hit.author, hit.available, hit.libs_book_id))


def get_partners_book(page=1, page_size=100, partner_id=1):
    query = '''
        query partners_books($page: Int, $page_size: Int, $partner_id: Int) {
                  partners_books(page: $page, page_size: $page_size, partner_id: $partner_id) {
                    id
                    partner_book_id
                    name
                    author
                    libs_book_id
                    year
                    picture
                    age
                    rating
                    genres
                    isbn
                  }
                }
            '''
    params = {'page': page, 'page_size': page_size, 'partner_id': partner_id}

    result = execude_libspartners(query=query, params=params)
    """
    результат
     {
        'partners_books': [{
            'picture': '', 
            'partner_book_id': '23723613', 
            'year': '1896', 
            'id': '187282', 
            'description': '', 
            'author': 'Коллектив авторов', 
            'libs_book_id': 0, 
            'name': 'Справочная книга о купцах С.-Петербурга на 1896 год'
            }]
     }
    """
    return result


def get_from_elastic_book(name, author):
    from elasticsearch_dsl import Q
    from .documents import BookDocument

    search = BookDocument.search().index('books')
    search = search.query(Q('match', title=name) & Q('match', author_text=author))
    # print('В эластике нашлось {} книг'.format(len(list(search))))

    books = []

    if len(list(search)):
        for item in search:
            #print(item._score, item.id, item.title, item.author)
            if item._score > 28:
                books.append(item.id)
    #else:
        #print('В эластике книги нет')

    if len(books):
        result = True
    else:
        result = False

    return result


def get_from_elastic_author(author):
    from authors.documents import AuthorDocument

    author_ids = []
    # print('Поиск автора')
    search = AuthorDocument.search().index('authors')
    search = search.query('match', name=author)

    for item in search:
        #print(item._score, item.id, item.name)
        if item._score > 15:
            if item.id not in author_ids:
                author_ids.append(item.id)

    return author_ids


def get_from_elastic_genre(genres):
    from genres.documents import GenreDocument

    genres_ids = []
    # print('Поиск жанров')
    search = GenreDocument.search().index('genres')
    search = search.query('match', name=genres)
    #print(search.to_dict())

    for item in search:
        #print(item._score, item.id, item.name)
        if item._score > 10:
            if item.id not in genres_ids:
                genres_ids.append(item.id)

    return genres_ids


def import_from_partners(page=1, page_size=1000, partner_id=1):

    isload = True
    page = page
    page_size = page_size
    newBook = 0
    newAuthor = 0

    while isload:
        partners_books = get_partners_book(page=page, page_size=page_size, partner_id=partner_id)

        if len(partners_books):
            print('Страница №', page)
            page += 1
            for partner_book in partners_books.get('partners_books'):
                #print('-----------Start-------------')
                #print('Пришла книга: {} автор {}'.format(partner_book['name'], partner_book['author']))
                try:
                    Book.objects.get(litres_id=partner_book['partner_book_id'])
                    #print('Книга есть')
                except Book.MultipleObjectsReturned:
                    print('Задвоение книги', partner_book)
                except Book.DoesNotExist:
                    #print('Книги нет, поиск в эластике')

                    if partner_book['author']:
                        result = get_from_elastic_book(partner_book['name'], partner_book['author'])

                        if not result:
                            newBook += 1
                            #print('Добавить книгу:', partner_book)

                            try:
                                if partner_book.get('year') is None:
                                    year = 0
                                else:
                                    year = int(partner_book.get('year'))
                            except ValueError:
                                 year = 0

                            if partner_book.get('isbn', '') is not None:
                                isbn = partner_book.get('isbn', '').replace('-', '')
                            else:
                                isbn = ''

                            book = Book(
                                title=partner_book['name'],
                                year=year,
                                age=int(partner_book.get('age', 0)),
                                rating=float(partner_book.get('rating', 0)),
                                created_by_id=5227,
                                modified_by_id=5227,
                                image=partner_book['picture'],
                                litres_id=partner_book['partner_book_id'],
                                isbn=isbn,
                                description=''
                            )

                            book.save()

                            author_ids = get_from_elastic_author(partner_book['author'])
                            if len(author_ids):
                                #print('Автор есть на либсе', partner_book['author'], author_ids)
                                book.author.set(author_ids)
                            else:
                                #print('Новый автор на либсе', partner_book['author'])
                                newAuthor += 1
                                # author = Author(
                                #     name=partner_book['author']
                                # )
                                # author.save()
                                # book.author.set([author.id])

                            genres_ids = get_from_elastic_genre(partner_book['genres'])
                            if len(genres_ids):
                                #print('Жанр есть на либсе', partner_book['genres'], genres_ids)
                                book.genre_new.set(genres_ids)
                        #else:
                            #print('Книга уже есть на либсе')
                    #else:
                        #print('У книги нет автора, пропускает')
                #print('-----------End-------------')
        else:
            isload = False

    print('Новых книг:', newBook)
    print('Новых авторов:', newAuthor)
