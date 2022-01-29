from django.shortcuts import render
# importing Django modules
from django.http import HttpResponse


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
    return HttpResponse("Set Questions (accessible by Teacher)")


# view results of all students (accessible by teacher only)
def view_results(request):
    return HttpResponse("View Results (accessible by Teacher)")
