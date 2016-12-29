from django.contrib import admin
from .models import SortLocation, Sort, SortLocationItem

# Register your models here.
admin.site.register(SortLocation)
admin.site.register(Sort)
admin.site.register(SortLocationItem)
