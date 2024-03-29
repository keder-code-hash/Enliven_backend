from django.urls import path
from storage.views import *

urlpatterns = [
    path("save/", save_questions, name="tempSaveQnA"),
    path("saveexamname/", save_examname, name="saveExamName"),
    path("fetchqna/", fetch_questions, name="fetchQnA"),
    path("deleteqna/", delete_questions, name="deleteQnA"),
    path("finalsubmit/", final_submit, name="finalSubmit"), 
    path("finalanssubmit/", final_ans_submit, name="finalAnsSubmit"), 
]
