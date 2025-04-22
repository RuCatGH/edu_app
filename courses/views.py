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


# ==================== Course User Management Views ====================


class CourseUserAddAPIView(APIView):
    def post(self, request):
        serializer = CourseUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        course_id = serializer.validated_data['course']
        user_id = serializer.validated_data['user']
        role = serializer.validated_data.get('role', 0)  # Default to student

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        # Check if user is already in the course
        if user_id in course.students or user_id in course.teachers:
            return Response({"error": "User already in course"}, status=400)

        # Add user to appropriate list
        if role == 0:  # Student
            course.students.append(user_id)
        elif role == 1:  # Moderator
            course.teachers.append(user_id)
        else:
            return Response({"error": "Invalid role"}, status=400)

        course.save()
        return Response({"user": user_id})


class CourseUserDeleteAPIView(APIView):
    def post(self, request):
        serializer = CourseUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        course_id = serializer.validated_data['course']
        user_id = serializer.validated_data['user']

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        # Remove user from both lists
        if user_id in course.students:
            course.students.remove(user_id)
        if user_id in course.teachers:
            course.teachers.remove(user_id)

        course.save()
        return Response({"user": user_id})


class CourseUserUpdateAPIView(APIView):
    def post(self, request):
        serializer = CourseUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        course_id = serializer.validated_data['course']
        user_id = serializer.validated_data['user']
        new_role = serializer.validated_data.get('role')

        if new_role is None:
            return Response({"error": "Role is required"}, status=400)

        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=404)

        # Remove user from current role
        if user_id in course.students:
            course.students.remove(user_id)
        if user_id in course.teachers:
            course.teachers.remove(user_id)

        # Add user to new role
        if new_role == 0:  # Student
            course.students.append(user_id)
        elif new_role == 1:  # Moderator
            course.teachers.append(user_id)
        else:
            return Response({"error": "Invalid role"}, status=400)

        course.save()
        return Response({"user": user_id})


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
        # Convert single version to list for versioning
        if isinstance(request.data.get('data'), dict):
            request.data['data'] = [request.data['data']]

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

        # Update assignment data
        if 'data' in request.data:
            assignment.data = request.data['data']
        if 'title' in request.data:
            assignment.title = request.data['title']
        if 'active' in request.data:
            assignment.active = request.data['active']
        if 'attempts_allowed' in request.data:
            assignment.attempts_allowed = request.data['attempts_allowed']
        if 'start_date' in request.data:
            assignment.start_date = request.data['start_date']
        if 'end_date' in request.data:
            assignment.end_date = request.data['end_date']

        assignment.save()
        return Response({"id": assignment_id})


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
