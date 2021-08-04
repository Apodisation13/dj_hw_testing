import pytest
from django.urls import reverse
from rest_framework.status import \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND

from students.models import Course
from rest_framework.test import APIClient


class TestCourse:
    def setup(self):
        self.course = Course.objects.create(name='Test Course X')
        self.client = APIClient()
        self.url = reverse('courses-list')

    @pytest.mark.django_db
    def test_course(self):
        assert self.course.id
        assert self.course.name == "Test Course X"

    @pytest.mark.django_db
    def test_create_ok_1(self):
        post_data = {'name': 'Test Course XXX'}
        response = self.client.post(self.url, post_data)
        assert HTTP_201_CREATED == response.status_code
        assert 'Test Course XXX' == response.data.get('name')

    @pytest.mark.django_db
    def test_create_not_ok_1(self):
        """wrong data - title doesnt correspond DB"""
        post_data = {'title': 'that is not possible!'}
        response = self.client.post(self.url, post_data)
        assert HTTP_400_BAD_REQUEST == response.status_code

    @pytest.mark.django_db
    def test_delete_course_ok_1(self):
        course = Course.objects.filter(pk=self.course.pk).first()
        assert self.course.pk == course.pk  # здесь инстанс ещё есть
        url = reverse('courses-detail', kwargs={'pk': self.course.pk})
        delete = self.client.delete(url)
        assert HTTP_204_NO_CONTENT == delete.status_code
        course = Course.objects.filter(pk=self.course.pk).first()
        assert None == course  # а здесь инстанса уже нет

    @pytest.mark.django_db
    def test_delete_course_not_ok_1(self):
        random_pk = 200  # пусть такого ключа заведомо нет
        url = reverse('courses-detail', kwargs={'pk': random_pk})
        delete = self.client.delete(url)
        assert HTTP_404_NOT_FOUND == delete.status_code  # нельзя удалить то чего нет
