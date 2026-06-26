from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet, StudentViewSet, AttendanceViewSet

router = DefaultRouter()
router.register(r'teachers', TeacherViewSet)
router.register(r'students', StudentViewSet)
router.register(r'attendance', AttendanceViewSet)

urlpatterns = [
    # Pass the router urls directly! 
    # Your main backend/urls.py already handles the 'api/' prefix.
    path('', include(router.urls)), 
]