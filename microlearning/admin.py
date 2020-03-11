from django.contrib import admin
from . import models


# Register your models here.
# class ArticleInstanceInline(admin.TabularInline):
#     model = 'ArticleInstance'


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'type', 'publish', 'status')
    # inlines = [ArticleInstanceInline]
    list_filter = ('type', 'publish', 'status')
    date_hierarchy = 'publish'
    ordering = ('publish', 'status')


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
