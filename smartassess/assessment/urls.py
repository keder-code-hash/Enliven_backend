from django.urls import path
from django.urls.conf import include 
from django.conf import settings
from django.conf.urls.static import static
from .views import  set_questions


urlpatterns=[   
    path('setquestion/',set_questions,name='setquestion'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
