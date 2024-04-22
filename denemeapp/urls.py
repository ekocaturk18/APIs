from django.urls import path
from . import views

urlpatterns = [
    path('api/a/', views.a, name='a'),
    path('api/b/', views.b, name='b'),
]
