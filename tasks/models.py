from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

PRIORITY_CHOICES = (
    ("LOW", "Low"),
    ("MEDIUM", "Medium"),
    ("HIGH", "High"),
    ("URGENT", "Urgent"),
)


STATUS_CHOICES = (
    ("TODO", "To Do"),
    ("IN_PROGRESS", "In Progress"),
    ("DONE", "Done"),
)


class Task(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='tasks',null=True)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default="LOW",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="TODO",
    )

    due_date = models.DateField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)