# testplan/api_views.py

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import TestPlanTemplate, PredefinedStep

def templates_list(request):
    """
    Returns a JSON list of all testplan templates.
    """
    templates = list(
        TestPlanTemplate.objects.all().values('id', 'name', 'description', 'created_at')
    )
    return JsonResponse(templates, safe=False)

def predefined_steps_list(request):
    """
    Returns a JSON list of all predefined steps.
    """
    steps = list(
        PredefinedStep.objects.all().values(
            'id', 'name', 'section', 'procedure', 'day_time_duration', 'nq_duration', 'executor', 'comments'
        )
    )
    return JsonResponse(steps, safe=False)

def load_template(request, template_id):
    """
    Loads a specific template, returning its metadata and its steps.
    """
    template = get_object_or_404(TestPlanTemplate, pk=template_id)
    steps = list(
        template.steps.all().values(
            'id', 'step_order', 'section', 'step', 'procedure', 'day_time_duration', 'nq_duration', 'executor', 'comments'
        )
    )
    data = {
        'id': template.id,
        'name': template.name,
        'description': template.description,
        'steps': steps,
    }
    return JsonResponse(data)
