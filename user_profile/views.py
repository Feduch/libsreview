import json
from django.db import IntegrityError
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from user_profile.models import Profile
from publications.models import Publication
from collection.models import Collection
from ratings.models import StarRatings
from allauth.account.models import EmailAddress


@login_required
def index(request):
    if not request.user.is_authenticated:
        redirect('/')
    return render(request, 'profile/profile.html')


@csrf_exempt
def get(request):
    to_template = {}
    if request.user.is_authenticated:
        # Профайл пользователя
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = Profile(user=request.user)
            profile.save()

        to_template['profile'] = {
            'username': profile.user.username,
            'email': profile.user.email
        }

        if profile.avatar:
            to_template['profile']['avatar'] = profile.avatar.url
        else:
            to_template['profile']['avatar'] = 'data:image/svg+xml;charset=UTF-8,%3Csvg%20width%3D%2275%22%20height%3D%2275%22%20xmlns%3D%22http%3A%2F%2Fwww.w3.org%2F2000%2Fsvg%22%20viewBox%3D%220%200%2075%2075%22%20preserveAspectRatio%3D%22none%22%3E%3Cdefs%3E%3Cstyle%20type%3D%22text%2Fcss%22%3E%23holder_16571ccf1dd%20text%20%7B%20fill%3Argba(255%2C255%2C255%2C.75)%3Bfont-weight%3Anormal%3Bfont-family%3AHelvetica%2C%20monospace%3Bfont-size%3A10pt%20%7D%20%3C%2Fstyle%3E%3C%2Fdefs%3E%3Cg%20id%3D%22holder_16571ccf1dd%22%3E%3Crect%20width%3D%2275%22%20height%3D%2275%22%20fill%3D%22%23777%22%3E%3C%2Frect%3E%3Cg%3E%3Ctext%20x%3D%2218.5546875%22%20y%3D%2242%22%3E75x75%3C%2Ftext%3E%3C%2Fg%3E%3C%2Fg%3E%3C%2Fsvg%3E'

        # Книги которые пользователь оценил
        ratings = StarRatings.objects.filter(user=request.user, book__isnull=False)
        to_template['books'] = []

        for rating in ratings:
            to_template['books'].append({
                'id': rating.book_id,
                'url': rating.book.get_absolute_url(),
                'title': rating.book.title,
                'authors': rating.book.get_link_authors(),
                'genres': rating.book.get_link_genres(),
                'rating': rating.book.rating,
                'userRating': rating.rating,
                'show_counter': rating.book.show_counter,
                'year': rating.book.year,
                'description': rating.book.description,
                'image': rating.book.get_image_preview()
            })

        # Посты пользователя
        posts = Publication.objects.filter(user=request.user)
        to_template['posts'] = []

        for post in posts:
            item = {
                'id': post.pk,
                'detailText': post.detail_text,
                'title': post.title,
                'showCounter': post.show_counter,
                'rating': post.rating,
                'dateUpdate': post.date_update,
                'url': post.get_absolute_url()
            }

            if post.image:
                item['image'] = post.image.url

            to_template['posts'].append(item)

        # Коллекции пользователя
        collections = Collection.objects.filter(user=request.user)
        to_template['collections'] = []

        for collection in collections:
            item = {
                'id': collection.pk,
                'text': collection.text,
                'title': collection.title,
                'showCounter': collection.show_counter,
                'rating': collection.rating,
                'dateUpdate': collection.date_update,
                'books': collection.book.all().count(),
                'url': collection.get_absolute_url()
            }

            if collection.image:
                item['image'] = collection.image.url

            to_template['collections'].append(item)

    return JsonResponse(to_template)


@csrf_exempt
def save(request):
    to_template = []
    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))

        profile = data.get('profile')
        password = data.get('password')

        try:
            user = User.objects.get(pk=request.user.id)
            user.username = profile.get('username')
            user.save(update_fields=['username'])
            to_template.append({'type': 'success', 'text': 'Имя пользователя сохранено', 'title': 'Успешно'})

            if password:
                user.set_password(data.get('password'))
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                to_template.append({'type': 'success', 'text': 'Пароль изменен', 'title': 'Успешно'})

        except User.DoesNotExist:
            to_template.append({'type': 'error', 'text': 'Ошибка, попробуйте позже', 'title': 'Ошибка'})
        except IntegrityError:
            to_template.append({'type': 'error', 'text': 'Это имя уже занято', 'title': 'Ошибка'})

    return JsonResponse({'result': to_template})


@csrf_exempt
def avatar_save(request):
    to_template = {
        'result': [],
        'avatar': None
    }
    if request.user.is_authenticated:
        avatar = request.FILES.get('avatar')
        try:
            if avatar:
                profile = Profile.objects.get(user=request.user)
                profile.avatar.save(avatar.name, avatar)
                to_template['avatar'] = profile.avatar.url
                to_template['result'].append({'type': 'success', 'text': 'Аватар изменен', 'title': 'Успешно'})
        except Profile.DoesNotExist:
            to_template['result'].append({'type': 'error', 'text': 'Ошибка, попробуйте позже', 'title': 'Ошибка'})

    return JsonResponse(to_template)


@csrf_exempt
def singin(request):
    to_template = {
        'result': [],
        'reload': False
    }
    data = json.loads(request.body.decode('utf-8'))

    email = data.get('email')
    password = data.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        to_template['result'].append({'type': 'success', 'text': 'Вы авторизованы', 'title': 'Успешно'})
        login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
        to_template['reload'] = True
    else:
        to_template['result'].append({'type': 'error', 'text': 'Не верный логин или пароль', 'title': 'Ошибка'})

    return JsonResponse(to_template)


@csrf_exempt
def reg(request):
    to_template = {
        'result': [],
        'reload': False
    }
    data = json.loads(request.body.decode('utf-8'))

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')

    try:
        User.objects.get(email=email)
        to_template['result'].append({'type': 'error', 'text': 'Пользователь с таким email уже зарегистрирован', 'title': 'Ошибка'})
    except User.DoesNotExist:
        try:
            User.objects.get(username=username)
            to_template['result'].append(
                {'type': 'error', 'text': 'Имя пользователя занято, попробуйте другое', 'title': 'Ошибка'})
        except User.DoesNotExist:
            user = User.objects.create_user(username, email, password)
            to_template['result'].append({'type': 'success', 'text': 'Вы зарегистрированы и авторизованы', 'title': 'Успешно'})
            login(request, user, backend='allauth.account.auth_backends.AuthenticationBackend')
            to_template['reload'] = True
            EmailAddress.objects.create(user=user, email=email, primary=True, verified=True)

    return JsonResponse(to_template)


@csrf_exempt
def reset(request):
    to_template = {
        'result': []
    }

    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')

    try:
        user = User.objects.get(email=email)
        to_template['result'].append(
            {'type': 'success', 'text': 'На {} выслали новый пароль'.format(email), 'title': 'Успешно'})
        password = User.objects.make_random_password()
        user.set_password(password)

        try:
            send_mail(
                'Libs.ru: Новый пароль',
                'Ваш новый пароль: {}'.format(password),
                'noreply@libs.ru',
                [email],
                fail_silently=False,
            )
        except Exception:
            to_template['result'].append(
                {'type': 'error', 'text': 'Письмо с новым паролем не отправилось', 'title': 'Ошибка'})

    except User.DoesNotExist:
        to_template['result'].append(
            {'type': 'error', 'text': 'Пользователь с таким email не найден', 'title': 'Ошибка'})

    return JsonResponse(to_template)