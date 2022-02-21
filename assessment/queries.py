from click import FileError 
from django.http import JsonResponse
import json
from .models import *
from users.models import *
import datetime
from django.core.exceptions import ObjectDoesNotExist
import os 


question="What is OS?"
standard_answer="An operating system (OS) is system software that manages computer hardware, software resources, and provides common services for computer programs."
student_answer="An Operating System (OS) is an interface between a computer user and computer hardware."
 
 

# create an exam
def create_exam(exam_name,marks,duration,created_by,course_name='default',description=None):
    
    # fetch course if course is not available create it
    course_obj,course_created=Course.objects.get_or_create(
        code=course_name,
        course_name=course_name,
        course_details="NULL"
    )

    exam_obj,exam_created=Exam.objects.get_or_create(exam_name=exam_name,marks=marks,course=course_name,description=description,duration=duration)
    if exam_created is True:
        exam_obj.save()
        exam_obj.created_by.add(created_by)

    # return exam_id
    return exam_obj.id,exam_created

# create question answer set and link to exam accordingly
# if exam does not exist raise an exception
def set_questions(question,exam_id,standard_answer,marks,created_by):
    try:
        exam_obj=Exam.objects.get(id=exam_id)
        if exam_obj is not None:

            # updation in question in question model
            # update_data={
            #     "question":question,
            #     "standard_ans":standard_answer
            # }
            # try:
            #     obj = Question.objects.get(
            #         exam_id=exam_id,
            #         question=question,
            #         standard_ans=standard_answer
            #     )
            #     for key, value in update_data.items():
            #         setattr(obj, key, value)
            #     obj.save()
            # except Question.DoesNotExist:
            #     new_values = {'first_name': 'John', 'last_name': 'Lennon'}
            #     new_values.update(defaults)
            #     obj = Person(**new_values)
            #     obj.save()

            # creation of questions in model
            question_obj,question_created=Question.objects.get_or_create(
                exam_id=exam_id,
                question=question,
                standard_ans=standard_answer,
                qstn_marks=marks
            )
            if question_created is True:
                question_obj.save()
                question_obj.created_by.add(created_by)

            return question_obj.id,question_created
    except ObjectDoesNotExist:
        return None,False

# set the student answer
def set_student_answer(exam_id,question_id,answer,answer_duration,answered_by):
    try:
        exam_obj=Exam.objects.get(id=exam_id)
        question_obj=Question.objects.get(id=question_id)

        # for updation 
        affected_rows=Answer.objects.filter(
            exam_id=exam_id,
            question_id=question_id,
            answered_by__email=answered_by.email
        ).update(
            answer=answer,
            answer_duration=answer_duration 
        )
        if affected_rows>=1:
            return affected_rows,True
        # for fresh creation
        if exam_obj is not None and question_obj is not None and affected_rows!=1: 
            answer_object,answer_created=Answer.objects.get_or_create(
                exam_id=exam_id,
                question_id=question_id,
                answer=answer,
                answer_duration=answer_duration
            )
            if answer_created is True:
                answer_object.save()
                answer_object.answered_by.add(answered_by)

            # email has to be checked if the existed answer_by and new answered_by are same or not,if not same add the answer otherwise leave it.
            answered_object_email=Register.objects.get(answer__id=answer_object.id).email 
            # same to same answer can be given for exact same exam and exact same question and exact same duration
            if answer_created is False and answer==answer_object.answer and answered_object_email!=answered_by.email: 
                answer_object.answered_by.add(answered_by)
                answer_created=True
            
            return answer_object.id,answer_created
        else:
            return affected_rows,True
        
    except ObjectDoesNotExist:
        return None,False

# save exam from json
def save_exam_from_json(filepath):
    if os.path.exists(filepath):
        try:
            json_data=open(filepath,mode='r',encoding='utf-8')
            exam_set=json.loads(json_data.read())
            
            # exam setter obj
            exam_setter_user_name=list(exam_set.keys())[0]
            exam_stter_obj=Register.objects.get(user_name__iexact=exam_setter_user_name)
            exam_dets_json=list(exam_set.values())[0]
            exam_name=exam_dets_json.get('exam_name')
            course=exam_dets_json.get('topic')
            exam_details=exam_dets_json.get('exam_details')
            duration=datetime.time(00,30,00)

            # create exam
            exam_id,status=create_exam(exam_name=exam_name,marks=100,duration=duration,created_by=exam_stter_obj,course_name=course,description=exam_details)
 
            json_data.close()

            return exam_id,status
        except FileError:
            print("File does not exist")
            return None,False

# save final question answer dataset
def save_exam_qna(user_id, filepath, exam_id):
    if os.path.exists(filepath):
        try:
            json_data=open(filepath,mode='r',encoding='utf-8')
            exam_set=json.loads(json_data.read())
            
            # exam setter obj
            exam_stter_obj=Register.objects.get(email__iexact=user_id)
            exam_dets_json=exam_set.get(user_id)
            exam_obj=Exam.objects.get(id=exam_id)
            try:
                marks = exam_dets_json.get("marks")
                exam_obj.marks = marks
                exam_obj.save()
                question_answer_pairs = exam_dets_json.get("qna")
                for items in question_answer_pairs:
                    qn = items.get("question")
                    ans = items.get("answer")
                    q_marks = items.get("marks")
                    set_questions(question=qn,exam_id=exam_id,standard_answer=ans,marks =q_marks,created_by=exam_stter_obj)

                json_data.close()
                return True
            except:
                return False

        except:
            return False

# fetch all details against any exam from db
def fetch_exam_details_by_id(exam_id=None):
    exam_obj=Exam.objects.filter(id=exam_id).values() 
    question_answer_pairs=[]
    
    question_all_pairs_obj=Question.objects.filter(exam_id=exam_id).values() 
    for item in list(question_all_pairs_obj): 
        question_answer_pairs.append(item)

    return list(exam_obj)[0],question_answer_pairs

# fetch all details against any exam from db
def fetch_exam_details_by_name(exam_name=None):
    exam_obj=Exam.objects.filter(exam_name=exam_name).values()
    return list(exam_obj)[0]

def fetch_exam_by_userid(user_id):
    exam_obj=Exam.objects.filter(created_by__email=user_id).values()
    return list(exam_obj)

def add_submition(exam_id, std_email_id):
    try:
        obj = ExamSubmissionDetail.objects.get(exam_id=exam_id, student_id=std_email_id)
        obj.is_submitted=True
        obj.save()
    except:
        submission = ExamSubmissionDetail(
            exam_id=exam_id,
            student_id=std_email_id,
            is_submitted=True
        )
        submission.save()

def is_exam_submitted(exam_id, std_email_id):
    try:
        ExamSubmissionDetail.objects.get(exam_id=exam_id, student_id=std_email_id, is_submitted=True)
        return True
    except:
        return False

def test(request):
    if request.method=="GET":
        # # exam of 30 minutes
        # exam_dur = datetime.time(00, 30, 00)
        # id,status=create_exam("Test1",100,duration=exam_dur,created_by=Register.objects.get(email__iexact="root@gmail.com"),course_name="OOPS",description="Test course")


        # q_id,q_status=set_questions(question="What is OS?",exam_id=12,standard_answer="An operating system is system software that manages computer hardware, software resources, and provides common services for computer programs.",created_by=Register.objects.get(email__iexact="root@gmail.com"))


        answer_duration=datetime.time(00,3,00)
        set_student_answer(exam_id=2,question_id=2,answer="CD is not",answer_duration=answer_duration,answered_by=Register.objects.get(email__iexact="admin@gmail.com"))

        # res,resp=save_exam_qna("./staticfiles/data/questions.json",3)

        res,resp=fetch_exam_details_by_id(exam_id=3)
        return JsonResponse({"st":res,"create_status":resp})
