# -*- coding: utf-8 -*-
from django.contrib import admin
from django.template.response import TemplateResponse

import cms
from cms.admin.placeholderadmin import PlaceholderAdmin
from cms.admin.placeholderadmin import FrontendEditableAdmin
from distutils.version import LooseVersion
from hvad.admin import TranslatableAdmin

from .forms import NewsForm, CategoryForm
from .models import News, Category, Tag, TaggedItem


class NewsAdmin(FrontendEditableAdmin, TranslatableAdmin, PlaceholderAdmin):

    list_display = ['__unicode__', 'publication_start', 'publication_end', 'all_translations']
    form = NewsForm
    frontend_editable_fields = ('title', 'lead_in')

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['title', 'slug', 'category', 'publication_start', 'publication_end']}),
            (None, {'fields': ['key_visual', 'lead_in', 'tags']})
        ]

        # show placeholder field if not CMS 3.0
        if LooseVersion(cms.__version__) < LooseVersion('3.0'):
            fieldsets.append(
                ('Content', {
                    'classes': ['plugin-holder', 'plugin-holder-nopage'],
                    'fields': ['content']}))

        return fieldsets

    def response_add(self, request, obj, post_url_continue=None):
        return TemplateResponse(request, 'aldryn_news/redirect_template.html',
                                {'redirect_url': obj.get_absolute_url()})

    def response_change(self, request, obj):
        return TemplateResponse(request, 'aldryn_news/redirect_template.html',
                                {'redirect_url': obj.get_absolute_url()})

admin.site.register(News, NewsAdmin)


class CategoryAdmin(TranslatableAdmin):

    form = CategoryForm
    list_display = ['__unicode__', 'all_translations', 'ordering']
    list_editable = ['ordering']

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['name', 'slug']}),
        ]
        return fieldsets

admin.site.register(Category, CategoryAdmin)


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem


class TagAdmin(TranslatableAdmin):

    list_display = ['__unicode__', 'all_translations']
    inlines = [TaggedItemInline]

    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            (None, {'fields': ['name', 'slug']}),
        ]
        return fieldsets


admin.site.register(Tag, TagAdmin)
