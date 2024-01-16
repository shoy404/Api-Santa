# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, ObtainTokenView

router = DefaultRouter()
router.register(r'usuarios', CustomUserViewSet, basename='usuario')

urlpatterns = [
    path('', include(router.urls)),
    path('token/', ObtainTokenView.as_view(), name='obtain_token'),
    path('usuarios/', CustomUserViewSet.as_view({'post': 'create'}), name='create_user'),
]
