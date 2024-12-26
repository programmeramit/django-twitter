from django.contrib import admin
from .models import *

admin.site.register(Tweet)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(HashTag)
admin.site.register(Profile)
admin.site.register(Bookmark)

