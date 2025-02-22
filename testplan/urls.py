from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.testplan_create, name='testplan_create'),
    path('detail/<int:pk>/', views.testplan_detail, name='testplan_detail'),
    path('success/', views.testplan_success, name='testplan_success'),
]