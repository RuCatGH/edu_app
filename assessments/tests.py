from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from courses.models import Course, Assignment
from assessments.models import Question, Attempt


class AssessmentsBaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher_id = 'teacher123'
        self.student_id = 'student123'
        self.course = Course.objects.create(
            title='Test Course',
            description='Test Description',
            owner=self.teacher_id
        )
        self.assignment = Assignment.objects.create(
            title='Test Assignment',
            course=self.course,
            creator=self.teacher_id,
            data={'questions': []}
        )
        self.question = Question.objects.create(
            course=self.course,
            creator=self.teacher_id,
            data=[{'question': 'Test question'}]
        )
        self.attempt = Attempt.objects.create(
            user=self.student_id,
            task=self.assignment,
            course=self.course,
            data={},
            finished=False
        )


class QuestionViewsTests(AssessmentsBaseTestCase):
    def test_question_create(self):
        url = reverse('assessments:question-create')
        data = {
            'data': [{'question': 'New question'}],
            'course': self.course.id,
            'creator': self.teacher_id
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_question_update(self):
        url = reverse('assessments:question-update')
        data = {
            'id': self.question.id,
            'newVersion': {'question': 'Updated question'}
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.question.refresh_from_db()
        self.assertEqual(len(self.question.data), 2)


class AttemptTests(AssessmentsBaseTestCase):
    def test_grade_attempt(self):
        url = reverse('assessments:attempt-grade')
        data = {
            'attempt': self.attempt.id,
            'grade': 85
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.grade, 85)

    def test_list_attempts(self):
        url = reverse('assessments:attempt-list')
        data = {
            'typeSearch': 'user',
            'user': self.student_id
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_attempt(self):
        url = reverse('assessments:attempt-create')
        data = {
            'user': self.student_id,
            'task': self.assignment.id,
            'course': self.course.id,
            'data': {}
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Attempt.objects.count(), 1)

    def test_update_attempt(self):
        url = reverse('assessments:attempt-update')
        data = {
            'attempt': self.attempt.id,
            'data': {'answer': 'Test answer'}
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attempt.refresh_from_db()
        self.assertIn('answer', self.attempt.data)

    def test_finish_attempt(self):
        url = reverse('assessments:attempt-finish')
        data = {
            'attempt': self.attempt.id
        }
        self.client.force_authenticate(user=None)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.attempt.refresh_from_db()
        self.assertTrue(self.attempt.finished)
