from django.contrib import admin

# Register your models here.

from courseQuery.models import User, Task


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('user', 'courseCode')
