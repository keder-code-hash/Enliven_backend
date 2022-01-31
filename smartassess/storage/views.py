from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.staticfiles.storage import staticfiles_storage

@csrf_exempt
def save_examname(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        exam_name = request.POST.get("exam_name")
        topic = request.POST.get("topic")
        exam_details = request.POST.get("exam_details")
        new_obj = {
            user_id : {
                "exam_name" : exam_name,
                "topic" : topic,
                "exam_details" : exam_details,
                "qna": []
            }
        }
        file_url = staticfiles_storage.path('data/questions.json')
        with open(file_url, 'r+') as file:
            data = json.load(file)
            data.update(new_obj)
            file.seek(0)
            json.dump(data, file)


@csrf_exempt
def save_questions(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        new_question = {question:answer}
        file_url = staticfiles_storage.path('data/questions.json')
        with open(file_url, 'r+') as file:
            main_data = json.load(file)
            data = main_data.get(user_id)
            data.get('qna').append(new_question)
            qno = len(data.get('qna'))
            print({user_id : data})
            main_data.update({user_id : data})
            file.seek(0)
            json.dump(main_data, file)
        
        return HttpResponse(qno)
    else:
        return HttpResponse("Invaild Request")

@csrf_exempt
def fetch_questions(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        qno = request.POST.get("question_id")
        file_url = staticfiles_storage.path('data/questions.json')
        with open(file_url, 'r') as file:
            main_data = json.load(file)
            data = main_data.get(user_id)
            qna_dict = data.get('qna')[int(qno)-1]
            for q, a in qna_dict.items():
                qna = {
                    "question" : q,
                    "answer" : a
                }
        
        return JsonResponse(qna)
    else:
        return HttpResponse("Invaild Request")