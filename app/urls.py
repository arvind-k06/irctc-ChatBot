from django.conf.urls import url
from app import views

urlpatterns = [
    url(r'^v1/', views.train)
]