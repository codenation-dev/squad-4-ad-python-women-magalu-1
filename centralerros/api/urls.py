from django.urls import include, path, re_path
from django.contrib import admin
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserApiViewSet)
router.register(r'agents', views.AgentApiViewSet)
router.register(r'events', views.EventApiViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('environments/', views.EnvironmentListOnlyAPIView.as_view()),
    path('levels/', views.LevelListOnlyAPIView.as_view()),
    path('auth/', include('rest_auth.urls')),
]
