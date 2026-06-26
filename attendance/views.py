from rest_framework import viewsets
from .models import Teacher, Student, Attendance
from .serializers import TeacherSerializer, StudentSerializer, AttendanceSerializer

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    # Optional: Filter attendance by date if passed in the query params (e.g., /api/attendance/?date=2026-06-22)
    def get_queryset(self):
        queryset = Attendance.objects.all()
        date = self.request.query_params.get('date')
        if date is not None:
            queryset = queryset.filter(date=date)
        return queryset