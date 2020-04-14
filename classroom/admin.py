from django.contrib import admin
from .models import Profile, Subject,  Student



# Register your models here.

admin.site.register(Profile)
admin.site.register(Student)
admin.site.register(Subject)
