from django.contrib import admin

from .models import Profile, Question, Answer, Tag, Like

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
admin.site.register(Like)