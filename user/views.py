from django.shortcuts import render
from django.contrib.auth.models import User
from user_profile.models import Profile
from django.http import Http404


def users(request):
    to_template = {}
    return render(request, 'users.html', to_template)


def user(request, pk=None, username=None):
    try:
        if pk:
            user = User.objects.get(pk=pk)
            url = "/users/{}".format(pk)
        elif username:
            user = User.objects.get(username=username)
            url = "/users/{}".format(username)

        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user)

        to_template = {
            'username': user.username,
            'url': url,
            'avatar': profile.get_avatar_small()
        }

    except User.DoesNotExist:
        raise Http404()

    return render(request, 'user.html', to_template)
