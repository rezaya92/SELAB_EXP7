from authentication.views import CreateUserView, MyTokenObtainPairView, StatisticsView
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', CreateUserView.as_view(), name="signup"),
    path('statistics/', StatisticsView.as_view(), name="statistics"),
]
