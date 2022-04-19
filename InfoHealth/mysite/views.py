from django.shortcuts import render
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def api_test(request):

    context = {
        "message": "Welcome to the InfoHealth API!"
    }


    return JsonResponse(context)

@csrf_exempt
def post_url(request):

    if request.method == "POST":
        context={"message": "POST request received", "data": request.POST["url"]}
        return JsonResponse(context)
    else:
        return JsonResponse({"message": "Please use POST method"})