from django.contrib import admin
from .models import WebPage, HeardFrom, GalleryImage, PageImage


class PageAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (('title', 'slug'), 'live', 'pub_date')
        }),
        (None, {
            'fields': ('template', 'content')
        }),
        ('Nav options', {
            'classes': ('collapse',),
            'fields': (('top_nav', 'main_nav', 'footer_nav'), 'weight', 'parent')
        }),
    )

admin.site.register(WebPage, PageAdmin)


class HeardFromAdmin(admin.ModelAdmin):
    list_display = ['value', 'frequency']
    fieldsets = (
        (None, {
            'fields': ('value',)
        }),
    )

admin.site.register(HeardFrom, HeardFromAdmin)


class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'caption', 'link', 'live']
    fieldsets = (
        (None, {
            'fields': (('title', 'image'), 'live', 'caption', 'tags', 'link', 'date')
        }),
    )

admin.site.register(GalleryImage, GalleryImageAdmin)


class PageImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image', 'page', 'caption', 'link']
    fieldsets = (
        (None, {
            'fields': (('title', 'image'), 'page', 'caption', 'date', 'tags', 'link')
        }),
    )

admin.site.register(PageImage, PageImageAdmin)