from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import *
from .serializers import *


# ==================== Question Views ====================
class QuestionCreateAPIView(APIView):
    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            question = serializer.save()
            return Response(QuestionSerializer(question).data, status=201)
        return Response(serializer.errors, status=400)

class QuestionUpdateAPIView(APIView):
    def put(self, request):
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
    def post(self, request, attemptId):
        try:
            attempt = Attempt.objects.get(id=attemptId)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt not found"}, status=404)
        
        attempt.grade = request.data.get('grade')
        attempt.save()
        return Response(AttemptSerializer(attempt).data)

class AttemptListAPIView(APIView):
    def get(self, request):
        user_ids = request.query_params.getlist('userIds[]')
        course_ids = request.query_params.getlist('courseIds[]')
        
        attempts = Attempt.objects.all()
        if user_ids:
            attempts = attempts.filter(user__id__in=user_ids)
        if course_ids:
            attempts = attempts.filter(course__id__in=course_ids)
        
        serializer = AttemptSerializer(attempts, many=True)
        return Response(serializer.data)

class AttemptCreateAPIView(APIView):
    def post(self, request):
        serializer = AttemptSerializer(data=request.data)
        if serializer.is_valid():
            # Проверка ограничений
            task = serializer.validated_data['task']
            user = serializer.validated_data['user']
            
            # Проверка активной попытки
            active_attempt = Attempt.objects.filter(
                task=task, 
                user=user, 
                finished=False
            ).exists()
            
            if active_attempt:
                return Response({"error": "Active attempt exists"}, status=409)
                
            attempt = serializer.save()
            return Response(AttemptSerializer(attempt).data, status=201)
        return Response(serializer.errors, status=400)

class AttemptUpdateAPIView(APIView):
    def put(self, request, attemptId):
        try:
            attempt = Attempt.objects.get(id=attemptId)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt not found"}, status=404)
        
        if attempt.finished:
            return Response({"error": "Attempt already finished"}, status=403)
            
        serializer = AttemptSerializer(attempt, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

class AttemptFinishAPIView(APIView):
    def post(self, request, attemptId):
        try:
            attempt = Attempt.objects.get(id=attemptId)
        except Attempt.DoesNotExist:
            return Response({"error": "Attempt not found"}, status=404)
        
        attempt.finished = True
        attempt.end_date = timezone.now()
        attempt.save()
        return Response(AttemptSerializer(attempt).data)