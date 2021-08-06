from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from students.models import *
from django.conf import settings


class StudentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):

    students = StudentSerializer

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    # def create(self, validated_data):
    #     raise ValidationError('Просто нельзя и всё')

    @staticmethod
    def validate_students(students: list):
        if len(students) > settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f'Нельзя добавить на курс больше {settings.MAX_STUDENTS_PER_COURSE} студентов')
        return students
