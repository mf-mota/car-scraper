from django.urls import path
from .views import CarCreateListView, BrandCreateListView, SingleCarView, SingleBrandView, AdvancedTextSearchCar

app_name = "cars_api"

urlpatterns = [
    path("cars/", CarCreateListView.as_view(), name="car_mult"),
    path("brands/", BrandCreateListView.as_view(), name="brands_mul"),
    path("cars/<int:pk>/", SingleCarView.as_view(), name="single_car"),
    path("brands/<int:pk>/", SingleBrandView.as_view(), name="single_brand"),
    path("cars/search/", AdvancedTextSearchCar.as_view(), name="car_search")
]