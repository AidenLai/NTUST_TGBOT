from django.db import models

# Create your models here.


class User(models.Model):
    chat_id = models.CharField(max_length=20, help_text="chat_id")


class Task(models.Model):
    courseCode = models.CharField(max_length=9, help_text="courseNum")
    user = models.ForeignKey(User, on_delete=models.PROTECT)
