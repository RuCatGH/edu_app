from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import *
from .serializers import *
from courses.models import Assignment


# ==================== Question Views ====================
class QuestionCreateAPIView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data, status=201)
        return Response(serializer.errors, status=400)


class QuestionUpdateAPIView(APIView):
    def post(self, request):
        question_id = request.data.get('id')
        new_version = request.data.get('newVersion')

        try:
            question = Question.objects.get(id=question_id)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=404)

        question.data.append(new_version)
        question.save()
        return Response(QuestionSerializer(question).data)


class QuestionGetAPIView(APIView):
    def post(self, request):
        question_ids = request.data
        questions = Question.objects.filter(id__in=question_ids)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


# ==================== Attempt Views ====================
class AttemptGradeAPIView(APIView):
    def post(self, request):
        attempt_id = request.data.get('attempt')
        try:
            attempt = Attempt.objects.get(id=attempt_id)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt not found"}, status=404)

        attempt.grade = request.data.get('grade')
        attempt.save()
        return Response({"attempt": attempt_id})


class AttemptListAPIView(APIView):
    def post(self, request):
        search_type = request.data.get('typeSearch', 'user')
        user_id = request.data.get('user')
        task_id = request.data.get('task')
        course_id = request.data.get('course')
        attempt_ids = request.data.get('ids', [])

        attempts = Attempt.objects.all()

        if search_type == 'user' and user_id:
            attempts = attempts.filter(user=user_id)
        elif search_type == 'task' and task_id:
            attempts = attempts.filter(task_id=task_id)
        elif search_type == 'course' and course_id:
            attempts = attempts.filter(course_id=course_id)
        elif search_type == 'ids' and attempt_ids:
            attempts = Attempt.objects.filter(id__in=attempt_ids)
            # Create a list to maintain order
            result = []
            for attempt_id in attempt_ids:
                try:
                    attempt = attempts.get(id=attempt_id)
                    result.append(AttemptSerializer(attempt).data)
                except Attempt.DoesNotExist:
                    result.append({"id": attempt_id})
            return Response(result)

        serializer = AttemptSerializer(attempts, many=True)
        return Response(serializer.data)


class AttemptCreateAPIView(APIView):
    def post(self, request):
        serializer = AttemptSerializer(data=request.data)
        if serializer.is_valid():
            # Get the task
            task = Assignment.objects.get(
                id=serializer.validated_data['task'].id)
            user_id = serializer.validated_data['user']

            # Check if task is active
            if not task.active:
                return Response({"error": "Task is not active"}, status=400)

            # Check time restrictions
            now = timezone.now()
            if task.start_date and now < task.start_date:
                return Response({"error": "Task is not available yet"}, status=400)
            if task.end_date and now > task.end_date:
                return Response({"error": "Task is no longer available"}, status=400)

            # Check attempt limits
            if task.attempts_allowed != -1:  # -1 means unlimited attempts
                user_attempts = Attempt.objects.filter(
                    task=task,
                    user=user_id
                ).count()
                if user_attempts >= task.attempts_allowed:
                    return Response({"error": "Maximum attempts reached"}, status=400)

            # Check for active attempt
            active_attempt = Attempt.objects.filter(
                task=task,
                user=user_id,
                finished=False
            ).exists()

            if active_attempt:
                return Response({"error": "Active attempt exists"}, status=409)

            attempt = serializer.save()
            return Response({"attempt": attempt.id}, status=201)
        return Response(serializer.errors, status=400)


class AttemptUpdateAPIView(APIView):
    def post(self, request):
        attempt_id = request.data.get('attempt')
        try:
            attempt = Attempt.objects.get(id=attempt_id)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt not found"}, status=404)

        if attempt.finished:
            return Response({"error": "Attempt already finished"}, status=403)

        # Check if task is still available
        task = attempt.task
        now = timezone.now()
        if task.end_date and now > task.end_date:
            return Response({"error": "Task is no longer available"}, status=400)

        serializer = AttemptSerializer(
            attempt, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"attempt": attempt_id})
        return Response(serializer.errors, status=400)


class AttemptFinishAPIView(APIView):
    def post(self, request):
        attempt_id = request.data.get('attempt')
        try:
            attempt = Attempt.objects.get(id=attempt_id)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt not found"}, status=404)

        if attempt.finished:
            return Response({"error": "Attempt already finished"}, status=403)

        # Check if task is still available
        task = attempt.task
        now = timezone.now()
        if task.end_date and now > task.end_date:
            return Response({"error": "Task is no longer available"}, status=400)

        attempt.finished = True
        attempt.end_date = timezone.now()
        attempt.save()
        return Response({"attempt": attempt_id})
