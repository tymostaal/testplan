from django.contrib import admin
from .models import (
    TestPlan, TestPlanStep,
    TestPlanTemplate, TemplateStep,
    PredefinedStep,
)

# Inline for TestPlanSteps in a TestPlan
class TestPlanStepInline(admin.TabularInline):
    model = TestPlanStep
    extra = 1
    fields = ('section', 'step_order', 'step', 'procedure', 'day_time_duration', 'nq_duration', 'executor', 'comments')

class TestPlanAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [TestPlanStepInline]

admin.site.register(TestPlan, TestPlanAdmin)

# Inline for TemplateSteps in a TestPlanTemplate
class TemplateStepInline(admin.TabularInline):
    model = TemplateStep
    extra = 1
    fields = ('section', 'step_order', 'step', 'procedure', 'day_time_duration', 'nq_duration', 'executor', 'comments')

class TestPlanTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    inlines = [TemplateStepInline]

admin.site.register(TestPlanTemplate, TestPlanTemplateAdmin)

# Predefined Steps can be registered directly
admin.site.register(PredefinedStep)
