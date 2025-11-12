from django.contrib import admin
from .models import Lab,Experiment,Comment,Profile

# Register your models here.
admin.site.register(Profile)
admin.site.register(Lab)
admin.site.register(Experiment)
admin.site.register(Comment)
