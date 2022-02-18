# Standard Library imports
import json
import datetime
from os import times
import re
from time import time 

# Django Library imports
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.staticfiles.storage import staticfiles_storage 

# Custom Library imports
from users.views import get_user, get_user_type, is_authenticated_user
from assessment.queries import create_exam, fetch_exam_details_by_name, save_exam_qna, set_student_answer
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

        print("Email:", user_id)
        file_url = staticfiles_storage.path("data/"+user_id+"/questions.json")
        print(file_url)
        file = open(file_url, "w")
        file.write(json.dumps(new_obj, indent=4))
        file.close()
        return HttpResponse(1)


@csrf_exempt
def save_questions(request):
    if request.method == "POST":
        user = get_user(request)
        user_type=user.user_role
        if user_type=='s': 
            user_id = request.POST.get("user_id") 
            qno = int(request.POST.get("question_id")) 
            answer = request.POST.get("answer")
            timeStamp=request.POST.get("finalTime") 
            count=0
            file_url = staticfiles_storage.path("data/"+user_id+"/all_questions.json")
            try:
                with open(file_url, "r+") as file:
                    main_data = json.load(file)
                    data = main_data.get("questions")
                    for q in data:
                        if q.get('id') == qno:
                            print(count)
                            print(len(json.loads(str(timeStamp)))) 
                            q["student_answer"] = answer  
                            timeObj=json.loads(timeStamp)[count].get("time_each")
                            q["time_taken"]["minute"]=timeObj.get("minute")
                            q["time_taken"]["second"]=timeObj.get("second") 
                            print(q)
                        count+=1
                    print(data)
                    main_data.update({"questions": data})
                    file.seek(0)
                    file.truncate()
                    json.dump(main_data, file, indent=4)
                return HttpResponse("success")

            except:
                return HttpResponse("unsuccess")

        elif user_type=='t':
            user_id = request.POST.get("user_id")
            question = request.POST.get("question")
            answer = request.POST.get("answer")
            qno = int(request.POST.get("qno"))
            new_question = {question: answer}
            flag = 0
            file_url = staticfiles_storage.path("data/"+user_id+"/questions.json")
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
                json.dump(main_data, file, indent=4)

            return HttpResponse(flag)
        else:
            pass

    else:
        return HttpResponse("Invaild Request")


@csrf_exempt
def fetch_questions(request):
    if request.method == "POST":
        user_id = get_user(request).email
        user_type=get_user_type(request=request)
        if user_type=="s":
            print(user_id)
            qno = int(request.POST.get("question_id"))
            file_url = staticfiles_storage.path("data/"+user_id+"/all_questions.json")
            print(file_url)
            with open(file_url, "r") as file:
                main_data = json.loads(file.read())
                question_data = main_data.get("questions")
                qstn={}
                try:
                    for question in question_data:
                        if question.get("id")==qno:
                            qstn={
                                "question" : question.get("question"),
                                "answer" : question.get("student_answer")
                            }
                except:
                    pass
            return JsonResponse(qstn)


        elif user_type=="t":
            qno = int(request.POST.get("question_id"))
            file_url = staticfiles_storage.path("data/"+user_id+"/questions.json")
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
            pass
    else:
        return HttpResponse("Invaild Request")


@csrf_exempt
def delete_questions(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        qno = int(request.POST.get("question_id"))
        flag = 1
        file_url = staticfiles_storage.path("data/"+user_id+"/questions.json")
        with open(file_url, "r+") as file:
            main_data = json.load(file)
            data = main_data.get(user_id)
            try:
                data.get("qna").pop(qno - 1)
                main_data.update({user_id: data})
                file.seek(0)
                json.dump(main_data, file, indent=4)
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
        file_url = staticfiles_storage.path("data/"+user_id+"/questions.json")
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

@csrf_exempt
def final_ans_submit(request):
    # set_student_answer(exam_id,question_id,answer,answer_duration,answered_by)
    answered_by = get_user(request)
    file_url = staticfiles_storage.path("data/"+answered_by.email+"/all_questions.json")
    print(file_url)
    answer_duration = datetime.time(0,0,0)
    with open(file_url, "r") as file:
        main_data = json.load(file)
        question_data = main_data.get("questions") 
        for q in question_data:
            flag = set_student_answer(q.get("exam_id"),q.get("id"),q.get("student_answer"),answer_duration,answered_by)[1]
            if(flag == False):
                break
    
    file = open(file_url, "w")
    file.write("{ }")
    file.close()
    if(flag == False):
        return HttpResponse(0)

    return HttpResponse(1)