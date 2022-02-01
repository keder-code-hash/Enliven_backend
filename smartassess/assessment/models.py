from django.db import models
from users.models import Course, Register


class Question(models.Model):
    # question_id = models.BigIntegerField(unique=True, primary_key=True,auto_created=True)
    question = models.CharField(max_length=100, unique=True)
    marks = models.IntegerField(blank=False)

    DIFFICULTY = (("E", "Easy"), ("M", "Medium"), ("H", "Hard"))
    level = models.CharField(max_length=20, choices=DIFFICULTY, default="E")


class Answer(models.Model):
    # ans_id = models.BigIntegerField(unique=True, primary_key=True,auto_created=True)
    answer = models.CharField(max_length=130)
    std_id = models.ManyToManyField(Register, related_name="answerd_by")
    # std_id = models.OneToOneField(Register,on_delete=models.CASCADE)



# set questions
class StandardQnA(models.Model):
    # _id = models.BigIntegerField(primary_key=True, unique=True,auto_created=True)
    question = models.ManyToManyField(Question)
    std_ans = models.ManyToManyField(Answer) 


class QnA(models.Model):
    question = models.ManyToManyField(Question )
    student_ans = models.ManyToManyField(Answer )


# take exam
class Exam(models.Model):
    # _id = models.BigIntegerField(primary_key=True, unique=True,auto_created=True)
    exam_name=models.CharField(max_length=50,blank=False)
    course = models.ManyToManyField(Course, related_name="course")
    standard_qna = models.ManyToManyField(StandardQnA)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.TimeField(blank=False)
    total_questions = models.IntegerField()
    full_marks = models.IntegerField()
    detailed_information=models.CharField(max_length=200,default='')


class Result(models.Model):
    # _id = models.BigIntegerField(primary_key=True, unique=True,auto_created=True)
    standard_qna = models.OneToOneField(StandardQnA, on_delete=models.CASCADE)
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)
    marks_obtained = models.FloatField(blank=False)


class AssessmentResult(models.Model):
    # _id = models.BigIntegerField(primary_key=True, unique=True,auto_created=True)
    exam_id = models.OneToOneField(Exam, on_delete=models.CASCADE)
    result = models.ManyToManyField(Result)
    total_marks_obtained = models.IntegerField(blank=False)
    evaluation_date = models.DateTimeField(auto_now_add=True)
