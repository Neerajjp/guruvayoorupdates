from django.urls import path, re_path
from main import views


app_name = "main"

urlpatterns = [
    re_path(r'^$', views.dashboard, name='dashboard'),
]