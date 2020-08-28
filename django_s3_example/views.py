from django.http import HttpResponse, JsonResponse


def file_save_view(request):
    return JsonResponse({'message': 'file saved'})

def file_load_view(request):
    return JsonResponse({'file': '...'})