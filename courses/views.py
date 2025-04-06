from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import *
from .serializers import *

# ==================== Course Views ====================


class CourseCreateAPIView(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            course = serializer.save()
            return Response({"id": course.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=400)


class CourseUpdateAPIView(APIView):
    def post(self, request):
        course_id = request.data.get('id')
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"id": course_id})
        return Response(serializer.errors, status=400)


class CourseDeleteAPIView(APIView):
    def post(self, request):
        course_id = request.data.get('id')
        try:
            course = Course.objects.get(id=course_id)
            course.delete()
            return Response({"id": course_id})
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)


class CourseGetAPIView(APIView):
    def post(self, request):
        course_ids = request.data
        response = []
        for cid in course_ids:
            try:
                course = Course.objects.get(id=cid)
                serializer = CourseSerializer(course)
                response.append(serializer.data)
            except Course.DoesNotExist:
                response.append({"id": cid})
        return Response(response)

# ==================== Lecture Views ====================


class LectureCreateAPIView(APIView):
    def post(self, request):
        serializer = LectureSerializer(data=request.data)
        if serializer.is_valid():
            lecture = serializer.save()
            return Response({"id": lecture.id}, status=201)
        return Response(serializer.errors, status=400)


class LectureUpdateAPIView(APIView):
    def post(self, request):
        lecture_id = request.data.get('id')
        try:
            lecture = Lecture.objects.get(id=lecture_id)
        except Lecture.DoesNotExist:
            return Response({"error": "Lecture not found"}, status=404)

        serializer = LectureSerializer(
            lecture, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"id": lecture_id})
        return Response(serializer.errors, status=400)


class LectureDeleteAPIView(APIView):
    def post(self, request):
        lecture_id = request.data.get('id')
        try:
            lecture = Lecture.objects.get(id=lecture_id)
            lecture.delete()
            return Response({"id": lecture_id})
        except Lecture.DoesNotExist:
            return Response({"error": "Lecture not found"}, status=404)


class LectureGetAPIView(APIView):
    def post(self, request):
        lecture_ids = request.data
        response = []
        for lid in lecture_ids:
            try:
                lecture = Lecture.objects.get(id=lid)
                serializer = LectureSerializer(lecture)
                response.append(serializer.data)
            except Lecture.DoesNotExist:
                response.append({"id": lid})
        return Response(response)

# ==================== Assignment Views ====================


class AssignmentCreateAPIView(APIView):
    def post(self, request):
        serializer = AssignmentSerializer(data=request.data)
        if serializer.is_valid():
            assignment = serializer.save()
            return Response({"id": assignment.id}, status=201)
        return Response(serializer.errors, status=400)


class AssignmentUpdateAPIView(APIView):
    def post(self, request):
        assignment_id = request.data.get('id')
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return Response({"error": "Assignment not found"}, status=404)

        serializer = AssignmentSerializer(
            assignment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"id": assignment_id})
        return Response(serializer.errors, status=400)


class AssignmentGetAPIView(APIView):
    def post(self, request):
        assignment_ids = request.data
        response = []
        for aid in assignment_ids:
            try:
                assignment = Assignment.objects.get(id=aid)
                serializer = AssignmentSerializer(assignment)
                response.append(serializer.data)
            except Assignment.DoesNotExist:
                response.append({"id": aid})
        return Response(response)
