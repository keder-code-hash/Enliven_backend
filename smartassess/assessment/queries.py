from multiprocessing.connection import answer_challenge
from django.http import JsonResponse
from .models import *
from users.models import *
import datetime
from django.core.exceptions import ObjectDoesNotExist

question="What is OS?"
standard_answer="An operating system (OS) is system software that manages computer hardware, software resources, and provides common services for computer programs."
student_answer="An Operating System (OS) is an interface between a computer user and computer hardware."
 
    
details = [
        {
            "q_no": 1,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 2,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 3,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        },
        {
            "q_no": 4,
            "qsn": "What is Inheritance",
            "stn_ans": "Inheritance in Java is a mechanism in which one object acquires all the properties and behaviors of a parent object. It is an important part of OOPs (Object Oriented programming system).",
            "std_ans": "Inheritance can be defined as the process where one class acquires the properties (methods and fields) of another.",
        }
    ]

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
def set_questions(question,exam_id,standard_answer,created_by):
    try:
        exam_obj=Exam.objects.get(id=exam_id)
        if exam_obj is not None:

            question_obj,question_created=Question.objects.get_or_create(
                exam_id=exam_id,
                question=question,
                standard_ans=standard_answer
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

        if exam_obj is not None and question_obj is not None:
            answer_object,answer_created=Answer.objects.get_or_create(
                exam_id=exam_id,
                question_id=question_id,
                answer=answer,
                answer_duration=answer_duration
            )
            if answer_created is True:
                answer_object.save()
                answer_object.answered_by.add(answered_by)

            # same to same answer can be given for exact same exam and exact same question and exact same duration
            if answer_created is False and answer==answer_object.answer: 
                answer_object.answered_by.add(answered_by)
                answer_created=True
            
            return answer_object.id,answer_created
    except ObjectDoesNotExist:
        return None,False


def test(request):
    if request.method=="GET":
        # exam of 30 minutes
        exam_dur = datetime.time(00, 30, 00)
        id,status=create_exam("Test1",100,duration=exam_dur,created_by=Register.objects.get(email__iexact="root@gmail.com"),course_name="OOPS",description="Test course")


        q_id,q_status=set_questions(question="What is OS?",exam_id=12,standard_answer="An operating system is system software that manages computer hardware, software resources, and provides common services for computer programs.",created_by=Register.objects.get(email__iexact="root@gmail.com"))


        answer_duration=datetime.time(00,3,00)
        a_id,a_status=set_student_answer(exam_id=2,question_id=1,answer="OS is a system which manages all peripheral devices,and software resources and provides a common GUI for all computer tasks.",answer_duration=answer_duration,answered_by=Register.objects.get(email__iexact="admin@gmail.com"))

        return JsonResponse({"st":a_id,"create_status":a_status})
