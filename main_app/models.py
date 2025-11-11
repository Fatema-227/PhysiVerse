from django.db import models
from django.urls import reverse

# Create your models here.
class Lab(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=100)
    image=models.ImageField(upload_to='main_app/static/uploads/',default="")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Experiment(models.Model):
    title=models.CharField(max_length=100)
    description=models.TextField(max_length=100)
    Simulation_Data=models.TextField()
    image=models.ImageField(upload_to='main_app/static/image/',default="")
    video=models.FileField(upload_to='main_app/static/videos/',default="")
    created_at=models.DateTimeField(auto_now_add=True)
    lab=models.ForeignKey(Lab,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

