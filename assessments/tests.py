from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from courses.models import Course, Assignment
from assessments.models import Question, Attempt


class AssessmentsBaseTestCase(TestCase):
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
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            course=self.course,
            creator=self.teacher,
            data={'questions': []}
        )
        self.question = Question.objects.create(
            course=self.course,
            creator=self.teacher,
            data=[{'question': 'Test question'}]
        )
        self.attempt = Attempt.objects.create(
            user=self.student,
            task=self.assignment,
            course=self.course,
            data={}
        )


class QuestionViewsTests(AssessmentsBaseTestCase):
    def test_question_create(self):
        url = reverse('assessments:question-create')
        data = {
            'data': [{'question': 'New question'}],
            'course': self.course.id,
            'creator': self.teacher.id
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_question_update(self):
        url = reverse('assessments:question-update')
        data = {
            'id': self.question.id,
            'newVersion': {'question': 'Updated question'}
        }
        self.client.force_authenticate(user=self.teacher)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(len(self.question.data), 2)


class AttemptTests(AssessmentsBaseTestCase):
    def test_grade_attempt(self):
        url = reverse('attempt-grade', args=[self.attempt.id])
        data = {'grade': 85}
        self.client.force_authenticate(user=self.teacher)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.grade, 85)

    def test_list_attempts(self):
        url = reverse('attempt-list') + '?userIds[]=' + str(self.student.id)
        self.client.force_authenticate(user=self.teacher)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_attempt(self):
        url = reverse('attempt-create')
        data = {
            'user': self.student.id,
            'task': self.assignment.id,
            'course': self.course.id,
            'data': {}
        }
        self.client.force_authenticate(user=self.student)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attempt.objects.count(), 2)

    def test_update_attempt(self):
        url = reverse('attempt-update', args=[self.attempt.id])
        data = {'data': {'answer': 'Test answer'}}
        self.client.force_authenticate(user=self.student)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attempt.refresh_from_db()
        self.assertIn('answer', self.attempt.data)

    def test_finish_attempt(self):
        url = reverse('attempt-finish', args=[self.attempt.id])
        self.client.force_authenticate(user=self.student)
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attempt.refresh_from_db()
        self.assertTrue(self.attempt.finished)
