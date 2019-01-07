from django.shortcuts import render


def right(request):
    return render(request, 'info/right.html')


def rule(request):
    return render(request, 'info/rule.html')