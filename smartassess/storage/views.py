from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def save_questions(request):
    if request.method == "POST":
        q = request.POST.get("question")
        return JsonResponse({"key":"got question"})
    else:
        return HttpResponse("Invaild Request")