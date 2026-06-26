from rest_framework import serializers
from .models import Teacher, Student, Attendance

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'name', 'email']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'roll_number']

class AttendanceSerializer(serializers.ModelSerializer):
    # This nested serializer allows us to see full student details in GET requests
    student_details = StudentSerializer(source='student', read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_details', 'teacher', 'date', 'status']