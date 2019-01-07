import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models.functions import Lower
from awards.models import Award



@csrf_exempt
def vue_awards_get(request):
    awards_list = []

    if request.user.is_authenticated:
        data = json.loads(request.body.decode('utf-8'))

        name = data.get('name')

        awards = Award.objects.annotate(lower_name=Lower('name')).order_by('name')
        awards = awards.filter(lower_name__startswith=name.lower())[:30]

        for award in awards:
            item = {
                'id': award.id,
                'name': award.name
            }

            awards_list.append(item)

    return JsonResponse({'awards': awards_list})
