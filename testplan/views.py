from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.urls import reverse
from .models import TestPlan, TestPlanStep
from .forms import TestPlanStepForm

def testplan_create(request):
    # Create formset factories for each section, allowing one extra blank form.
    PreparationFormSet = modelformset_factory(
        TestPlanStep, form=TestPlanStepForm, extra=1, can_delete=True
    )
    ExecutionFormSet = modelformset_factory(
        TestPlanStep, form=TestPlanStepForm, extra=1, can_delete=True
    )
    WrapupFormSet = modelformset_factory(
        TestPlanStep, form=TestPlanStepForm, extra=1, can_delete=True
    )
    
    if request.method == 'POST':
        prep_formset = PreparationFormSet(request.POST, queryset=TestPlanStep.objects.none(), prefix='prep')
        exec_formset = ExecutionFormSet(request.POST, queryset=TestPlanStep.objects.none(), prefix='exec')
        wrap_formset = WrapupFormSet(request.POST, queryset=TestPlanStep.objects.none(), prefix='wrap')
        
        # Debug prints for errors if needed
        if not prep_formset.is_valid():
            print("Prep errors:", prep_formset.errors)
        if not exec_formset.is_valid():
            print("Exec errors:", exec_formset.errors)
        if not wrap_formset.is_valid():
            print("Wrap errors:", wrap_formset.errors)
        
        if prep_formset.is_valid() and exec_formset.is_valid() and wrap_formset.is_valid():
            # Create the parent TestPlan; you can extend this to include more details.
            testplan = TestPlan.objects.create(title="TestPlan created on now")
            
            # Process Preparation Steps
            for form in prep_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    step_instance = form.save(commit=False)
                    step_instance.section = 'preparation'
                    step_instance.testplan = testplan
                    # Optionally assign a default step_order if not provided
                    if not step_instance.step_order:
                        step_instance.step_order = 0
                    step_instance.save()
            
            # Process Execution Steps
            for form in exec_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    step_instance = form.save(commit=False)
                    step_instance.section = 'execution'
                    step_instance.testplan = testplan
                    if not step_instance.step_order:
                        step_instance.step_order = 0
                    step_instance.save()
            
            # Process Wrap-Up Steps
            for form in wrap_formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                    step_instance = form.save(commit=False)
                    step_instance.section = 'wrapup'
                    step_instance.testplan = testplan
                    if not step_instance.step_order:
                        step_instance.step_order = 0
                    step_instance.save()
            
            # Redirect to the detail view of the newly created TestPlan.
            return redirect(reverse('testplan_detail', args=[testplan.pk]))
        else:
            print("Form is not valid. Not redirecting.")
    else:
        # For GET: create empty formsets with initial data for the hidden fields.
        prep_formset = PreparationFormSet(
            queryset=TestPlanStep.objects.none(), 
            prefix='prep', 
            initial=[{'section': 'preparation', 'step_order': 0}]
        )
        exec_formset = ExecutionFormSet(
            queryset=TestPlanStep.objects.none(), 
            prefix='exec', 
            initial=[{'section': 'execution', 'step_order': 0}]
        )
        wrap_formset = WrapupFormSet(
            queryset=TestPlanStep.objects.none(), 
            prefix='wrap', 
            initial=[{'section': 'wrapup', 'step_order': 0}]
        )
    
    context = {
        'prep_formset': prep_formset,
        'exec_formset': exec_formset,
        'wrap_formset': wrap_formset,
    }
    return render(request, 'testplan/testplan_form.html', context)

def testplan_success(request):
    return render(request, 'testplan/testplan_success.html')

def testplan_detail(request, pk):
    testplan = get_object_or_404(TestPlan, pk=pk)
    prep_steps = testplan.steps.filter(section='preparation').order_by('step_order')
    exec_steps = testplan.steps.filter(section='execution').order_by('step_order')
    wrap_steps = testplan.steps.filter(section='wrapup').order_by('step_order')
    context = {
       'testplan': testplan,
       'prep_steps': prep_steps,
       'exec_steps': exec_steps,
       'wrap_steps': wrap_steps,
    }
    return render(request, 'testplan/testplan_detail.html', context)