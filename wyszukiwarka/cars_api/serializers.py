from typing import Any
from rest_framework import serializers
from cars import models
from django import forms
from django.contrib.admin import SimpleListFilter
from django.db.models import Q


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Car
        fields = ['id', 'brand', 'title', 'year', 'fuel', 'mileage', 'price', 
                    'engine_size', 'bhp_count', 'gearbox', 'summary', 'tk_lemmatized']
        
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Brand
        fields = ['id', 'name']

# class BrandFilter(SimpleListFilter):
#     title = "brand"

#     def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
#         return Brand.objects.all().values_list('id', 'name')
    
#     def queryset(self, request, queryset):
#         if self.value():
#             return queryset.filter(
#                 Q(brand_id=self.value()).filter(deleted=False)
#             )
#         return queryset


class SearchFormSerializer(serializers.Serializer):
    search = serializers.CharField()
    brand = serializers.ChoiceField(
        choices=models.Brand.objects.all().values_list('id', 'name'),
        required=False
    )

