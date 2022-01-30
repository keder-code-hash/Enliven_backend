from django.db import models


# Create your models here.
class Question:
    question_no = models.IntegerField(unique=True)
    question = models.CharField(max_length=100, unique=True)
    standard_ans = models.CharField(max_length=200)
    subject = models.CharField(max_length=20, unique=True)


class Answer:
    ans_id = models.IntegerField(unique=True)
    question_no = models.IntegerField(unique=True)
    answer = models.CharField(max_length=200)
    std_id = models.IntegerField(unique=True)
