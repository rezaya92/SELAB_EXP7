from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.models import User

from .serializers import UserSerializer


class CreateUserView(CreateAPIView):

    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['national_id'] = user.username
        token['is_doctor'] = user.is_doctor
        token['is_patient'] = user.is_patient
        token['is_admin'] = user.is_superuser
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class MyAuthClass(JWTAuthentication):
    def get_raw_token(self, header):
        return header


class StatisticsView(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [MyAuthClass]
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        users = User.objects.all()
        user_statistics = [{'count': users.filter(date_joined__day=x.day, date_joined__month=x.month,
                                                  date_joined__year=x.year).count(), 'date': x}
                           for x in users.dates('date_joined', 'day')]
        doctors = users.filter(is_doctor=True)
        doctor_statistics = [{'count': doctors.filter(date_joined__day=x.day, date_joined__month=x.month,
                                                      date_joined__year=x.year).count(), 'date': x}
                             for x in doctors.dates('date_joined', 'day')]

        return Response({'user_statistics': user_statistics, 'doctor_statistics': doctor_statistics})
