import json
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from subscribe.models import Subscriber


@api_view(['POST', 'DELETE'])
@permission_classes((AllowAny, ))
def subscribe(request, format=None):
    """
    Подписка на уведомления:
    - о начале продажи книг,
    - обнолвение коллекций,
    - появление новых книг у автора
    """
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        book_id = data.get('book_id')
        author_id = data.get('author_id')
        collection_id = data.get('collection_id')

        if book_id:
            try:
                Subscriber.objects.get(email=email, book_id=book_id)

                content = {
                    'info': 'Вы уже подписаны',
                    'isIsset': True
                }
                return Response(content, status.HTTP_200_OK)
            except Subscriber.DoesNotExist:
                Subscriber(
                    email=email,
                    book_id=book_id
                ).save()

                content = {
                    'info': 'Вы подписаны'
                }
                return Response(content, status.HTTP_200_OK)

        if author_id:
            try:
                Subscriber.objects.get(email=email, author_id=author_id)

                content = {
                    'info': 'Вы уже подписаны',
                    'isIsset': True
                }
                return Response(content, status.HTTP_200_OK)
            except Subscriber.DoesNotExist:
                Subscriber(
                    email=email,
                    author_id=author_id
                ).save()

                content = {
                    'info': 'Вы подписаны'
                }
                return Response(content, status.HTTP_200_OK)

        if collection_id:
            try:
                Subscriber.objects.get(email=email, collection_id=collection_id)

                content = {
                    'info': 'Вы уже подписаны',
                    'isIsset': True
                }
                return Response(content, status.HTTP_200_OK)
            except Subscriber.DoesNotExist:
                Subscriber(
                    email=email,
                    collection_id=collection_id
                ).save()

                content = {
                    'info': 'Вы подписаны'
                }
                return Response(content, status.HTTP_200_OK)

    if request.method == 'DELETE':
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email')
        book_id = data.get('book_id')
        author_id = data.get('author_id')
        collection_id = data.get('collection_id')

        if book_id:
            Subscriber.objects.filter(email=email, book_id=book_id).delete()

            content = {
                'info': 'Вы отписаны'
            }
            return Response(content, status.HTTP_200_OK)

        if author_id:
            Subscriber.objects.filter(email=email, author_id=author_id).delete()

            content = {
                'info': 'Вы отписаны'
            }
            return Response(content, status.HTTP_200_OK)

        if collection_id:
            Subscriber.objects.filter(email=email, collection_id=collection_id).delete()

            content = {
                'info': 'Вы отписаны'
            }
            return Response(content, status.HTTP_200_OK)

    content = {
        'info': 'Ошика, попробуйте позже'
    }
    return Response(content, status.HTTP_404_NOT_FOUND)


def send_notify(book_id=None, collection_id=None):
    """Высылает уведомление подписчику"""
    if book_id:
        subscribers = Subscriber.objects.filter(book__id=book_id)

        for subscriber in subscribers:
            try:
                subject, from_email, to = 'Libs.ru: Книга {} поступила в продажу'.format(subscriber.book.title), 'noreply@libs.ru', subscriber.email
                html_content = '<p>Здравствуйте!</p>' \
                               '<p>Книга <a href="https://libs.ru{0}?utm_source=email&utm_medium=subscribe&utm_campaign=book&utm_content={1}">{1}</a> поступила в продажу. ' \
                               '<a href="https://libs.ru{0}?utm_source=email&utm_medium=subscribe&utm_campaign=book&utm_content={1}">Посмотреть цены</a>.</p>' \
                               '<p>Вы получили это сообщение, потому что были подписаны на уведомление для этой книги. ' \
                               'Ваш email удален из списка рассылки.</p>'.format(subscriber.book.get_absolute_url(), subscriber.book.title)
                msg = EmailMessage(subject, html_content, from_email, [to])
                msg.content_subtype = "html"
                msg.send()

                subscriber.delete()
            except Exception as e:
                print ('Не ушло письмо для {} о книге {}'.format(subscriber.email, subscriber.book.title))

    if collection_id:
        pass

    return True
