from django.contrib import admin

from ci_monitor.pull import models
admin.site.register(models.CiServer)
admin.site.register(models.CiJob)
admin.site.register(models.UserCiJob)