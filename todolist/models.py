from django.db import models
from django.contrib.auth.models import User

PRIORITY_CHOICES = (
    ("High", "High"),
    ("Medium", "Medium"),
    ("Low", "Low"),
)

CATEGORY_CHOICES = (
    ("Work", "Work"),
    ("Study", "Study"),
    ("Personal", "Personal"),
    ("Health", "Health"),
    ("Other", "Other"),
)

class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default="Medium")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="Personal")

    due_date = models.DateField(null=True, blank=True)

    completed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.task


class ContactMessage(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
