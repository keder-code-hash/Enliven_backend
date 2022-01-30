from django.db import models
from users.models import Course


class Question(models.Model):
    question_id = models.BigIntegerField(unique=True, primary_key=True)
    question = models.CharField(max_length=100, unique=True)
    marks = models.IntegerField(blank=False)

    DIFFICULTY = (("E", "Easy"), ("M", "Medium"), ("H", "Hard"))
    level = models.CharField(max_length=20, choices=DIFFICULTY, default="E")


class Answer(models.Model):
    ans_id = models.BigIntegerField(unique=True, primary_key=True)
    answer = models.CharField(max_length=130)
    std_id = models.ManyToManyField(Question, related_name="answerd_by")


# set questions
class StandardQnA(models.Model):
    _id = models.BigIntegerField(primary_key=True, unique=True)
    question = models.ManyToManyField(Question)
    std_ans = models.ManyToManyField(Answer)


class QnA(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    student_ans = models.OneToOneField(Answer, on_delete=models.CASCADE)


# take exam
class Exam(models.Model):
    _id = models.BigIntegerField(primary_key=True, unique=True)
    course = models.ManyToManyField(Course, related_name="course")
    qna = models.OneToOneField(QnA, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    duration = models.TimeField(blank=False)
    total_questions = models.IntegerField()
    full_marks = models.IntegerField()


class Result(models.Model):
    _id = models.BigIntegerField(primary_key=True, unique=True)
    standard_qna = models.OneToOneField(StandardQnA, on_delete=models.CASCADE)
    answer = models.OneToOneField(Answer, on_delete=models.CASCADE)
    marks_obtained = models.FloatField(blank=False)


class AssessmentResult(models.Model):
    _id = models.BigIntegerField(primary_key=True, unique=True)
    exam_id = models.OneToOneField(Exam, on_delete=models.CASCADE)
    result = models.ManyToManyField(Result)
    total_marks_obtained = models.IntegerField(blank=False)
    evaluation_date = models.DateTimeField(auto_now_add=True)
