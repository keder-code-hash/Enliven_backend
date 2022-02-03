# Standard Library imports
import json
import datetime

# Django Library imports
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import MultipleObjectsReturned
from django.contrib.staticfiles.storage import staticfiles_storage

# Custom Library imports
from users.views import get_user, is_authenticated_user
from assessment.queries import create_exam, fetch_exam_details_by_name, save_exam_qna
from assessment.models import Question


@csrf_exempt
def save_examname(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        exam_name = request.POST.get("exam_name")
        topic = request.POST.get("topic")
        exam_details = request.POST.get("exam_details")
        marks = request.POST.get("marks")
        hr = int(request.POST.get("hr"))
        min = int(request.POST.get("min"))
        duration = datetime.time(hr, min, 00)
        # create_exam(exam_name,marks,duration,created_by,course_name='default',description=None)

        new_obj = {
            user_id: {
                "exam_name": exam_name,
                "topic": topic,
                "exam_details": exam_details,
                "marks": marks,
                "qna": [],
            }
        }

        if (
            create_exam(
                exam_name, marks, duration, get_user(request), topic, exam_details
            )[1]
            is False
        ):
            return HttpResponse(0)

        file_url = staticfiles_storage.path("data/questions.json")
        with open(file_url, "r+") as file:
            data = json.load(file)
            data.update(new_obj)
            file.seek(0)
            json.dump(data, file)

        return HttpResponse(1)


@csrf_exempt
def save_questions(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        question = request.POST.get("question")
        answer = request.POST.get("answer")
        qno = int(request.POST.get("qno"))
        new_question = {question: answer}
        flag = 0
        file_url = staticfiles_storage.path("data/questions.json")
        with open(file_url, "r+") as file:
            main_data = json.load(file)
            data = main_data.get(user_id)
            length = len(data.get("qna"))
            if qno <= length:
                data.get("qna")[qno - 1] = new_question
                flag = 1

            else:
                data.get("qna").append(new_question)

            main_data.update({user_id: data})
            file.seek(0)
            json.dump(main_data, file)

        return HttpResponse(flag)

    else:
        return HttpResponse("Invaild Request")


@csrf_exempt
def fetch_questions(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        qno = int(request.POST.get("question_id"))
        file_url = staticfiles_storage.path("data/questions.json")
        with open(file_url, "r") as file:
            main_data = json.load(file)
            data = main_data.get(user_id)
            try:
                qna_dict = data.get("qna")[qno - 1]
                for q, a in qna_dict.items():
                    qna = {"question": q, "answer": a}
            except IndexError:
                qna = {"question": "", "answer": ""}

        return JsonResponse(qna)
    else:
        return HttpResponse("Invaild Request")


@csrf_exempt
def delete_questions(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        qno = int(request.POST.get("question_id"))
        flag = 1
        file_url = staticfiles_storage.path("data/questions.json")
        with open(file_url, "r+") as file:
            main_data = json.load(file)
            data = main_data.get(user_id)
            try:
                data.get("qna").pop(qno - 1)
                main_data.update({user_id: data})
                file.seek(0)
                json.dump(main_data, file)
                file.truncate()
            except IndexError:
                flag = 0
        return HttpResponse(flag)

    else:
        return HttpResponse("Invaild Request")


@csrf_exempt
def final_submit(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        file_url = staticfiles_storage.path("data/questions.json")
        with open(file_url, "r") as file:
            main_data = json.load(file)
            exam_name = main_data.get(user_id).get("exam_name")

        exam = fetch_exam_details_by_name(exam_name)[0]
        exam_id = exam.get("id")
        if save_exam_qna(file_url, exam_id):
            file = open(file_url, "w")
            file.write("{ }")
            file.close()
            return HttpResponse(1)
        else:
            return HttpResponse(0)

    else:
        return HttpResponse("Invaild Request")


############################## Answer ################################


@csrf_exempt
def save_answer(request):
    exam_id = None

    if request.method == "POST":
        exam_id = request.body.decode("utf-8")

    print(exam_id)  # debug
