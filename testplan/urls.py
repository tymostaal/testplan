from django.urls import path
from . import api_views
from . import views

urlpatterns = [
    # Existing testplan views
    path('create/', views.testplan_create, name='testplan_create'),
    path('detail/<int:pk>/', views.testplan_detail, name='testplan_detail'),
    
    # New wizard pages
    path('new/', views.new_testplan_landing, name='new_testplan_landing'),
    path('new/checklist/', views.new_testplan_checklist, name='new_testplan_checklist'),
    
    # API endpoints (existing)
    path('api/templates_list/', api_views.templates_list, name='templates_list'),
    path('api/predefined_steps_list/', api_views.predefined_steps_list, name='predefined_steps_list'),
    path('api/load_template/<int:template_id>/', api_views.load_template, name='load_template'),
    path('api/save_predefined_step/', api_views.save_predefined_step, name='save_predefined_step'),
    path('api/save_template/', api_views.save_template, name='save_template'),
    path('api/save_checklist/', api_views.save_checklist, name='save_checklist'),
]