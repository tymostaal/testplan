from django.db import models
from django.utils import timezone

# Main TestPlan and its Steps
class TestPlan(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class TestPlanStep(models.Model):
    SECTION_CHOICES = (
        ('preparation', 'Preparation Steps'),
        ('execution', 'Execution Steps'),
        ('wrapup', 'Wrap-Up Steps'),
    )
    testplan = models.ForeignKey(TestPlan, on_delete=models.CASCADE, related_name='steps')
    step_order = models.PositiveIntegerField(default=0)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    step = models.CharField(max_length=255)
    procedure = models.TextField(blank=True)
    day_time_duration = models.CharField(max_length=100, blank=True)
    nq_duration = models.CharField(max_length=100, blank=True)
    executor = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['section', 'step_order']
    
    def __str__(self):
        return f"{self.get_section_display()} - {self.step} (Order: {self.step_order})"

# Library of TestPlan Templates
class TestPlanTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    folder = models.CharField(max_length=255, blank=True, default="")  # NEW: Folder field for grouping templates
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class TemplateStep(models.Model):
    SECTION_CHOICES = (
        ('preparation', 'Preparation Steps'),
        ('execution', 'Execution Steps'),
        ('wrapup', 'Wrap-Up Steps'),
    )
    template = models.ForeignKey(TestPlanTemplate, on_delete=models.CASCADE, related_name='steps')
    step_order = models.PositiveIntegerField(default=0)
    section = models.CharField(max_length=20, choices=SECTION_CHOICES)
    step = models.CharField(max_length=255)
    procedure = models.TextField(blank=True)
    day_time_duration = models.CharField(max_length=100, blank=True)
    nq_duration = models.CharField(max_length=100, blank=True)
    executor = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    
    class Meta:
        ordering = ['section', 'step_order']
    
    def __str__(self):
        return f"{self.template.name} - {self.get_section_display()} - {self.step}"

# Library of Predefined Steps (individual reusable steps)
class PredefinedStep(models.Model):
    CATEGORY_CHOICES = (
        ('preparation', 'Preparation Steps'),
        ('execution', 'Execution Steps'),
        ('wrapup', 'Wrap-Up Steps'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    folder = models.CharField(max_length=255, blank=True, default="")  # NEW: Folder field for grouping predefined steps
    section = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    procedure = models.TextField(blank=True)
    day_time_duration = models.CharField(max_length=100, blank=True)
    nq_duration = models.CharField(max_length=100, blank=True)
    executor = models.CharField(max_length=100, blank=True)
    comments = models.TextField(blank=True)
    
    def __str__(self):
        return self.name


class ChecklistResponse(models.Model):
    testplan = models.ForeignKey('TestPlan', on_delete=models.CASCADE, related_name='checklist_responses')
    responses = models.JSONField(default=dict)  # Requires Django 3.1+; stores all responses as JSON
    saved_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Checklist for {self.testplan.title} at {self.saved_at}"