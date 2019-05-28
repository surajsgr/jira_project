from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# from users.models import Profile
from django.urls import reverse
import request


class Task(models.Model):
    status_list = [("Assigned", "Assigned"), ("In Progress", "In Progress"), ("QA", "Moved to QA"),
                   ("Completed", "Completed")]
    title = models.CharField(max_length=100)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, choices=status_list, default="Assigned")
    completion_date=models.DateTimeField(default=timezone.now())

    def publish(self):
        self.date_posted = timezone.now()
        self.save()

    def __str__(self):
        return self.title

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        print("task view found model")
        return reverse("task-home")



class Comment(models.Model):
    task = models.ForeignKey('task.Task', related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("task-home")

    def __str__(self):
        return self.text




