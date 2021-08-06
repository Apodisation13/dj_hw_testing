import pytest
from django.urls import reverse
from rest_framework.status import \
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, \
    HTTP_404_NOT_FOUND, HTTP_200_OK, HTTP_302_FOUND
from django.test import Client
from students.models import *

TEST_FIELDS = ['name', 'expected_status']
TEST_DATA = (
    ('X Course', HTTP_201_CREATED),
    ('A Course', HTTP_201_CREATED),
    ('TT FF', HTTP_201_CREATED)
)


@pytest.mark.django_db
class TestCourseBaker:
    def setup(self):
        self.url_list = reverse('courses-list')

    def test_get_first(self, api_client, course_factory):
        """5 instances, get first"""
        quantity = 5
        course_factory(_quantity=quantity)
        course_1 = Course.objects.first()
        url = reverse('courses-detail', kwargs={'pk': course_1.pk})
        response = api_client.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data.get('name') == course_1.name

    def test_get_all(self, api_client, course_factory):
        """5 instances, get all"""
        quantity = 5
        course_factory(_quantity=quantity)
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == quantity

    def test_delete(self, api_client, course_factory):
        """5 instances, 1 to_be_deleted"""
        quantity = 5
        course_factory(_quantity=quantity)
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == quantity  # 5 courses created
        course_del = Course.objects.first()  # let's delete one, first for example
        url = reverse('courses-detail', kwargs={'pk': course_del.pk})
        response_del = api_client.delete(url)
        assert response_del.status_code == HTTP_204_NO_CONTENT
        response_after_del = api_client.get(self.url_list)
        assert len(response_after_del.data) == quantity - 1  # 5 was, 4 remained

    def test_delete_course_not_ok(self, api_client, course_factory):
        """5 created, but trying to delete non-existent PK"""
        quantity = 5
        course_factory(_quantity=quantity)
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == quantity  # 5 created
        random_pk = 10000  # assuming there's no such pk
        url = reverse('courses-detail', kwargs={'pk': random_pk})
        delete_trying = api_client.delete(url)
        assert delete_trying.status_code == HTTP_404_NOT_FOUND  # can't delete non-existent
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == quantity  # so still all 5 left after failed attempt

    def test_search_by_name(self, api_client):
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0  # no courses yet

        # manual creation for search checking, search for Python, 2 instances will be found
        Course.objects.bulk_create(
            [
                Course(name='Z'),
                Course(name='C Python'),
                Course(name='R Python')
            ]
        )

        response = api_client.get(self.url_list, data={'search': 'Python'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 2  # 2 found
        assert response.data[0].get('name') == 'C Python'  # first found name is C Python

    def test_filter_by_name(self, api_client):
        """both existed and non-existent"""
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0  # no courses yet
        # manual creation for filter checking, search for C Python, only 1 will be found
        Course.objects.bulk_create(
            [
                Course(name='Z'),
                Course(name='C Python'),
                Course(name='R Python')
            ]
        )
        response = api_client.get(self.url_list, data={'name': 'C Python'})
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0].get('name') == 'C Python'  # one found

        response = api_client.get(self.url_list, data={'name': 'Non-existent Course'})
        assert response.status_code == HTTP_200_OK  # still HTTP_200_OK, but
        assert response.data == []  # non found

    def test_filter_by_id(self, api_client):
        response = api_client.get(self.url_list)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0
        # manual creation for filter checking, search for course_3's id
        Course.objects.bulk_create(
            [
                Course(name='Z'),
                Course(name='A Baby'),
                Course(name='TRYYYYYY TO FIIIIIIIND ME')
            ]
        )
        c3_id = Course.objects.last().id
        response = api_client.get(self.url_list, data={'id': c3_id})
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0].get('name') == 'TRYYYYYY TO FIIIIIIIND ME'

    def test_filter_by_non_existent_id(self, api_client):
        random_pk = 200000  # assuming there's no such pk
        response = api_client.get(self.url_list, data={'id': random_pk})
        assert response.status_code == HTTP_400_BAD_REQUEST

    @pytest.mark.parametrize(TEST_FIELDS, TEST_DATA)
    def test_create_ok(self, api_client, name, expected_status):
        """3 tests"""
        post_data = {'name': name}
        response = api_client.post(self.url_list, post_data)
        assert response.status_code == expected_status
        assert response.data.get('name') == name

    def test_create_not_ok(self, api_client):
        """Wrong field name"""
        post_data = {'title': 'Wrong Test Data'}
        response = api_client.post(self.url_list, post_data)
        assert response.status_code == HTTP_400_BAD_REQUEST
        courses_list = Course.objects.all()
        assert len(courses_list) == 0

    def test_patch_success(self, api_client, course_factory):
        course_factory(_quantity=5)
        course_to_patch = Course.objects.last()
        new_data = {'name': 'Test Patch Succeed'}
        url = reverse('courses-detail', kwargs={'pk': course_to_patch.pk})
        response = api_client.patch(url, data=new_data)
        assert response.status_code == HTTP_200_OK
        assert Course.objects.filter(pk=course_to_patch.pk)[0].name == 'Test Patch Succeed'

    def test_patch_wrong_instance(self, api_client, course_factory):
        course_factory(_quantity=5)
        random_pk = 20000
        new_data = {'name': 'Test Patch Succeed'}
        url = reverse('courses-detail', kwargs={'pk': random_pk})
        response = api_client.patch(url, data=new_data)
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_max_students_success(self, api_client, course_factory, student_factory, settings):
        students_quantity = 2
        course_factory(_quantity=1)  # create 1 test course
        student_factory(_quantity=students_quantity)  # create 2 students
        assert len(Student.objects.all()) == students_quantity
        settings.MAX_STUDENTS_PER_COURSE = 2  # set this setting to 2 instead of 20
        students_pk = [student.pk for student in Student.objects.all()]
        course = Course.objects.first()
        new_data = {'students': students_pk}
        url = reverse('courses-detail', kwargs={'pk': course.pk})
        response = api_client.patch(url, data=new_data)  # add 2 students to our course
        assert response.status_code == HTTP_200_OK  # since 2 is allowed, it's ok

    def test_max_students_fail(self, api_client, course_factory, student_factory, settings):
        students_quantity = 3
        course_factory(_quantity=1)  # create 1 test course
        student_factory(_quantity=students_quantity)  # now trying to create 3 students
        assert len(Student.objects.all()) == students_quantity
        settings.MAX_STUDENTS_PER_COURSE = 2  # set this setting to 2 instead of 20
        students_pk = [student.pk for student in Student.objects.all()]
        course = Course.objects.first()
        new_data = {'students': students_pk}
        url = reverse('courses-detail', kwargs={'pk': course.pk})
        response = api_client.patch(url, data=new_data)  # trying to add 3 students
        assert response.status_code == HTTP_400_BAD_REQUEST  # it's not allowed, bad request

    def test_redirect(self):
        client = Client()
        response = client.get("")  # пустой путь home

        assert response.status_code == HTTP_302_FOUND
        assert response.url == "/api/v1/"  # redirect на api/v1/
