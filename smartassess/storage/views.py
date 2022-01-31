from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def save_questions(request):
    if request.method == "POST":
        q = request.POST.get("question")
        return HttpResponse(q)
    else:
        return HttpResponse("Invaild Request")