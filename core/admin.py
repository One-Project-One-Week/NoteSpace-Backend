from django.contrib import admin
from core.models import User, Notes, Summary

# Register your models here.
admin.site.register(User)
admin.site.register(Notes)
admin.site.register(Summary)

