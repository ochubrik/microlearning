from django.contrib import admin
from . import models


# Register your models here.
@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'type', 'status', 'publish')
    list_filter = ('status', 'type', 'publish')
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
