from django.contrib import admin
from user.models import Profile, LoginLog

admin.site.register(Profile)
admin.site.register(LoginLog)
