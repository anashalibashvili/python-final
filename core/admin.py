from django.contrib import admin
from core.models import Question, Answer, Vote, Tag

# Register your models here.
admin.site.register([Question, Answer, Vote, Tag])
