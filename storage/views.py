# Standard Library imports
import json
import datetime
# Django Library imports
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from django.contrib.staticfiles.storage import staticfiles_storage 

# Custom Library imports
from users.views import get_user, get_user_type
from assessment.queries import create_exam, fetch_exam_details_by_name, save_exam_qna, set_student_answer


@csrf_exempt
def save_examname(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        exam_name = request.POST.get("exam_name")
        topic = request.POST.get("topic")
        exam_details = request.POST.get("exam_details")
        hr = int(request.POST.get("hr"))
        min = int(request.POST.get("min"))
        duration = datetime.time(hr, min, 00)
        # create_exam(exam_name,marks,duration,created_by,course_name='default',description=None)

        new_obj = {
            user_id: {
                "exam_name": exam_name,
                "topic": topic,
                "exam_details": exam_details,
                "marks": 0,
                "qna": [],
            }
        }

        if (
            create_exam(
                exam_name, 0, duration, get_user(request), topic, exam_details
            )[1]
            is False
        ):
            return HttpResponse(0)

        file_url = staticfiles_storage.path("data/"+user_id+"/questions.json")
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
            file_url = staticfiles_storage.path("data/"+user_id+"/all_questions.json")
            try:
                with open(file_url, "r+") as file:
                    main_data = json.load(file)
                    data = main_data.get("questions")
                    for q in data:
                        if q.get('id') == qno:
                            q["student_answer"] = answer    
                    main_data.update({"questions": data})
                    file.seek(0)
                    file.truncate()
                    json.dump(main_data, file, indent=4)
                    file.close()
                return HttpResponse("success")

            except:
                return HttpResponse("unsuccess")

        elif user_type=='t':
            user_id = request.POST.get("user_id")
            question = request.POST.get("question")
            answer = request.POST.get("answer")
            qno = int(request.POST.get("qno"))
            full_marks = int(request.POST.get("fullMarks"))

            try:
                marks = int(request.POST.get("marks"))
            except:
                marks = 1

            new_question = {
                "question":question,
                "answer": answer,
                "marks":marks
                }
            flag = 0
            file_url = staticfiles_storage.path("data/"+user_id+"/questions.json")
            with open(file_url, "r+") as file:
                main_data = json.load(file)
                data = main_data.get(user_id)
                data["marks"] = full_marks
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
            # print(user_id)
            qno = int(request.POST.get("question_id"))
            file_url = staticfiles_storage.path("data/"+user_id+"/all_questions.json")
            # print(file_url)
            with open(file_url, "r") as file:
                main_data = json.loads(file.read())
                question_data = main_data.get("questions")
                qstn={}
                try:
                    for question in question_data:
                        if question.get("id")==qno:
                            qstn={
                                "question" : question.get("question"),
                                "answer" : question.get("student_answer"),
                                "marks" : question.get("qstn_marks")
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
                    qna = {
                        "question": qna_dict.get("question"), 
                        "answer": qna_dict.get("answer"),
                        "marks": qna_dict.get("marks")
                    }
                except IndexError:
                    qna = {"question": "", "answer": "", "marks":0}

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
            main_data = json.load(file).get(user_id)
            exam_name = main_data.get("exam_name")

        exam = fetch_exam_details_by_name(exam_name)
        exam_id = exam.get("id")
        if save_exam_qna(user_id, file_url, exam_id):
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
    
    timeStamp=request.POST.get("finalTime") 
    timeArray=json.loads(timeStamp)
    # print(timeArray)
    # print(json.loads(json.dumps(timeArray[0])))  
    try:
        with open(file_url, "r+") as file:
            main_data = json.load(file)
            data = main_data.get("questions")
            for q in data:
                id=int(q.get('id') )  
                for timeObj in timeArray:
                    obj=json.loads(json.dumps(timeObj))
                    # print(obj["q_id"])
                    if(int(obj["q_id"])==id):
                        each_time_obj=json.loads(json.dumps(obj.get('time_each')))
                        # print("each_time_obj")  
                        q["time_taken"]["minute"]=each_time_obj.get("minute")
                        q["time_taken"]["second"]=each_time_obj.get("second")   
            main_data.update({"questions": data})
            file.seek(0)
            file.truncate()
            json.dump(main_data, file, indent=4)
    except:
        pass 
    with open(file_url, "r") as file:
        main_data = json.load(file)
        # print(main_data)
        question_data = main_data.get("questions") 
        # print(question_data)
        for q in question_data:
            try:
                answer_duration = datetime.time(0,int(q['time_taken']['minute']),int(q['time_taken']['second']))
            except:
                answer_duration = datetime.time(0,0,0)
            flag = set_student_answer(q.get("exam_id"),q.get("id"),q.get("student_answer"),answer_duration,answered_by)[1]
            if(flag == False):
                break
    
    file = open(file_url, "w")
    file.write("{ }")
    file.close()
    if(flag == False):
        return HttpResponse(0)
    else:
        return HttpResponse(1)