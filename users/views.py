import os
<<<<<<< HEAD:users/views.py
=======
import profile
from typing import Dict
>>>>>>> 97cc22d69a9a9da4268c8f13cc4ea4f5384c054f:smartassess/users/views.py
import json
from django.http.response import HttpResponse
from assessment.models import Exam
from assessment.queries import fetch_exam_by_userid
from assessment.models import Question
from .serializers import RegisterSerializers
from .models import Register
from users.token_generator import get_access_token, get_refresh_token
from django.shortcuts import render
from django.http import HttpResponseRedirect

# user view or delete.
from django.shortcuts import render, redirect
from .forms import RegisterForm, LogInForm, profileForm
from rest_framework import exceptions
from django.urls import reverse
import jwt
from rest_framework import exceptions
from django.conf import settings
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives
from django.contrib.staticfiles.storage import staticfiles_storage
# from
<<<<<<< HEAD:users/views.py
=======
from .cloudinary import upload_image

>>>>>>> 97cc22d69a9a9da4268c8f13cc4ea4f5384c054f:smartassess/users/views.py
############################################################


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = {
                "first_name": form.cleaned_data["first_name"],
                "last_name": form.cleaned_data["last_name"],
                "user_name": form.cleaned_data["user_name"],
                "email": form.cleaned_data["emailid"],
                "password": form.cleaned_data["user_password"],
            }
            if Register.objects.filter(email__iexact=data["email"]).exists() == False:
                serialized = RegisterSerializers(data=data)
                if serialized.is_valid():
                    serialized.save()
                else:
                    raise exceptions.ValidationError(serialized.error_messages())
                return HttpResponseRedirect(reverse("homePage"))
            else:
                return HttpResponse("User already exist with same email.")
    else:
        form = RegisterForm()
    return render(request, "Signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            email_id = form.cleaned_data["emailid"]
            data = {
                "email": form.cleaned_data["emailid"],
                "password": form.cleaned_data["user_password"],
            }
            user_data = Register.objects.get(email__exact=data.get("email"))
            if user_data.check_password(data.get("password")) == True:
                dir_path = "./staticfiles/data/"+email_id
                try:
                    os.mkdir(dir_path)
                    file_url = dir_path+"/questions.json"
                    uneval_exam = Exam.objects.filter(created_by__email=email_id,is_evaluated=False).values()
                    qna_list = []
                    for exam in uneval_exam:
                        exam_id = exam.get("id")
                        qna = Question.objects.filter(exam_id=exam_id).values()
                        for q in qna:
                            qna_obj = {
                                q.get("question"):q.get("standard_ans")
                            }
                            qna_list.append(qna_obj)

                        new_obj = {
                                email_id: {
                                    "exam_name": exam.get("exam_name"),
                                    "topic": exam.get("course"),
                                    "exam_details": exam.get("description"),
                                    "marks": exam.get("marks"),
                                    "qna": qna_list,
                                }
                            }
                    qfile = open(file_url, 'w')
                    qfile.write(json.dumps(new_obj,indent=4))
                    qfile.close()
                    
                except:
                    pass
                if user_data.user_role == "t":
                    response = HttpResponseRedirect(reverse("teacher_dashboard"))
                if user_data.user_role == "s":
                    response = HttpResponseRedirect(reverse("student_dashboard"))

                data = {"last_login": datetime.datetime.now(datetime.timezone.utc)}
                for key, val in data.items():
                    setattr(user_data, key, val)
                user_data.save()
                access_token = get_access_token(user_data)
                refresh_token = get_refresh_token(user_data)
                response.set_cookie(
                    key="refreshtoken", value=refresh_token, httponly=True
                )
                response.set_cookie(
                    key="accesstoken", value=access_token, httponly=True
                )
                response.data = {"token": access_token, "username": user_data.user_name}
                return response
            else:
                pass
        else:
            pass
    else:
        form = LogInForm()
    return render(request, "Login.html", {"form": form})


def custom_log_out(request):
    user = get_user(request)
    access_token = request.COOKIES.get("accesstoken")
    refresh_token = request.COOKIES.get("refreshtoken")
    response = HttpResponseRedirect(reverse("homePage"))
    if (access_token is not None) and (refresh_token is not None):
        response.delete_cookie("accesstoken")
        response.delete_cookie("refreshtoken")
        p = "./staticfiles/data/"+user.email
        ls = os.listdir(p)
        for i in ls:
            os.unlink(p+"/"+i)
        os.rmdir(p)
        return response
    else:
        return response


def is_authenticated_user(request):
    access_token = request.COOKIES.get("accesstoken")
    if access_token is not None:
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            email = payload["email"]
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
            raise exceptions.AuthenticationFailed("invalid email id")
    else:
        return False


def homeView(request):
    if request.method == "GET":
        is_auth = is_authenticated_user(request)
        if is_auth:
            access = request.COOKIES.get("accesstoken")
            decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
            email_id = decoded_data.get("email")
            user = Register.objects.get(email__iexact=email_id)
            context = {
                "is_authenticated": is_authenticated_user(request), 
                "user_name": user.user_name,
                "user_role": user.user_role,
                "profile_pic_url": user.profile_pic_url,
            }
        else:
            context = {
                "is_authenticated": is_auth,
                "user_name": ""
            }

        return render(request, "Home.html", context)


def userProfileView(request):
    try:
        payload_data = jwt.decode(
            request.COOKIES.get("accesstoken"), settings.SECRET_KEY, algorithms="HS256"
        )
        email = payload_data.get("email")
        try:
            user = Register.objects.get(email__iexact=email)
            current_year = datetime.datetime.now().year
            user_db = str(user.date_of_birth)
            user_db = str(user.date_of_birth)
            age = user_db
            context = {
                "is_authenticated": is_authenticated_user(request),
                "user": user,
                "age": age,
            }

            return render(request, "Userprofile.html", context)
        except Register.DoesNotExist as err:
            raise exceptions.AuthenticationFailed("Invalid email id.")
    except jwt.exceptions.DecodeError:
        msg = {"msg": "Are you logged in ?"}
        return render(request, "Error.html", msg)
    except jwt.ExpiredSignatureError or jwt.DecodeError:
        return custom_log_out(request)


def upDateProfile(request):
    access = request.COOKIES.get("accesstoken")
    decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
    email_id = decoded_data.get("email")
    user = Register.objects.get(email__iexact=email_id)
    if request.method == "POST":
        form = profileForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                "user_name": form.cleaned_data.get("user_name"),
                "first_name": form.cleaned_data.get("first_name"),
                "last_name": form.cleaned_data.get("last_name"),
                "interests": form.cleaned_data.get("interests"),
                "bio": form.cleaned_data.get("bio"),
                "date_of_birth": form.cleaned_data.get("date_of_birth"),
                "ph_no": form.cleaned_data.get("ph_no"),
            }
            try:
                user_data = Register.objects.get(email=email_id)
                for key, val in data.items():
                    setattr(user_data, key, val)
                user_data.save()
            except Register.DoesNotExist:
                user_data = Register(**data)
                user_data.save()

            if request.FILES:
                profile_pic=request.FILES['profile_pic'] 
                print(profile_pic)
                profile_pic_url=upload_image(profile_pic).get("secure_url")
                Register.objects.filter(email__iexact=user.email).update(profile_pic_url=profile_pic_url)
            return redirect("profile")

    form = profileForm()
    context = {
        "is_authenticated": is_authenticated_user(request),
        "user": user,
        "form": form,
        "user_name": user.user_name,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "interests": user.interests,
        "bio": user.bio,
        "date_of_birth": user.date_of_birth,
        "ph_no": user.ph_no,
        "profile_pic_url": user.profile_pic_url,
    }
    # print(context)
    return render(request, "updateprofile.html", context)


@csrf_exempt
def contactForm(request):
    if request.method == "POST":
        name = request.POST.get("firstName") + request.POST.get("lastName")
        email = request.POST.get("email")
        message = request.POST.get("message")

        subject, from_email, to = (
            "contact",
            "kedernath.mallick.tint022@gmail.com",
            "kedernath.mallick.tint022@gmail.com",
        )
        text_context = f"{name}wants to contact with you"
        html_content = (
            "<p><strong>EMAIL:</strong>" + email + "</p><br><h4>MESSAGE:</h4>" + message
        )
        msg = EmailMultiAlternatives(subject, text_context, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    return HttpResponse({"msg": "success"})


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
    access_token = request.COOKIES.get("accesstoken")
    if access_token is not None:
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            email = payload["email"]
            user = Register.objects.get(email=email)
            if user is not None:
                return user.user_role

        except jwt.ExpiredSignatureError as ex:
            custom_log_out(request)
        except jwt.DecodeError:
            return False
        except Register.DoesNotExist as ne:
            raise exceptions.AuthenticationFailed("Invalid email id")
    else:
        return False

def get_user(request):
    access_token = request.COOKIES.get("accesstoken")
    if access_token is not None:
        try:
            payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms="HS256")
            email = payload["email"]
            user = Register.objects.get(email=email)
            if user is not None:
                return user

        except jwt.ExpiredSignatureError as ex:
            custom_log_out(request)
        except jwt.DecodeError:
            return None
        except Register.DoesNotExist as ne:
            raise exceptions.AuthenticationFailed("Invalid email id")
    else:
        return None

def teacher_dashboard(request):
    access = request.COOKIES.get("accesstoken")
    decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
    email_id = decoded_data.get("email")
    user = Register.objects.get(email__iexact=email_id)
    exam_data = fetch_exam_by_userid(email_id)
    file_url = staticfiles_storage.path('data/'+email_id+'/questions.json')
        
    try:
        with open(file_url, 'r') as file:
            exam_name = json.load(file).get(email_id).get("exam_name")

        for exam in exam_data:
            if exam["exam_name"] == exam_name:
                exam["editable"] = True
            else:
                exam["editable"] = False

    except:
        pass

    context = {
            "is_authenticated": is_authenticated_user(request), 
            "user_name": user.user_name,
            "user_id": user.email,
            "profile_pic_url": user.profile_pic_url,
            "exam": exam_data
        }

    if get_user_type(request) == "t":
        return render(request, "TeacherDashboard.html", context)
    else:
        return render(request, "Error.html", context)


def student_dashboard(request): 
    access = request.COOKIES.get("accesstoken")
    decoded_data = jwt.decode(access, settings.SECRET_KEY, algorithms="HS256")
    email_id = decoded_data.get("email")
    user = Register.objects.get(email__iexact=email_id)
    exam_data=Exam.objects.filter().all().values() 
    exam_data=list(exam_data)
    try:
        file_url = staticfiles_storage.path('data/'+email_id+'/exam_details.json')
        json_data=open(file_url,mode='w',encoding='utf-8')
        for exam in exam_data:
            time={
                "hour":exam["duration"].hour,
                "minute":exam["duration"].minute
            } 
            exam["duration"]=time
            exam["created_at"]="" 
        exams={"exam":exam_data}
        json_obj=json.dumps(exams,indent=4)
        json_data.write(json_obj)
    except FileNotFoundError:
        pass
    context = {
        "is_authenticated": is_authenticated_user(request), 
        "user_name": user.user_name,
        "profile_pic_url": user.profile_pic_url,
        "exam_data": exam_data
        }
    if get_user_type(request) == "s":
        return render(request, "StudentDashboard.html", context)
    else:
        return render(request, "Error.html", context)
