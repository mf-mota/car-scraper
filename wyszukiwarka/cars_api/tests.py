from rest_framework.test import APITestCase
from cars.models import Car, Brand
from cars import data_processer as dp
from django.urls import reverse
from rest_framework import status
from django.db.models.deletion import ProtectedError
import statistics as stats


class BaseAPITestCase(APITestCase):
    def setUp(self):
        brand_1 = Brand.objects.create(
            name="TestBrand"
        )
        brand_2 = Brand.objects.create(
            name="TestBrand2"
        )
        Car.objects.create(
            brand_id = brand_1.id,
            title="TestBrand Vehicle 2.0",
            summary="Silnik 2.0 diesel, 150 KM, serwisowany do końca w ASO. Panorama i Alcantara",
            engine_size=1998,
            bhp_count=179,
            mileage=90570,
            fuel="diesel",
            gearbox="manualna",
            year=2016,
            price=78000,
            tk_lemmatized = dp.tokenize_lemmatize("Silnik 2.0 diesel, 150 KM, serwisowany do końca w ASO. Panorama i Alcantara")
        )
        Car.objects.create(
            brand_id = brand_1.id,
            title="TestBrand Vehicle 1.8 150",
            summary="Śliczny biały kolor. Dostępny od ręki. Od 1 właściciela. Alkantara",
            engine_size=1800,
            bhp_count=150,
            mileage=50000,
            fuel="benzyna",
            gearbox="manualna",
            year=2018,
            price=67000,
            tk_lemmatized = dp.tokenize_lemmatize("Śliczny biały kolor. Dostępny od ręki. 1 właściciel")
        )
        Car.objects.create(
            brand_id = brand_2.id,
            title="TestBrand2 Focus 1.6R2",
            summary="Focus 1.6, Nowe sprzęgło, rozrząd!!",
            engine_size=1599,
            bhp_count=170,
            mileage=350900,
            fuel="benzyna",
            gearbox="manualna",
            year=2009,
            price=30450,
            tk_lemmatized = dp.tokenize_lemmatize("Focus 1.6, Nowe sprzęgło, rozrząd!!")
        )

class ListingEndpointTest(BaseAPITestCase):
    # List Views (GET)
    def test_get_all_cars(self):
        url = reverse('cars_api:car_mult')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 3)


    def test_get_all_brands(self):
        url = reverse('cars_api:brands_mul')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 2)


    # Single Instance Views (GET)
    def test_single_car_get(self):
        car = Car.objects.all().first()
        url = reverse('cars_api:single_car', args=[car.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], car.title)


    def test_single_brand_get(self):
        brand = Brand.objects.all().first()
        url = reverse('cars_api:single_brand', args=[brand.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], brand.name)


    # POST Methods
    def test_car_post(self):
        url = reverse('cars_api:car_mult')
        brand = Brand.objects.first()
        new_data = {
            "brand": brand.id,
            "title": "TestBrand Vehicle 2.0",
            "summary": "Silnik 2.0 diesel, 150 KM, serwisowany do końca w ASO. Panorama i Alcantara",
            "engine_size": 1998,
            "bhp_count": 179,
            "mileage": 90570,
            "fuel": "diesel",
            "gearbox": "manualna",
            "year": 2016,
            "price":78000,
            "tk_lemmatized": dp.tokenize_lemmatize("Silnik 2.0 diesel, 150 KM, serwisowany do końca w ASO. Panorama i Alcantara")
        }
        response = self.client.post(url, new_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_brand_post(self):
        url = reverse('cars_api:brands_mul')
        new_brand = {
            "name": "Brand new example"
        }
        response = self.client.post(url, new_brand, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    

    # DELETE
    def test_brand_delete(self):
        brand = Brand.objects.first()
        url = reverse('cars_api:single_brand', args=[brand.id])
        try:
            self.client.delete(url)
        except ProtectedError: 
            pass
        else:
            self.assertFalse(True)


    def test_car_delete(self):
        car = Car.objects.first()
        url = reverse('cars_api:single_car', args=[car.id])
        response = self.client.delete(url)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


    # KEY WORD SEARCH TEST
        
    def test_car_keyword_search(self):
        car = Car.objects.all().filter(title="TestBrand Vehicle 2.0").first()
        url = reverse('cars_api:car_search')
        data = {"brand": car.brand_id, 
                "search": "ąlcatára"
                }
        
        response = self.client.post(url, data)
        self.assertGreaterEqual(response.data["Key Values"]["offer_count"], 1)


    def test_car_keyword_search_stats(self):
        brand_id = Brand.objects.all().filter(name="TestBrand").first().id
        cars = Car.objects.all().filter(brand_id=brand_id)
        url = reverse('cars_api:car_search') # there are 2 cars with this brand
        data = {"brand": brand_id, 
                "search": "ąlcantára"
                }
        
        response = self.client.post(url, data)
        values = response.data["Key Values"]
        self.assertEqual(values["offer_count"], 2)
        self.assertGreaterEqual(values["avg_price"], stats.mean([car.price for car in cars]))
        self.assertEqual(values["avg_year"], stats.mean([car.year for car in cars]))
        self.assertEqual(values["avg_mileage"], stats.mean([car.mileage for car in cars]))
        self.assertEqual(values["avg_bhp"], stats.mean([car.bhp_count for car in cars]))
        self.assertEqual(values["min_price"], min([car.price for car in cars]))
        self.assertEqual(values["max_price"], max([car.price for car in cars]))


