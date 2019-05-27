from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone


# class Group(models.Model):
#     Group_name = models.CharField(max_length=100,blank=True,default=None)
#     created_date = models.DateTimeField(default=timezone.now)



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    # group_name=models.ForeignKey(Group,on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        return super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


