from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from .views import set_questions, test_results, view_all_results, assessment,load_assessment_result,fetch_stnd_QnA,save_assessment_answer
from .queries import test

urlpatterns = (
    [
        path("setquestion/", set_questions, name="setquestion"),
        path("view_all_results/", view_all_results, name="view_all_results"),
        path("result/", test_results, name="result"),
        path("assessment/", assessment, name="assessment"),

        path('load_assessment_res/',load_assessment_result,name="loadResult"),
        path('fetch_stnd_qna/',fetch_stnd_QnA,name="fetch_stnd_qna"),
        path('fetch_exam_qn/',save_assessment_answer,name="fetch_exam_qn"),

        path('testing_db/',test,name="test"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
