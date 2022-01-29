from typing import Dict
import json
from django.contrib.auth.hashers import make_password
from django.http.response import HttpResponse, JsonResponse
from rest_framework.views import APIView
from .serializers import userSerializer,RegisterSerializers,RegisterUpdateSerializer
from .models import Register
from rest_framework import serializers, status
from rest_framework.permissions import IsAdminUser,IsAuthenticated,AllowAny
from rest_framework.response import Response
from users.jwtAuth import JWTAuthentication
from users.token_generator import get_access_token,get_refresh_token
from django.shortcuts import render
from django.http import HttpResponseRedirect
#user view or delete.
from django.shortcuts import render, redirect
from .forms import RegisterForm,LogInForm,profileForm ,resetPassInit
from rest_framework import exceptions
from django.urls import reverse
import jwt
from rest_framework import exceptions
from django.conf import settings 
import datetime
from django.http import Http404
from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_protect, requires_csrf_token,ensure_csrf_cookie,csrf_exempt
from django.core.mail import EmailMultiAlternatives 
from django.template.loader import get_template
from django.core.mail import EmailMessage 
from django.template import Context, context
# from 

 
############################################################

def register_view(request):
    if request.method=='POST':
        form=RegisterForm(request.POST)
        if form.is_valid():
            data={
                'first_name':form.cleaned_data['first_name'],
                'last_name':form.cleaned_data['last_name'],
                'user_name':form.cleaned_data['user_name'],
                'email':form.cleaned_data['emailid'],
                'password':form.cleaned_data['user_password']
            }
            if Register.objects.filter(email__iexact=data['email']).exists() ==False:
                serialized=RegisterSerializers(data=data)
                if serialized.is_valid():
                    serialized.save()
                else:
                    raise exceptions.ValidationError(serialized.error_messages())
                return HttpResponseRedirect(reverse('homePage'))
            else:
                return HttpResponse("User already exist with same email.")
    else:
        form=RegisterForm()
    return render(request,'Signup.html',{'form':form})    

def login_view(request):
    if request.method=='POST':
        form=LogInForm(request.POST)
        # print(form)
        if form.is_valid():
            data={
                'email':form.cleaned_data['emailid'],
                'password':form.cleaned_data['user_password']
            }
            user_data=Register.objects.get(email__exact=data.get('email'))
            if user_data.check_password(data.get('password'))==True:
                if user_data.user_role == 't':
                    response=HttpResponseRedirect(reverse('teacher_dashboard'))
                if user_data.user_role == 's':
                    response=HttpResponseRedirect(reverse('student_dashboard'))

                data={
                    'last_login':datetime.datetime.now(datetime.timezone.utc)
                }
                for key,val in data.items():
                        setattr(user_data,key,val)
                user_data.save()
                access_token = get_access_token(user_data)
                refresh_token = get_refresh_token(user_data)
                response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
                response.set_cookie(key='accesstoken',value=access_token,httponly=True)
                response.data = {
                    "token": access_token,
                    "username": user_data.user_name
                }
                return response
            else:
                pass
        else:
            pass
    else:
        form=LogInForm()
    return render(request,'Login.html',{'form':form})

def custom_log_out(request):
    access_token=request.COOKIES.get('accesstoken')
    refresh_token=request.COOKIES.get('refreshtoken')
    response=HttpResponseRedirect(reverse('homePage'))
    if (access_token is not None) and (refresh_token is not None):
        response.delete_cookie('accesstoken')
        response.delete_cookie('refreshtoken')
        return response
    else:
        return response



def is_authenticated_user(request):
    access_token = request.COOKIES.get('accesstoken')
    if access_token is not None:
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            email = payload['email']
            user = Register.objects.get(email=email)
            if user is not None:
                return True
            else:
                return False
        except jwt.ExpiredSignatureError as ex:
            custom_log_out(request)
        except jwt.DecodeError:
            return False
        except Register.DoesNotExist as ne:
            raise exceptions.AuthenticationFailed('invalid email id')
    else:
        return False

def homeView(request):
    if request.method=="GET":  
        context={
            'is_authenticated':is_authenticated_user(request) 
        } 
        return render(request,'Home.html',context) 

def userProfileView(request): 
    try:
        payload_data=jwt.decode(request.COOKIES.get('accesstoken'),settings.SECRET_KEY,algorithms="HS256")
        email=payload_data.get('email')
        try:
            user=Register.objects.get(email__iexact=email) 
            current_year=datetime.datetime.now().year
            user_db=str(user.date_of_birth)
            user_db=str(user.date_of_birth)
            age=user_db
            context={
                'is_authenticated': is_authenticated_user(request), 
                'user':user,
                'age':age
            }
            return render(request,'Userprofile.html',context)
        except Register.DoesNotExist as err:
            raise exceptions.AuthenticationFailed('Invalid email id.')
    except jwt.ExpiredSignatureError or jwt.DecodeError:
        return custom_log_out(request) 

def upDateProfile(request):
    access = request.COOKIES.get('accesstoken')
    decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
    email_id = decoded_data.get('email')
    user = Register.objects.get(email__iexact=email_id)
    if request.method == 'POST':
        form=profileForm(request.POST,request.FILES)
        if form.is_valid():
            data={
                'user_name':form.cleaned_data.get('user_name'),
                'first_name':form.cleaned_data.get('first_name'),
                'last_name':form.cleaned_data.get('last_name'),
                'interests':form.cleaned_data.get('interests'),
                'bio':form.cleaned_data.get('bio'),
                'date_of_birth':form.cleaned_data.get('date_of_birth'),
                'ph_no': form.cleaned_data.get('ph_no'),
            } 
            try:
                user_data=Register.objects.get(email=email_id)
                for key,val in data.items():
                    setattr(user_data,key,val)
                user_data.save()
            except Register.DoesNotExist:
                user_data=Register(**data)
                user_data.save()
           
            # if request.FILES: 
            #     profile_pic=request.FILES['profile_pic']
            #     profile_pic_name=request.FILES['profile_pic'].name
            #     # profile_pic_url=upload_image(profile_pic,profile_pic_name,"Blog/Profile/").get("secure_url")
            #     Register.objects.filter(email__iexact=user.email).update(profile_pic_url=profile_pic_url)
            return redirect('profile')
            
    form=profileForm()
    context={
        'is_authenticated':is_authenticated_user(request),
        'user':user,
        'form':form,
        'user_name': user.user_name,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'interests': user.interests,
        'bio': user.bio,
        'date_of_birth': user.date_of_birth,
        'ph_no': user.ph_no, 
        'profile_pic_url':user.profile_pic_url
    }
    # print(context)
    return render(request, 'updateprofile.html',context)

@csrf_exempt
def contactForm(request):
    if request.method=='POST':
        name=request.POST.get('firstName')+request.POST.get('lastName')
        email=request.POST.get('email')
        message=request.POST.get('message')

        subject,from_email,to='contact',"kedernath.mallick.tint022@gmail.com","kedernath.mallick.tint022@gmail.com"
        text_context=f'{name}wants to contact with you'
        html_content='<p><strong>EMAIL:</strong>'+email+'</p><br><h4>MESSAGE:</h4>'+message
        msg=EmailMultiAlternatives(subject,text_context,from_email,[to])
        msg.attach_alternative(html_content,'text/html')
        msg.send()
        
    return HttpResponse({"msg":"success"})

# @csrf_exempt
# def resetPassword(request,token):
#     if request.method=='POST': 
#         access_tok=token
#         password=request.POST.get('password')
#         conf_password=request.POST.get('conf_password') 
#         if password!=conf_password: 
#             msg={
#                 'st':'nm'
#             }
#             return JsonResponse(msg)
#         else:
#             try:
#                 payload = jwt.decode(access_tok, settings.SECRET_KEY, algorithms="HS256")
#                 email = payload['email']
#                 try:
#                     new_pass=make_password(password)
#                     data={
#                         'password':new_pass
#                     }
#                     user = Register.objects.get(email=email)
#                     for key,val in data.items():
#                         setattr(user,key,val)
#                     user.save()
#                     msg={
#                         "st":"su"
#                     }
#                     return JsonResponse(msg)
#                 except Register.DoesNotExist:
#                     print("user does not exist")
#             except jwt.ExpiredSignatureError as ex:
#                 msg={
#                         "st":"le"
#                     }
#                 return JsonResponse(msg)
#             except jwt.DecodeError:
#                 print("ERROR")
#             except Register.DoesNotExist as ne:
#                 raise exceptions.AuthenticationFailed('invalid email id') 
#     # print(make_password("token")) 
#     context={
#         'token':token,
#         'is_authenticated':is_authenticated_user(request)
#     }
#     return render(request,'resetPassword.html',context)


# @csrf_exempt
# def resetPasswordInit(request):
#     if request.method=='POST':
#         email=request.POST.get('email')
#         user=Register.objects.filter(email=email)
#         print(email)
#         if user.exists() is False:
#             msg={
#                 "st":"er",
#                 "ms":"please give the verified email with your account"
#             }
#             return JsonResponse(msg)
#         else:
#             msg={
#                 "st":"su",
#                 "ms":"We have e-mailed your password reset link!"
#             }
#             access_token=get_access_token(Register.objects.get(email=email))
#             ctx={
#                 'resetPass_url':'http://127.0.0.1:8000/'+'reset_password/'+access_token
#             }
#             message = get_template("emails/reset_pass.html").render(ctx)
#             mail = EmailMessage(
#                 subject="Reset Password",
#                 body=message,
#                 from_email="kedernath.mallick.tint022@gmail.com",
#                 to=["kedernath.mallick.tint022@gmail.com"],
#                 reply_to=["kedernath.mallick.tint022@gmail.com"],
#             )
#             mail.content_subtype = "html"
#             mail.send()
#
#             return JsonResponse(msg)
#     context={
#         'is_authenticated':is_authenticated_user(request),
#     }
#     return render(request,'resetPasswordInit.html',context)


def get_user_type(request):
    access_token = request.COOKIES.get('accesstoken')
    if access_token is not None:
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            email = payload['email']
            user = Register.objects.get(email=email)
            if user is not None:
                return user.user_role

        except jwt.ExpiredSignatureError as ex:
            custom_log_out(request)
        except jwt.DecodeError:
            return False
        except Register.DoesNotExist as ne:
            raise exceptions.AuthenticationFailed('invalid email id')
    else:
        return False



def teacher_dashboard(request):
    data = [1,2,3,4,5,6,7,8,9,10]

    context = {
        'is_authenticated': is_authenticated_user(request),
        'exam_pages': data
    }

    if get_user_type(request) == 't':
        return render(request, 'TeacherDashboard.html', context)
    else:
        return render(request, 'Error.html', context)


def student_dashboard(request):
    data = [1,2,3,4,5,6,7,8,9,10]

    context = {
        'is_authenticated': is_authenticated_user(request),
        'exam_pages': data
    }
    if get_user_type(request) == 's':
        return render(request, 'StudentDashboard.html', context)
    else:
        return render(request, 'Error.html', context)
