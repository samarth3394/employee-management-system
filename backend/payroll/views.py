from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import serializers
from .models import Payroll


class PayrollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payroll
        fields = '__all__'


class PayrollViewSet(ModelViewSet):
    queryset = Payroll.objects.all()
    serializer_class = PayrollSerializer

    # 🔐 LOGIN REQUIRED (login_required equivalent)
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
