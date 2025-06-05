from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('result/', views.result_view, name='result'),
    path('cookies-required/', views.cookies_required, name='cookies_required'),
]
