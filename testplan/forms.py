# testplan/forms.py
from django import forms
from .models import TestPlanStep

class TestPlanStepForm(forms.ModelForm):
    class Meta:
        model = TestPlanStep
        fields = ['step_order', 'section', 'step', 'procedure',
                  'day_time_duration', 'nq_duration', 'executor', 'comments']
        widgets = {
            'step_order': forms.NumberInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-2 py-1'
            }),
            'step': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-2 py-1'
            }),
            'procedure': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-2 py-1 resize-y',
                'rows': 1,
            }),
            'day_time_duration': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-2 py-1'
            }),
            'nq_duration': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-2 py-1'
            }),
            'executor': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded px-2 py-1'
            }),
            'comments': forms.Textarea(attrs={
                'class': 'w-full border border-gray-300 rounded px-2 py-1 resize-y',
                'rows': 1,
            }),
            'section': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make hidden fields not required so that missing input won't trigger a validation error.
        self.fields['section'].required = False
        self.fields['step_order'].required = False