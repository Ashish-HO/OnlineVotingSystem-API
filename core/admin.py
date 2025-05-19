from django.contrib import admin

# Register your models here.
from . import models

admin.site.register(models.Candidate)
admin.site.register(models.Voter)
admin.site.register(models.Post)
