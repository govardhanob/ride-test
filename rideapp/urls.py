from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import RegisterViewSet, RideViewSet, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register('register', RegisterViewSet, basename='register')
router.register('rides', RideViewSet, basename='ride')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
