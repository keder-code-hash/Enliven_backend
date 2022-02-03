from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static
from .views import set_questions, test_results, view_all_results, assessment,load_assessment_result
from .queries import test

urlpatterns = (
    [
        path("setquestion/", set_questions, name="setquestion"),
        path("view_all_results/", view_all_results, name="view_all_results"),
        path("result/", test_results, name="result"),
        path("assessment/", assessment, name="assessment"),

        path('load_assessment_res/',load_assessment_result,name="loadResult")
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
