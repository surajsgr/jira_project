from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from users.models import Profile
from django.urls import reverse


class Task(models.Model):
    status_list = [("Assigned", "Assigned"), ("In Progress", "In Progress"), ("QA", "Moved to QA"),
                   ("Completed", "Completed")]
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=status_list, default="Assigned")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('task-home')




