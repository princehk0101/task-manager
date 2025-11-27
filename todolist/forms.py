from django import forms
from .models import Task, ContactMessage

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['task', 'description', 'priority', 'category', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']
