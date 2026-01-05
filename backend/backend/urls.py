from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from accounts.views import LoginView
from employees.views import EmployeeViewSet, DepartmentViewSet
from attendance.views import AttendanceViewSet
from payroll.views import PayrollViewSet

router = DefaultRouter()
router.register('employees', EmployeeViewSet)
router.register('departments', DepartmentViewSet)
router.register('attendance', AttendanceViewSet)
router.register('payroll', PayrollViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', LoginView.as_view()),
]

urlpatterns += router.urls
