from django.contrib import admin
from .models import TestPlan, TestPlanStep

class TestPlanStepInline(admin.TabularInline):
    model = TestPlanStep
    extra = 1
    fields = ['section', 'step_order', 'step', 'procedure', 'day_time_duration', 'nq_duration', 'executor', 'comments']
    readonly_fields = []  # For now, allow editing

class TestPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    inlines = [TestPlanStepInline]

admin.site.register(TestPlan, TestPlanAdmin)

class TestPlanStepAdmin(admin.ModelAdmin):
    list_display = ['testplan', 'section', 'step_order', 'step']
    list_filter = ['section']
    ordering = ['testplan', 'section', 'step_order']

admin.site.register(TestPlanStep, TestPlanStepAdmin)