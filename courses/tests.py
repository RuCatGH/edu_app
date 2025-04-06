from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from courses.models import Course, Lecture, Assignment


class CoursesBaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = User.objects.create_user(
            username='teacher',
            password='testpass123',
            is_staff=True
        )
        self.student = User.objects.create_user(
            username='student',
            password='testpass123'
        )
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.teacher
        )
        self.lecture = Lecture.objects.create(
            title='Test Lecture',
            course=self.course,
            creator=self.teacher,
            data={'content': 'Test content'}
        )
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            course=self.course,
            creator=self.teacher,
            data={'questions': []}
        )


class CourseTests(CoursesBaseTestCase):
    def test_create_course(self):
        url = reverse('courses:course-create')
        data = {
            'title': 'New Course',
            'description': 'New Description',
            'owner': self.teacher.id
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_update_course(self):
        url = reverse('courses:course-update')
        data = {
            'id': self.course.id,
            'title': 'Updated Title',
            'description': 'Updated Description'
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.title, 'Updated Title')

    def test_delete_course(self):
        url = reverse('courses:course-delete')
        data = {'id': self.course.id}
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.count(), 0)

    def test_get_courses(self):
        url = reverse('courses:course-get')
        data = [self.course.id]
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.course.id)


class LectureTests(CoursesBaseTestCase):
    def test_create_lecture(self):
        url = reverse('courses:lecture-create')
        data = {
            'title': 'New Lecture',
            'data': {'content': 'New content'},
            'course': self.course.id,
            'creator': self.teacher.id,
            'activate': True
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lecture.objects.count(), 2)

    def test_update_lecture(self):
        url = reverse('courses:lecture-update')
        data = {
            'id': self.lecture.id,
            'title': 'Updated Lecture',
            'data': {'content': 'Updated content'}
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lecture.refresh_from_db()
        self.assertEqual(self.lecture.title, 'Updated Lecture')

    def test_delete_lecture(self):
        url = reverse('courses:lecture-delete')
        data = {'id': self.lecture.id}
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lecture.objects.count(), 0)

    def test_get_lectures(self):
        url = reverse('courses:lecture-get')
        data = [self.lecture.id]
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.lecture.id)


class AssignmentTests(CoursesBaseTestCase):
    def test_create_assignment(self):
        url = reverse('courses:task-create')
        data = {
            'title': 'New Assignment',
            'data': {'questions': []},
            'course': self.course.id,
            'creator': self.teacher.id,
            'active': True,
            'attempts': 3
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assignment.objects.count(), 2)

    def test_update_assignment(self):
        url = reverse('courses:task-update')
        data = {
            'id': self.assignment.id,
            'title': 'Updated Assignment',
            'data': {'questions': [{'q1': 'test'}]}
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assignment.refresh_from_db()
        self.assertEqual(self.assignment.title, 'Updated Assignment')

    def test_get_assignments(self):
        url = reverse('courses:task-get')
        data = [self.assignment.id]
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['id'], self.assignment.id)
