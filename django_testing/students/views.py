from django.shortcuts import redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from students.filters import CourseFilter
from students.models import Course
from students.serializers import CourseSerializer


class CoursesViewSet(ModelViewSet):

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    search_fields = ['name', ]
    filterset_class = CourseFilter


def home(request):
    """ВОТ ЭТО api-root - как бы дефолтное name DefaultRouter, можно менять api/v1/чёугодно, api-root останется"""
    return redirect('api-root')
