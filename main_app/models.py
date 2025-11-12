from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default="", upload_to='main_app/static/image/profiles/')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

class Lab(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=900)
    image=models.ImageField(upload_to='main_app/static/uploads/',default="")
    created_at=models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('labs_detail', kwargs={'pk': self.id})


class Experiment(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=900)
    Simulation_Data=models.TextField()
    image=models.ImageField(upload_to='main_app/static/image/',default="")
    video=models.FileField(upload_to='main_app/static/videos/',default="")
    created_at=models.DateTimeField(auto_now_add=True)
    lab=models.ForeignKey(Lab,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('experiments_detail', kwargs={'pk': self.id})


class Comment(models.Model):
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    experiment=models.ForeignKey(Experiment,on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Comment by {self.user}"

    def get_absolute_url(self):
        return reverse('comments_detail', kwargs={'pk': self.id})
