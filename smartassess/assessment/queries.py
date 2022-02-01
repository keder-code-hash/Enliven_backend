from django.http import JsonResponse
from assessment.models import *
from users.models import *

# create standard Question Answer Set from teacher
def create_standardQnaSet(question,standard_ans):
    question_obj=Question(question=question,marks=2,level="H")
    question_obj.save()

    answer_setter=Register.objects.get(email__iexact="root@gmail.com")
    standard_ans_obj=Answer(answer=standard_ans)
    standard_ans_obj.save()
    standard_ans_obj.std_id.add(answer_setter)

    standard_QnA_set=StandardQnA()
    standard_QnA_set.save()
    standard_QnA_set.question.add(question_obj)
    standard_QnA_set.std_ans.add(standard_ans_obj)

# create question answer set for student answer 
def create_student_answer(question,student_answer):
    question_obj=Question.objects.get(question__iexact=question)

    answer_setter=Register.objects.get(email__iexact="admin@gmail.com")
    student_ans_obj=Answer(answer=student_answer)
    student_ans_obj.save()
    student_ans_obj.std_id.add(answer_setter)

    QnAObject=QnA()
    QnAObject.save()
    QnAObject.question.add(question_obj)
    QnAObject.student_ans.add(student_ans_obj) 

#create an exam with detailed info
def create_exam(exam_name,course_name,standard_question_ans_set,duration,total_questions,full_marks,detailed_information=None):
    # check the course is exist or not
    course_obj=Course.objects.get(course_name__ieexact=course_name)
    if course_obj is None:
        course_object=Course(course_name=course_name,code="default",course_details={}) 
        course_object.save()

    

question="What is OS?"
standard_answer="An operating system (OS) is system software that manages computer hardware, software resources, and provides common services for computer programs."
student_answer="An Operating System (OS) is an interface between a computer user and computer hardware."


def test(request):
    if request.method=="GET":
        # create_standardQnaSet(question=question,standard_ans=standard_answer)
        create_student_answer(question=question,student_answer=student_answer)
        return JsonResponse({"st":"Success"})
    