from django.shortcuts import render
# importing Django modules
from django.http import HttpResponse
from  users.views import is_authenticated_user

# index page
def index(request):
    return HttpResponse("Landing Page")


# test page
def test(request):
    return HttpResponse("Test Page")


# test results
def test_results(request):
    return HttpResponse("Test results")


# self assessment
def self_assessment(request):
    return HttpResponse("Self Assessment")


# set questions for examination (accessible by teacher only)
def set_questions(request): 
    questions_list=[1,2,3,4,5,6]
    context={
            "questions_num":questions_list,
            'is_authenticated':is_authenticated_user(request) 
        } 
    return render(request,'Examset.html',context)


# view results of all students (accessible by teacher only)
def view_results(request):
    return HttpResponse("View Results (accessible by Teacher)")
