from django.db import models
from django.contrib.auth.models import User

# Model for the resources


class Resource(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

# Model for the announcements

class Announcement(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    # True for general, False for specific students
    for_all = models.BooleanField(default=True)
    specific_student = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)  # Optional

    def __str__(self):
        if self.for_all:
            return f"BROADCAST: {self.message[:50]}..."  # General announcement
        else:
            # Specific announcement, showing the intended student
            return f"To {self.specific_student.username}: {self.message[:50]}..."

# Model for the marks


class Mark(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_title = models.CharField(max_length=255)
    score = models.IntegerField()

    def __str__(self):
        return f"{self.assignment_title} - {self.student.username} ({self.score})"


class Query(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={
                                'groups__name': "Students"})
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query from {self.student.username} at {self.timestamp}"
