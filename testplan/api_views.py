import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import TestPlan, TestPlanTemplate, PredefinedStep, TemplateStep, ChecklistResponse

def templates_list(request):
    templates = list(
        TestPlanTemplate.objects.all().values('id', 'name', 'description', 'folder', 'created_at')
    )
    return JsonResponse(templates, safe=False)

def predefined_steps_list(request):
    steps = list(
        PredefinedStep.objects.all().values(
            'id', 'name', 'folder', 'section', 'procedure', 'day_time_duration',
            'nq_duration', 'executor', 'comments'
        )
    )
    return JsonResponse(steps, safe=False)

def load_template(request, template_id):
    template = get_object_or_404(TestPlanTemplate, pk=template_id)
    steps = list(
        template.steps.all().values(
            'id', 'step_order', 'section', 'step', 'procedure',
            'day_time_duration', 'nq_duration', 'executor', 'comments'
        )
    )
    data = {
        'id': template.id,
        'name': template.name,
        'description': template.description,
        'folder': template.folder,
        'steps': steps,
    }
    return JsonResponse(data)

@csrf_exempt
def save_predefined_step(request):
    """
    Saves a step as a new PredefinedStep (for later reuse).
    Expected POST JSON:
    {
      "name": "Step Title",
      "description": "Step description",
      "folder": "Folder Name",   # optional
      "section": "preparation",   # or "execution" or "wrapup"
      "procedure": "...",
      "day_time_duration": "...",
      "nq_duration": "...",
      "executor": "...",
      "comments": "..."
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            step = PredefinedStep.objects.create(
                name=data.get('name'),
                description=data.get('description', ''),
                folder=data.get('folder', ''),
                section=data.get('section'),
                procedure=data.get('procedure', ''),
                day_time_duration=data.get('day_time_duration', ''),
                nq_duration=data.get('nq_duration', ''),
                executor=data.get('executor', ''),
                comments=data.get('comments', '')
            )
            return JsonResponse({'status': 'success', 'id': step.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@csrf_exempt
def save_template(request):
    """
    Saves the current testplan configuration as a new template.
    Expected POST JSON:
    {
      "name": "Template Name",
      "description": "Template description",
      "folder": "Folder Name",  # optional
      "steps": [
          {
              "step_order": 0,
              "section": "preparation",
              "step": "Step Title",
              "procedure": "...",
              "day_time_duration": "...",
              "nq_duration": "...",
              "executor": "...",
              "comments": "..."
          },
          ...
      ]
    }
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            template = TestPlanTemplate.objects.create(
                name=data.get('name'),
                description=data.get('description', ''),
                folder=data.get('folder', '')
            )
            steps = data.get('steps', [])
            for s in steps:
                TemplateStep.objects.create(
                    template=template,
                    step_order=s.get('step_order', 0),
                    section=s.get('section'),
                    step=s.get('step'),
                    procedure=s.get('procedure', ''),
                    day_time_duration=s.get('day_time_duration', ''),
                    nq_duration=s.get('nq_duration', ''),
                    executor=s.get('executor', ''),
                    comments=s.get('comments', '')
                )
            return JsonResponse({'status': 'success', 'id': template.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)


@csrf_exempt
def save_checklist(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            responses = data.get('responses')
            # For simplicity, we create a new TestPlan record here;
            # In a real scenario, you might tie this to a user session or an existing testplan.
            testplan = TestPlan.objects.create(title="New TestPlan from Checklist")
            ChecklistResponse.objects.create(testplan=testplan, responses=responses)
            return JsonResponse({'status': 'success', 'testplan_id': testplan.id})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)