from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

# Register your models here.
from . import models

# Allows us to sort of mimic the behavior of foreign keys in the admin... making
# them inline
class TaggedItemInline(GenericTabularInline):
    model = models.TaggedItem

class MoveAdmin(admin.ModelAdmin):
    inlines = [TaggedItemInline]
    list_display = ["__unicode__", "slug"]
    fields = ["title", "order", "embed_code", "share_message", "featured", "active",
    "move_type", "slug"]
    # this auto creates slug fields
    # fields = ["title", "embed_code", "slug"]
    # prepopulated_fields = {'slug': ["title",]}

    class Meta:
        model = models.Move

class MoveInline(admin.TabularInline): #make moves inline
    model = models.Move

class TypeAdmin(admin.ModelAdmin):
    inlines = [MoveInline, TaggedItemInline]
    class Meta:
        model = models.Type

admin.site.register(models.Move, MoveAdmin)
admin.site.register(models.Type, TypeAdmin)
admin.site.register(models.TaggedItem)
# admin.site.register(models.UserType)
