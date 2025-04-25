from django.contrib import admin
from note_management.models import Note, Summary, Bookmark
# Register your models here.
admin.site.register(Note)
admin.site.register(Summary)
admin.site.register(Bookmark)
