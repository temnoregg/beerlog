from django.contrib import admin

from models import *

class IngredientInline(admin.TabularInline):
    model = Ingredient


class LogInline(admin.TabularInline):
    model = Log

class BeerAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date_started', 'date_finished', 'is_active')
    list_filter = ('is_active', 'category')
    inlines = [IngredientInline, LogInline]
    

admin.site.register(Beer, BeerAdmin)
admin.site.register(Log)
admin.site.register(Ingredient)
admin.site.register(Category)