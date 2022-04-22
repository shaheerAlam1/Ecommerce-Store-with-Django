from django.contrib import admin
from .models import Tag, TaggedItem 
# Register your models here.
admin.site.register(Tag)
admin.site.register(TaggedItem)