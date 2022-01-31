from django.urls import path
from storage.views import *

urlpatterns = (
    [
        path("save/", save_questions)
    ]
)
