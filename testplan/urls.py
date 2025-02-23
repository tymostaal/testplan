from django.urls import path
from . import api_views
from . import views  # existing views

urlpatterns = [
    # Existing testplan views
    path('create/', views.testplan_create, name='testplan_create'),
    path('detail/<int:pk>/', views.testplan_detail, name='testplan_detail'),
    
    # API endpoints
    path('api/templates/', api_views.templates_list, name='templates_list'),
    path('api/predefined_steps/', api_views.predefined_steps_list, name='predefined_steps_list'),
    path('api/load_template/<int:template_id>/', api_views.load_template, name='load_template'),
]