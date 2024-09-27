# tools/admin.py
from django.contrib import admin
from .models import Tool, CO2Absorption, Category

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'co2_emission', 'category', 'is_electric', 'energy_class')
    list_filter = ('category', 'is_electric', 'energy_class')
    search_fields = ('name', 'category__name')

    # def alternatives_display(self, obj):
    #     return ", ".join([alt.name for alt in obj.alternatives.all()])
    # alternatives_display.short_description = 'Alternatywy'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
