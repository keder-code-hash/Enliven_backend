from users.jwtAuth import refresh_acsess_token
from django.contrib.auth.models import User
from django.urls import path
from django.urls.conf import include
from rest_framework.urlpatterns import format_suffix_patterns
import rest_framework
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import Users, contactForm,register_view,login_view,custom_log_out,homeView,userProfileView,upDateProfile
# from django.contrib.auth.views import logout


urlpatterns=[ 
    path('api/', Users.as_view()),
    path('register/',register_view,name='register'),
    path('', homeView, name='homePage'),
    path('login/',login_view,name='login'), 
    path('logout/',custom_log_out,name='logout'), 
    path('refreshtoken/',refresh_acsess_token),
    path('contact',contactForm,name='contact'), 
    path('profile/',userProfileView,name='profile'), 
    path('updateProfile/', upDateProfile, name='updateProfile'),
    # path('reset_password/<str:token>/',views.resetPassword,name='reset_password'),
    
    # path('reset_password_init/',views.resetPasswordInit,name='reset_password_init')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
