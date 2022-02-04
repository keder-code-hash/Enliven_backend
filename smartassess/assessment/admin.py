from django.contrib import admin
from assessment.models import *

# Register your models here.
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Evaluation)
admin.site.register(Monitor)