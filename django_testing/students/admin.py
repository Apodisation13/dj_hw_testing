from django.contrib import admin

from .models import *


class InLine(admin.TabularInline):
    model = Course.students.through


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    ...


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [InLine, ]
