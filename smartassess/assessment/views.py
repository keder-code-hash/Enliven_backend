from re import sub
from django.shortcuts import render

# importing Django modules
from django.http import HttpResponse
from users.views import is_authenticated_user

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


# view all results
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
def self_assessment(request):
    return HttpResponse("Self Assessment")


# set questions for examination (accessible by teacher only)
def set_questions(request):
    questions_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
    context = {
        "questions_num": questions_list,
        "is_authenticated": is_authenticated_user(request),
    }
    if context["is_authenticated"]:
        return render(request, "Examset.html", context)
    else:
        err_log = {
            "msg" : "Are you logged in?"
        }
        return render(request, "Error.html", err_log)


# view results of all students (accessible by teacher only)
def view_results(request):
    return HttpResponse("View Results (accessible by Teacher)")
