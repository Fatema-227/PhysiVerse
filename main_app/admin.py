from django.contrib import admin
from .models import Lab,Experiment,Comment

# Register your models here.
admin.site.register(Lab)
admin.site.register(Experiment)
admin.site.register(Comment)
