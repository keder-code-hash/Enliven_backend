import os
import json
import requests
from math import ceil
import subprocess as sp
import base64
from time import time
from PIL import Image, ImageFile
import io
# from datauri import DataURI

# importing Django modules
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from assessment.face_rec_script import faceRec
from users.models import Register
from users.views import is_authenticated_user, get_user, get_user_type
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist

# Custom module imports
from assessment.models import Answer, Exam, Question
from assessment.queries import fetch_exam_details_by_id, submit_manual_check
from assessment.model_prediction import make_prediction


def assessment_json_gen(exam_id, email_id, user_id):
    try:
        exam_dets = Exam.objects.filter(id=exam_id).values()
        data = Question.objects.filter(exam_id=exam_id).values()
        all_questions = list(data)
        try:
            score = 0.0
            file_url = staticfiles_storage.path(
                "data/" + user_id + "/assessment_details.json"
            )
            json_data = open(file_url, mode="w", encoding="utf-8")
            for question in all_questions:
                student_answer=Answer.objects.get(exam_id=exam_id,question_id=question["id"],answered_by__email=email_id) 
                question['student_answer'] = student_answer.answer
                question['eval_details'] = student_answer.eval_details
                question['percentage'] = student_answer.match_percentage
                question['status'] = student_answer.remarks
                question['marks'] = student_answer.marks
                question['std_email'] = email_id
                score += student_answer.marks
                question.pop("created_at")
            exam_dets = list(exam_dets)[0]
            time = {
                "hour": exam_dets["duration"].hour,
                "minute": exam_dets["duration"].minute,
            }
            exam_dets["duration"] = time
            exam_dets["score"] = ceil(score)
            exam_dets.pop("created_at")
            assessment_set = {"exam": exam_dets, "ass_set": all_questions}
            json_obj = json.dumps(assessment_set, indent=4)
            json_data.write(json_obj)
            if len(all_questions) > 0:
                return {"st": 1}
            else:
                return {"st": 0}
        except ObjectDoesNotExist:
            return {"st": 0}
    except FileNotFoundError:
        return {"st": 0}


# for student
@csrf_exempt
def load_assessment_result(request):
    if request.method == "POST":
        user = get_user(request=request)
        email_id = user.email
        exam_id = request.POST.get("exam_id")
        res = assessment_json_gen(exam_id, email_id, email_id)
        return JsonResponse(res)


# for teacher
@csrf_exempt
def load_assessment_result_teacher(request):
    user = get_user(request)
    if user.user_role == 't':
        if request.method=="POST":
            exam_id = request.POST.get("exam_id")
            email = request.POST.get("email")
            question_id = request.POST.get("q_id")
            marks = request.POST.get("updatedMarks")
            ansStatus = request.POST.get("ansStatus")
            submit_manual_check(email,exam_id,question_id,marks,ansStatus)

        elif request.method=="GET":
            exam_id = request.GET.get("exam_id")
            email = request.GET.get("email")  

        assessment_json_gen(exam_id, email, user.email)
        try:
            file_url = staticfiles_storage.path(
                "data/" + user.email + "/assessment_details.json"
            )
            json_data = open(file_url, mode="r", encoding="utf-8")
            data = json.loads(json_data.read())
            exam_details = data.get("exam")
            actual_ans = data.get("ass_set")
        except:
            pass
        context = {
            "user": user,
            "exam": exam_details,
            "score": exam_details.get("score"),
            "actual_ans": actual_ans,
            "question_no": len(actual_ans),
            "is_authenticated": is_authenticated_user(request),
        }

        return render(request, "StudentResult.html", context)

    else:
        err_log = {"msg": "Invaild Request!"}
        return render(request, "Error.html", err_log)


# test results
def test_results(request):
    user = get_user(request)
    try:
        file_url = staticfiles_storage.path(
            "data/" + user.email + "/assessment_details.json"
        )
        json_data = open(file_url, mode="r", encoding="utf-8")
        data = json.loads(json_data.read())
        exam_details = data.get("exam")
        actual_ans = data.get("ass_set")
    except:
        pass

    context = {
        "user": user,
        "exam": exam_details,
        "score": exam_details.get("score"),
        "actual_ans": actual_ans,
        "question_no": len(actual_ans),
        "is_authenticated": is_authenticated_user(request),
    }

    return render(request, "StudentResult.html", context)


@csrf_exempt
def fetch_stnd_QnA(request):
    if request.method == "POST":
        id = request.POST.get("set_id")
        user = get_user(request)
        try:
            file_url = staticfiles_storage.path(
                "data/" + user.email + "/assessment_details.json"
            )
            json_data = open(file_url, mode="r", encoding="utf-8")
            data = json.loads(json_data.read())
            actual_ans = data.get("ass_set")
            for qna in actual_ans:
                if qna.get("id") == int(id):
                    actual_ans = qna
                    break
            json_data.close()
            # print(actual_ans.get("eval_details"))
            eval_details = actual_ans.get("eval_details").replace("'", '"')
            eval_details = json.loads(eval_details)
            context = {
                "actual_ans": actual_ans,
                "contradiction": eval_details.get("contradiction"),
                "entailment": eval_details.get("entailment"),
                "neutral": eval_details.get("neutral")
            }
            return JsonResponse(context)
        except:
            pass
        return JsonResponse({})


# view results of all students (accessible by teacher only)
def view_all_results(request):
    user = get_user(request)
    exam_id = int(request.GET.get("exam_id"))
    exam_obj = Exam.objects.get(id=exam_id)
    obj = Answer.objects.values_list("answered_by").filter(exam_id=exam_id)
    stn_set = set(obj)
    result = []
    for stn in stn_set:
        email = stn[0]
        user_name = Register.objects.values_list("first_name", "last_name").filter(
            email=email
        )
        data = {"name": (user_name[0][0] + " " + user_name[0][1]), "email": email}
        result.append(data)

    subject = "OOP"
    context = {
        "user": user,
        "exam_id": exam_id,
        "exam_name": exam_obj.exam_name,
        "course": exam_obj.course,
        "marks": exam_obj.marks,
        "details": result,
        "subject": subject,
        "is_authenticated": is_authenticated_user(request),
    }

    return render(request, "TeacherResult.html", context)


@csrf_exempt
def save_assessment_answer(request):
    if request.method == "POST":
        exam_id = request.POST.get("exam_id")
        email_id = get_user(request).email
        exam, question_list = fetch_exam_details_by_id(exam_id)
        question_list = list(question_list)
        try:
            file_url = staticfiles_storage.path(
                "data/" + email_id + "/all_questions.json"
            )
            json_data = open(file_url, mode="w", encoding="utf-8")
            for q in question_list:
                q["student_answer"] = ""
                t = {"minute": "", "second": ""}
                q["time_taken"] = t
                q.pop("created_at")
                q.pop("standard_ans")

            new_obj = {
                "exam_id": exam.get("id"),
                "exam_name": exam.get("exam_name"),
                "topic": exam.get("course"),
                "exam_details": exam.get("description"),
                "marks": exam.get("marks"),
                "duration": {
                    "hour": exam.get("duration").hour,
                    "minute": exam.get("duration").minute,
                },
                "questions": question_list,
            }

            json_obj = json.dumps(new_obj, indent=4)
            json_data.write(json_obj)

            return JsonResponse({"st": 1})
        except FileNotFoundError:
            return JsonResponse({"st": 0})


# self assessment
@csrf_exempt
def assessment(request):
    user = get_user(request)
    email_id = user.email
    try:
        file_url = staticfiles_storage.path("data/" + email_id + "/all_questions.json")
        json_data = open(file_url, mode="r", encoding="utf-8")
        main_data = json.loads(json_data.read())
        question_list = main_data.get("questions")

        exam_dets = {
            "exam_name": main_data.get("exam_name"),
            "topic": main_data.get("topic"),
            "exam_details": main_data.get("exam_details"),
            "marks": main_data.get("marks"),
            "duration": {
                "hour": main_data.get("duration").get("hour"),
                "minute": main_data.get("duration").get("minute"),
            },
        }
        
        json_data.close() 
    except FileNotFoundError:
        pass

    context = {
        "user": user,
        "is_authenticated": is_authenticated_user(request),
        "qno": question_list,
        "max_no": len(question_list),
        "exam": exam_dets
        # "data":
    }
    return render(request, "AttemptExam.html", context)


# set questions for examination (accessible by teacher only)
def set_questions(request):
    user = get_user(request)
    file_url = staticfiles_storage.path("data/" + user.email + "/questions.json")
    data = ""
    with open(file_url, "r+") as file:
        data = json.load(file).get(user.email)

    qno = list(range(1, len(data.get("qna")) + 2))
    max_qno = len(qno)
    if qno == []:
        qno = [1]
        max_qno = 1
    context = {
        "is_authenticated": is_authenticated_user(request),
        "user": user,
        "data": data,
        "qno": qno,
        "max_qno": max_qno,
    }
    if context["is_authenticated"] and user.user_role == "t":
        return render(request, "Examset.html", context)
    else:
        err_log = {"msg": "Are you logged in?"}
        return render(request, "Error.html", err_log)


def view_results(request):
    return HttpResponse("View Results (accessible by Teacher)")


@csrf_exempt
def eval_exam(request):
    if request.method == "GET":
        if get_user_type(request) == "t":
            exam_id = int(request.GET.get("exam_id"))
            exam_obj = Exam.objects.get(id=exam_id)
            exam_obj.is_evaluated = True
            exam_obj.save()
            qna_list = fetch_exam_details_by_id(exam_id)[1]
            for qna in qna_list:
                q_id = qna.get("id")
                std_ans = qna.get("standard_ans")
                qn_marks = qna.get("qstn_marks")
                ans_list = Answer.objects.filter(
                    exam_id=exam_id, question_id=q_id
                ).values()
                for ans in ans_list:
                    a_id = ans.get("id")
                    stn_ans = ans.get("answer")
                    try:
                        sts, remarks, percentage, full_respond = make_prediction(
                            stn_ans, std_ans, 0
                        )
                        
                        ans_obj = Answer.objects.get(id=a_id)
                        ans_obj.remarks = remarks
                        ans_obj.marks = (percentage / 100) * qn_marks
                        ans_obj.match_percentage = percentage
                        ans_obj.eval_details = full_respond
                        ans_obj.save()
                    except:
                        pass

            return HttpResponse(1)

        else:
            return HttpResponse(0)

    else:
        return HttpResponse(0)

def save_image(data_uri, stored_path):
    # with open("tmp.data", "w") as f:
    #     f.write(data_uri)

    # preprocessing
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    data_uri = data_uri[1:-1]
    length = len(data_uri) - len("data:image/png;base64,")
    data_uri += "=" * (length % 4)

    print("Length:", length)

    im = Image.open(io.BytesIO(base64.b64decode(str(data_uri).split(",")[1])))
    im.save(stored_path, "png")


face_api_url = "https://face-detect-arghyasahoo.cloud.okteto.net"

@csrf_exempt
def checkImage(request):
    if request.method == "POST":
        try:
            user_obj = get_user(request)
            userid = user_obj.email
            imageData = request.POST.get("currImg")
            # * save image
            original_img_path = staticfiles_storage.path("data/"+ userid+ "/"+ f"original_{userid.replace('.com', '')}"+ ".png"
            )
            save_image(imageData, original_img_path)
            img_file = open(original_img_path, 'rb')
            files = {'file': img_file}
            getdata = requests.post(face_api_url+'/detect', files=files)
            img_file.close()
            if getdata.json().get("success") == "OK":
                return HttpResponse(1)
            else:
                return HttpResponse(0)
        except:
            return HttpResponse(2)

@csrf_exempt
def observeCam(request):
    if request.method == "POST":
        user_obj = get_user(request)
        userid = user_obj.email

        imageData = request.POST.get("observeImg")
        # * save image
        curr_img_path = staticfiles_storage.path(
            "data/" + userid + "/" + str(int(time())) + ".png"
        )
        save_image(imageData, curr_img_path)
        img_file = open(curr_img_path, 'rb')
        files = {'file': img_file}
        detection = requests.post(face_api_url+'/detect', files=files)
        if str(list(detection.json().keys())[0]) == "success":
            orig_img_path = staticfiles_storage.path("data/"+ userid+ "/"+ f"original_{userid.replace('.com', '')}"+ ".png")
            rec = faceRec(orig_img_path, curr_img_path) 
            if(rec.get("status")):
                return HttpResponse(1)
            else:
                return HttpResponse(3)
        else:
            if detection.json().get("error") == "MFD":
                return HttpResponse(2)
            elif detection.json().get("error") == "EXPT":
                return HttpResponse(0)
