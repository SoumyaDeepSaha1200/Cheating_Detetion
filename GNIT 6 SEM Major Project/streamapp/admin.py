from django.contrib import admin
from streamapp.models import *
# Register your models here.
admin.site.register(course)
admin.site.register(teachers)
admin.site.register(modules)
admin.site.register(mcq)
admin.site.register(course_details)
admin.site.register(reply)
admin.site.register(AttendanceRecord)
admin.site.register(Profile)