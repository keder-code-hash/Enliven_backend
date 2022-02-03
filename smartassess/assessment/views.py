import json

# importing Django modules
from django.http import HttpResponse
from django.shortcuts import render
from users.views import is_authenticated_user, get_user
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.exceptions import MultipleObjectsReturned
from django.views.decorators.csrf import csrf_exempt

# Custom module imports
from assessment.models import Question


# index page
def index(request):
    return HttpResponse("Landing Page")


# test page
def test(request):
    return HttpResponse("Test Page")


# test results
def test_results(request):
    exam_title = "Object Oriented Programming"
    total_marks = 100
    score = 80
    details = [
        {
            "q_no": 1,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 2,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 3,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 4,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 5,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
    ]

    context = {
        "details": details,
        "score": score,
        "exam_title": exam_title,
        "total_marks": total_marks,
        "is_authenticated": is_authenticated_user(request),
    }

    return render(request, "StudentResult.html", context)


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
            exam["created_at"]="" 
            exam['student_answer']=""
        exams={"questions":question_list}
        json_obj=json.dumps(exams,indent=4)
        json_data.write(json_obj)
    except FileNotFoundError:
        pass
    # print(question_list)

    context = {
        "is_authenticated": is_authenticated_user(request),
        "question_list": question_list,
        "qno": question_list,
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
