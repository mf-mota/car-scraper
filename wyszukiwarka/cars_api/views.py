from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from cars import models
from . import serializers as slz
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django import forms
from django_pandas.io import read_frame
from cars import data_processer as dp
from django.db import transaction



# Create your views here.

# List Create -> docs: Used for read-write endpoints to represent a collection of model instances.
class CarCreateListView(generics.ListCreateAPIView):
    queryset = models.Car.objects.all()
    serializer_class = slz.CarSerializer

class BrandCreateListView(generics.ListCreateAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = slz.BrandSerializer

# RetrieveUpdateDestroyAPIView -> Used for read-write-delete endpoints to represent a single model instance.

class SingleCarView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Car.objects.all()
    serializer_class = slz.CarSerializer

class SingleBrandView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Brand.objects.all()
    serializer_class = slz.BrandSerializer

class AdvancedTextSearchCar(APIView):
    serializer_class = slz.SearchFormSerializer
    description = "This view can be used for advanced text search. \
                   \nA separate version where the summary of each vehicle \
                   was previously tokenized and lemmatized"

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        search_term = serializer.validated_data['search']
        brand = serializer.validated_data['brand']

        print(search_term, brand)
        # qs = models.Car.objects.all().filter(brand_id=)
        queryset = models.Car.objects.all().filter(brand_id=brand)

        df = read_frame(queryset)
        df.to_csv("before.csv")
        
        print(df)

        processed_df = dp.process_df_summary(df)
        processed_df.to_csv("after.csv")

        filtered_df = dp.retrieve_filtered(dataframe=processed_df, keyword=search_term)
        matching_ids = filtered_df['id'].tolist()

        queryset = models.Car.objects.filter(id__in=matching_ids)
        serializer = slz.CarSerializer(queryset, many=True)


        stats = {"Search Term": search_term, "Key Values": dp.calculate_stats(filtered_df), "cars": serializer.data}

        return Response(stats, status=status.HTTP_200_OK)

