
from django.urls import path
from user import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('main/', views.main, name='main'),
]
