from django.contrib import admin
from cars import models

# Register your models here.
@admin.register(models.Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(models.Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'brand', 'title', 'year', 'fuel', 'mileage', 'price', 
                    'engine_size', 'bhp_count', 'gearbox', 'summary', 'tk_lemmatized']
