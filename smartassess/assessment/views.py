import json 

# importing Django modules
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render 
from users.views import is_authenticated_user, get_user
from django.contrib.staticfiles.storage import staticfiles_storage 
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
# Custom module imports
from assessment.models import Answer, Exam, Question


@csrf_exempt
def load_assessment_result(request):
    if request.method=="POST":
        user=get_user(request=request)
        email_id=user.email
        exam_id=request.POST.get("exam_id")
        try:
            exam_dets=Exam.objects.filter(id=exam_id).values()
            data=Question.objects.filter(exam_id=exam_id).values() 
            all_questions=list(data)
            try:
                file_url = staticfiles_storage.path('data/assessment_details.json')
                json_data=open(file_url,mode='w',encoding='utf-8')
                for question in all_questions:
                    student_answer=Answer.objects.get(exam_id=exam_id,question_id=question["id"],answered_by__email=email_id) 
                    question['student_answer']=student_answer.answer
                    question.pop("created_at") 
                exam_dets=list(exam_dets)[0] 
                time={
                    "hour":exam_dets["duration"].hour,
                    "minute":exam_dets["duration"].minute
                } 
                exam_dets["duration"]=time
                exam_dets.pop("created_at")
                print()
                assessment_set={
                    "exam":exam_dets,
                    "ass_set":all_questions
                }
                json_obj=json.dumps(assessment_set,indent=4)
                json_data.write(json_obj)
                return JsonResponse({"st":1})
            except ObjectDoesNotExist:
                return JsonResponse({"st":0})
        except FileNotFoundError: 
            return JsonResponse({"st":0})
# test results
def test_results(request):
    try:
        file_url = staticfiles_storage.path('data/assessment_details.json')
        json_data=open(file_url,mode='r',encoding='utf-8')
        data=json.loads(json_data.read())
        exam_details=data.get('exam')
        actual_ans=data.get('ass_set')
    except:
        pass

    context = {
        "exam":exam_details,
        "actual_ans":actual_ans,
        "question_no":len(actual_ans),
        "is_authenticated": is_authenticated_user(request),
    }

    return render(request, "StudentResult.html", context)
@csrf_exempt
def fetch_stnd_QnA(request):
    if request.method=="POST":
        id=request.POST.get('set_id')
        try:
            file_url = staticfiles_storage.path('data/assessment_details.json')
            json_data=open(file_url,mode='r',encoding='utf-8')
            data=json.loads(json_data.read())  
            actual_ans=data.get('ass_set')[int(id)-1]
            json_data.close()
            print(actual_ans)
            context = { 
                "actual_ans":actual_ans, 
            } 
            return JsonResponse(context)
        except:
            pass
        return JsonResponse({})

        

# view results of all students (accessible by teacher only)
def view_all_results(request):
    result = [
        {"name": "Arghya", "roll": 3685128, "marks": 60},
        {"name": "Purnadip", "roll": 6123465, "marks": 70},
        {"name": "Keder", "roll": 8541236, "marks": 80},
        {"name": "Random", "roll": 7845126, "marks": 90},
    ]
    subject = "OOP"

    context = {
        "details": result,
        "subject": subject,
        "is_authenticated": is_authenticated_user(request),
    }

    return render(request, "TeacherResult.html", context)


# self assessment
@csrf_exempt
def assessment(request):
    if request.method == "POST":
        exam_id = request.body.decode("utf-8")

    exam_id = 3
    question_list = Question.objects.filter(exam_id=exam_id).values() 
    question_list = list(question_list)
    try:
        file_url = staticfiles_storage.path('data/all_questions.json')
        json_data=open(file_url,mode='w',encoding='utf-8')
        for exam in question_list: 
            exam['student_answer']=""
            exam.pop("created_at")
            exam.pop("standard_ans")

        exams={"questions":question_list}
        json_obj=json.dumps(exams,indent=4)
        json_data.write(json_obj)
    except FileNotFoundError:
        pass
    # print(question_list)

    context = {
        "is_authenticated": is_authenticated_user(request),
        "qno": question_list,
        "max_no": len(question_list)
    }
    return render(request, "AttemptExam.html", context)


# set questions for examination (accessible by teacher only)
def set_questions(request):
    user = get_user(request)
    file_url = staticfiles_storage.path("data/questions.json")
    data = ""
    with open(file_url, "r+") as file:
        data = json.load(file).get(user.user_name)

    qno = list(range(1, len(data.get("qna")) + 2))
    max_qno = len(qno)
    if qno == []:
        qno = [1]
        max_qno = 1
    context = {
        "is_authenticated": is_authenticated_user(request),
        "user": user,
        "data": data,
        "qno": qno,
        "max_qno": max_qno,
    }
    if context["is_authenticated"] and user.user_role == "t":
        return render(request, "Examset.html", context)
    else:
        err_log = {"msg": "Are you logged in?"}
        return render(request, "Error.html", err_log)


def view_results(request):
    return HttpResponse("View Results (accessible by Teacher)")
