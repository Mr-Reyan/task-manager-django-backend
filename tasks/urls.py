from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
router = DefaultRouter()
router.register(
    "tasks",
    TaskViewSet,
    basename="task"
)

urlpatterns = [
    path('register/',registerView),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView),
    path('token/refresh/',TokenRefreshView.as_view()),
    path('password_reset/',password_reset),
    path('password_reset_confirm/',password_reset_confirm),
]

urlpatterns += router.urls