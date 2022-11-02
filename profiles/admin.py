from django.contrib import admin
from .models import Review,ReportUser, ReportPost

admin.site.register(Review)
admin.site.register(ReportUser)
admin.site.register(ReportPost)