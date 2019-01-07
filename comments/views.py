import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from comments.models import Comment


@csrf_exempt
def get(request):
    """
    Получает отзывы к книге
    """
    data = json.loads(request.body.decode('utf-8'))
    book_id = int(data.get('book_id'))
    page_size = int(data.get('count', 10))
    page = int(data.get('page'))

    comment_count = Comment.objects.filter(book_id=book_id).count()

    first = page * page_size - page_size
    last = page * page_size
    comments = Comment.objects.filter(book_id=book_id)[first:last]

    comments_list = []

    for comment in comments:
        comments_list.append({
            'id': comment.id,
            'username': comment.user.username,
            'url': "/users/{}/".format(comment.user.id),
            'text': comment.text,
            'createdDate': comment.date_create
        })

    is_auth = True
    if not request.user.is_authenticated:
        is_auth = False

    return JsonResponse({'comments': comments_list, 'isAuth': is_auth, 'commentCount': comment_count})


@csrf_exempt
def set(request):
    """
    Сохраняет отзыв
    """
    data = json.loads(request.body.decode('utf-8'))
    book_id = int(data.get('book_id'))
    text = data.get('text')
    comment_item = {}

    if request.user.is_authenticated:
        comment = Comment(
            user=request.user,
            text=text,
            book_id=book_id
        )
        comment.save()

        comment_item = {
            'id': comment.id,
            'username': comment.user.username,
            'url': "/users/{}/".format(comment.user.id),
            'text': comment.text,
            'createdDate': comment.date_create
        }

    return JsonResponse({'comment': comment_item})