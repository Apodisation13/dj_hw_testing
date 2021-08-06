# import pytest
# from django.urls import reverse
# from rest_framework.status import \
#     HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
#
# from students.models import Course
#
#
# @pytest.mark.django_db
# class TestCourse:
#     def setup(self):
#         # self.course = Course.objects.create(name='Test Course X')
#         self.url = reverse('courses-list')
#
#     def test_course(self):
#         assert self.course.id
#         assert self.course.name == "Test Course X"
#
#     @pytest.mark.parametrize(
#         ['name', 'expected_status'],
#         (
#             ('X Course', HTTP_201_CREATED),
#             ('A Course', HTTP_201_CREATED),
#             ('TT FF', HTTP_201_CREATED)
#         )
#     )
#     def test_create_ok_1(self, api_client, name, expected_status):
#         """3 tests"""
#         post_data = {'name': name}
#         response = api_client.post(self.url, post_data)
#         assert expected_status == response.status_code
#         assert name == response.data.get('name')
#         r = api_client.get(self.url, data={'search': 'Course'})
#         assert r.status_code == 200
#         assert len(r.data) == 2
#
#     def test_create_not_ok_1(self, api_client):
#         """wrong data - title doesnt correspond DB"""
#         post_data = {'title': 'that is not possible!'}
#         response = api_client.post(self.url, post_data)
#         assert HTTP_400_BAD_REQUEST == response.status_code
#
#     def test_delete_course_ok_1(self, api_client):
#         course = Course.objects.filter(pk=self.course.pk).first()
#         assert self.course.pk == course.pk  # здесь инстанс ещё есть
#         url = reverse('courses-detail', kwargs={'pk': self.course.pk})
#         delete = api_client.delete(url)
#         assert HTTP_204_NO_CONTENT == delete.status_code
#         course = Course.objects.filter(pk=self.course.pk).first()
#         assert course is None  # а здесь инстанса уже нет
#
#     def test_delete_course_not_ok_1(self, api_client):
#         course = Course.objects.filter(pk=self.course.pk).first()
#         assert self.course.pk == course.pk  # здесь инстанс ещё есть
#         random_pk = 200  # пусть такого ключа заведомо нет
#         url = reverse('courses-detail', kwargs={'pk': random_pk})
#         delete = api_client.delete(url)
#         assert HTTP_404_NOT_FOUND == delete.status_code  # нельзя удалить то чего нет
#         course = Course.objects.filter(pk=self.course.pk).first()
#         assert course is not None  # проверим что курс ещё есть
#
#     def test_patch(self, api_client, course_factory):
#         course_factory(_quantity=5)
#
